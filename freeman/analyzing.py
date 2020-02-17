import sys

import pandas as pd
import networkx as nx

try:
    import seaborn as sns
except NotImplementedError:
    sns = None

from math import isclose, sqrt, log
from statistics import variance
from random import choices, sample
from itertools import product, permutations, combinations
from scipy.stats import shapiro, normaltest, kstest, norm, powerlaw, expon, pearsonr, chi2_contingency, ttest_1samp, ttest_ind, ttest_rel
from scipy.cluster.hierarchy import dendrogram
from statsmodels.api import OLS, Logit

try:
    from prince import CA

    from matplotlib import pyplot as plt
except NotImplementedError:
    pass

from .drawing import get_node_label
from .exploring import Log


DPI = 100

DEC = 6


def _varzero(a):
    return isclose(variance(a), 0)


def _product(population, k, max_perm):
    return (choices(population, k=k) for _ in range(max_perm))


def _permutations(population, max_perm):
    return (sample(population, len(population)) for _ in range(max_perm))


def _series(iterable):
    if iterable is None:
        return None
    if isinstance(iterable, pd.Series):
        return iterable
    if isinstance(iterable, Log):
        return _series(iterable.wrapped).apply(lambda v: log(v) + iterable.shift)
    return pd.Series(iterable)


def _iterable(df, key):
    if key is None:
        return None
    if isinstance(key, Log):
        return Log(_iterable(df, key.wrapped), key.shift)
    return df[key]


def _cortest(x, y, max_perm):
    x = _series(x)
    y = _series(y)
    r, p = pearsonr(x, y)
    if max_perm is not None:
        population = list(y)
        if max_perm == 0:
            resamples = permutations(population)
        else:
            resamples = _permutations(population, max_perm)
        above = 0
        total = 0
        for resample in resamples:
            result, _ = _cortest(x, resample, None)
            if (r < 0 and result <= r) or r == 0 or (r > 0 and result >= r):
                above += 1
            total += 1
        p = 2 * (above / total)
    return r, p


def _chitest(x, y, max_perm):
    x = _series(x)
    y = _series(y)
    observed = pd.crosstab(x, y)
    chi2, p, _, _ = chi2_contingency(observed)
    n = len(x)
    r, k = observed.shape
    phi2 = max(0, chi2 / n - ((k - 1) * (r - 1)) / (n - 1))
    k -= (k - 1)**2 / (n - 1)
    r -= (r - 1)**2 / (n - 1)
    v = sqrt(phi2 / min(k - 1, r - 1))
    if max_perm is not None:
        population = list(y)
        if max_perm == 0:
            resamples = permutations(population)
        else:
            resamples = _permutations(population, max_perm)
        above = 0
        total = 0
        for resample in resamples:
            result, _ = _chitest(x, resample, None)
            if result >= v:
                above += 1
            total += 1
        p = above / total
    return v, p


def _indtest(a, b, max_perm):
    a = _series(a)
    b = _series(b)
    length = len(a)
    if length < 2 or len(b) < 2 or (_varzero(a) and _varzero(b)):
        return None
    t, p = ttest_ind(a, b, equal_var=False)
    if max_perm is not None:
        population = list(a) + list(b)
        if max_perm == 0:
            resamples = permutations(population)
        else:
            resamples = _permutations(population, max_perm)
        above = 0
        total = 0
        for resample in resamples:
            result = _indtest(resample[:length], resample[length:], None)
            if result is None:
                return None
            result = result[0]
            if (t < 0 and result <= t) or t == 0 or (t > 0 and result >= t):
                above += 1
            total += 1
        p = 2 * (above / total)
    return t, p


def _reltest(a, b, max_perm):
    a = _series(a)
    b = _series(b)
    length = len(a)
    if length < 2 or length != len(b) or _varzero(A - B for A, B in zip(a, b)):
        return None
    t, p = ttest_rel(a, b)
    if max_perm is not None:
        population = (False, True)
        if max_perm == 0:
            resamples = product(population, repeat=length)
        else:
            resamples = _product(population, length, max_perm)
        above = 0
        total = 0
        for resample in resamples:
            resample_a = []
            resample_b = []
            for i, keep in enumerate(resample):
                if keep:
                    resample_a.append(a[i])
                    resample_b.append(b[i])
                else:
                    resample_a.append(b[i])
                    resample_b.append(a[i])
            result = _reltest(resample_a, resample_b, None)
            if result is None:
                return None
            result = result[0]
            if (t < 0 and result <= t) or t == 0 or (t > 0 and result >= t):
                above += 1
            total += 1
        p = 2 * (above / total)
    return t, p


def _crosstab(g, nodes, weight):
    try:
        iter(nodes)
    except TypeError:
        raise TypeError('nodes must be iterable')

    nodes = set(nodes)

    if any(n not in g.nodes for n in nodes):
        raise ValueError('nodes must be a subset of the graph nodes')
    if len(nodes) == 0 or len(nodes) == g.number_of_nodes():
        raise ValueError('nodes must be a non-empty proper subset of the graph nodes')

    nodes = [n for n in g.nodes if n in nodes]
    other = [m for m in g.nodes if m not in nodes]

    for n, m in g.edges:
        if (n in nodes and m in nodes) or (n in other and m in other):
            raise ValueError('nodes must define a bipartition')
        if isinstance(g, nx.DiGraph) and (n in other and m in nodes):
            raise ValueError('nodes must define a directed bipartition')

    matrix = []
    for n in nodes:
        line = []
        for m in other:
            if g.has_edge(n, m):
                value = g.edges[n, m].get(weight, 1)
            else:
                value = sys.float_info.epsilon
            line.append(value)
        matrix.append(line)

    return pd.DataFrame(matrix, nodes, other)


def _project(g, ca, observed):
    pos = ca.row_coordinates(observed)
    for n, x, y in zip(observed.index, pos[0], pos[1]):
        g.nodes[n]['pos'] = (x, y)

    pos = ca.column_coordinates(observed)
    for m, x, y in zip(observed.columns, pos[0], pos[1]):
        g.nodes[m]['pos'] = (x, y)


def concat(dataframes, key):
    for value, df in dataframes.items():
        df[key] = value
    return pd.concat(dataframes.values(), ignore_index=True)


def assign(df, other, key):
    index = df.index.intersection(other.index)
    df[key] = other.loc[index][key]


def distest_loose(x):
    x = _series(x)
    data = {
        'Shapiro-Wilk (normal)': shapiro(x),
        'D\'Agostino-Pearson (normal)': normaltest(x),
        'Kolmogorov-Smirnov (normal)': kstest(x, norm.cdf, norm.fit(x)),
        'Kolmogorov-Smirnov (powerlaw)': kstest(x, powerlaw.cdf, powerlaw.fit(x)),
        'Kolmogorov-Smirnov (exponential)': kstest(x, expon.cdf, expon.fit(x)),
    }
    keys = data.keys()
    values = (p for _, p in data.values())
    return pd.DataFrame(values, keys, ['p-value']).round(DEC)


def distest(df, x):
    return distest_loose(_iterable(df, x))


def cortest_loose(x, y, max_perm=None):
    r, p = _cortest(x, y, max_perm)
    return round(r, DEC), round(p, DEC)


def cortest(df, x, y, max_perm=None):
    return cortest_loose(_iterable(df, x), _iterable(df, y), max_perm)


def chitest_loose(x, y, max_perm=None):
    v, p = _chitest(x, y, max_perm)
    return round(v, DEC), round(p, DEC)


def chitest(df, x, y, max_perm=None):
    return chitest_loose(_iterable(df, x), _iterable(df, y), max_perm)


def onetest_loose(a, mean):
    a = _series(a)
    if len(a) < 2 or _varzero(a):
        return None
    _, p = ttest_1samp(a, mean)
    return round(p, DEC)


def onetest(df, a, mean):
    return onetest_loose(_iterable(df, a), mean)


def indtest_loose(a, b, max_perm=None):
    result = _indtest(a, b, max_perm)
    if result is None:
        return None
    return round(result[1], DEC)


def indtest(df, a, b, max_perm=None):
    return indtest_loose(_iterable(df, a), _iterable(df, b), max_perm)


def reltest_loose(a, b, max_perm=None):
    result = _reltest(a, b, max_perm)
    if result is None:
        return None
    return round(result[1], DEC)


def reltest(df, a, b, max_perm=None):
    return reltest_loose(_iterable(df, a), _iterable(df, b), max_perm)


def mixtest_loose(x, y, max_perm=None):
    data = {}
    for X, Y in zip(_series(x), _series(y)):
        if Y not in data:
            data[Y] = []
        data[Y].append(X)
    result = []
    index = []
    for y1, y2 in combinations(data, 2):
        result.append(indtest_loose(data[y1], data[y2], max_perm))
        index.append('{}, {}'.format(y1, y2))
    return pd.DataFrame(result, index, ['p-value'])


def mixtest(df, x, y, max_perm=None):
    return mixtest_loose(_iterable(df, x), _iterable(df, y), max_perm)


def linregress_loose(X, y, *args, **kwargs):
    X = list(zip(*(_series(x) for x in X)))
    y = _series(y)
    model = OLS(y, X)
    result = model.fit(*args, **kwargs)
    return result.summary()


def linregress(df, X, y, *args, **kwargs):
    return linregress_loose((_iterable(df, x) for x in X), _iterable(df, y), *args, **kwargs)


def logregress_loose(X, y, *args, **kwargs):
    X = list(zip(*(_series(x) for x in X)))
    y = _series(y)
    model = Logit(y, X)
    result = model.fit(*args, **kwargs)
    return result.summary()


def logregress(df, X, y, *args, **kwargs):
    return logregress_loose((_iterable(df, x) for x in X), _iterable(df, y), *args, **kwargs)


def intencode_loose(x, order=None):
    x = _series(x)
    values = x.unique()
    if order is None:
        order = tuple(sorted(values))
    else:
        if not isinstance(order, (tuple, list)):
            raise TypeError('order must be a tuple or list')
        if len(order) > len(set(order)):
            raise ValueError('order has repeated values')
        if any(value not in order for value in values):
            raise ValueError('data has values not in order')
    return x.apply(lambda v: order.index(v))


def intencode(df, x, order=None):
    df = df.copy()
    df[x] = intencode_loose(df[x], order)
    return df


def binencode_loose(x):
    x = _series(x)
    values = x.unique()
    return {value: x.apply(lambda v: int(v == value)) for value in values}


def binencode(df, x):
    df = df.copy()
    X = binencode_loose(df[x])
    for value in X:
        df['{}_{}'.format(x, value)] = X[value]
    del df[x]
    return df


def resize_next_plot(width, height):
    plt.figure(figsize=(width / DPI, height / DPI), dpi=DPI)


def resize_all_plots(width, height):
    plt.rcParams['figure.figsize'] = (width / DPI, height / DPI)
    plt.rcParams['figure.dpi'] = DPI


def displot_loose(x):
    sns.distplot(_series(x))


def displot(df, x):
    displot_loose(_iterable(df, x))


def barplot_loose(x, control=None):
    sns.countplot(_series(x), hue=_series(control))


def barplot(df, x, control=None):
    barplot_loose(_iterable(df, x), _iterable(df, control))


def linplot_loose(x, y, control=None):
    sns.lineplot(_series(x), _series(y), _series(control))


def linplot(df, x, y, control=None):
    linplot_loose(_iterable(df, x), _iterable(df, y), _iterable(df, control))


def scaplot_loose(x, y, control=None):
    sns.scatterplot(_series(x), _series(y), _series(control))


def scaplot(df, x, y, control=None):
    scaplot_loose(_iterable(df, x), _iterable(df, y), _iterable(df, control))


def matplot_loose(X, control=None):
    X = [_series(x) for x in (*X, control)]
    for i, x in enumerate(X):
        if x is not None:
            if x.name is None:
                x.name = i
    df = pd.concat(X, 1)
    X = [None if x is None else x.name for x in X]
    sns.pairplot(df, X[-1], vars=X[:-1])


def matplot(df, X, control=None):
    matplot_loose((_iterable(df, x) for x in X), _iterable(df, control))


def valcount_loose(x, order=None, transpose=False):
    x = _series(x)
    df = pd.DataFrame(x.value_counts(True)).round(2)
    df.columns = ['All']
    if order is not None:
        if not isinstance(order, (tuple, list)):
            raise TypeError('order must be a tuple or list')
        if len(order) > len(set(order)):
            raise ValueError('order has repeated values')
        if any(value not in order for value in df.index):
            raise ValueError('data has values not in order')
        df = df.reindex(order).fillna(0)
    if transpose:
        return df.transpose()
    return df


def valcount(df, x, order=None, transpose=False):
    return valcount_loose(_iterable(df, x), order, transpose)


def contable_loose(x, y):
    return pd.crosstab(_series(x), _series(y), margins=True, normalize=True)


def contable(df, x, y):
    return contable_loose(_iterable(df, x), _iterable(df, y))


def corplot_loose(x, y):
    observed = pd.crosstab(_series(x), _series(y))
    ca = CA()
    ca.fit(observed)
    ca.plot_coordinates(observed)


def corplot(df, x, y):
    corplot_loose(_iterable(df, x), _iterable(df, y))


def corplot_twomode(g, nodes, weight='weight'):
    observed = _crosstab(g, nodes, weight)
    ca = CA()
    ca.fit(observed)
    ca.plot_coordinates(observed)


def analyze_to_move(g, nodes, weight='weight'):
    observed = _crosstab(g, nodes, weight)
    ca = CA()
    ca.fit(observed)
    _project(g, ca, observed)


def analyze_last_to_move_all(graphs, nodes, weight='weight'):
    last = graphs[-1]
    observed = _crosstab(last, nodes, weight)
    ca = CA()
    ca.fit(observed)
    _project(last, ca, observed)
    for g in graphs[:-1]:
        if sorted(g.nodes) != sorted(last.nodes):
            raise ValueError('all graphs must have the same nodes')
        observed = _crosstab(g, nodes, weight)
        _project(g, ca, observed)


def boxplot_loose(x, y, control=None):
    sns.boxplot(_series(x), _series(y), _series(control), orient='h')


def boxplot(df, x, y, control=None):
    boxplot_loose(_iterable(df, x), _iterable(df, y), _iterable(df, control))


def girvan_newman(g):
    d = 0.0
    linkage = []
    clusters = []

    for C in reversed(list(nx.community.girvan_newman(g))):
        for c in C:
            if c not in clusters:
                if len(c) > 1:
                    i = 0
                    while clusters[i] is None or not clusters[i].issubset(c):
                        i += 1
                    j = clusters.index(c - clusters[i])
                    d += 1
                    linkage.append([i, j, d, len(c)])
                    clusters[i] = None
                    clusters[j] = None
                clusters.append(c)

    while len(linkage) < g.number_of_nodes() - 1:
        j = len(clusters) - 1
        i = 0
        while clusters[i] is None:
            i += 1
        c = clusters[i] | clusters[j]
        d += 1
        linkage.append([i, j, d, len(c)])
        clusters[i] = None
        clusters[j] = None
        clusters.append(c)

    labels = []
    for n in g.nodes:
        label = get_node_label(g, n)
        if label is None:
            label = n
        labels.append(label)

    dendrogram(linkage, orientation='right', labels=labels)


if sns is not None:
    sns.set()
