import pandas as pd
import seaborn as sns
import networkx as nx

from math import isclose, sqrt, log
from statistics import variance
from random import choices, sample
from itertools import chain, product, permutations, combinations
from scipy.stats import shapiro, normaltest, kstest, norm, powerlaw, expon, pearsonr, chi2_contingency, ttest_1samp, ttest_ind, ttest_rel
from scipy.cluster.hierarchy import dendrogram
from statsmodels.api import OLS, Logit
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from prince import CA

from matplotlib import pyplot as plt

from .exploring import extract_nodes, extract_edges, Log
from .moving import normalize


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


def _iterable(df, col):
    if col is None:
        return None
    if isinstance(col, Log):
        return Log(df[col.wrapped], col.shift)
    return df[col]


def _nf(g, col):
    return _iterable(g.nodeframe, col)


def _ef(g, col):
    return _iterable(g.edgeframe, col)


def _cortest(x, y, max_perm):
    x = _series(x)
    y = _series(y)
    r, p = pearsonr(x, y)
    if max_perm is not None:
        population = tuple(y)
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
    n = observed.sum().sum()
    r, k = observed.shape
    phi2 = max(0, chi2 / n - ((k - 1) * (r - 1)) / (n - 1))
    k -= (k - 1)**2 / (n - 1)
    r -= (r - 1)**2 / (n - 1)
    v = sqrt(phi2 / min(k - 1, r - 1))
    if max_perm is not None:
        population = tuple(y)
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
        population = tuple(a) + tuple(b)
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


def set_nodeframe(g):
    data = {
        'id': g.nodes,
    }
    g.nodeframe = pd.DataFrame(data)


def set_edgeframe(g):
    data = {
        'source': (n for n, m in g.edges),
        'target': (m for n, m in g.edges),
    }
    g.edgeframe = pd.DataFrame(data)


def set_nodecol(g, col, map):
    g.nodeframe[col] = tuple(extract_nodes(g, map))


def set_edgecol(g, col, map):
    g.edgeframe[col] = tuple(extract_edges(g, map))


def concat(dfs, col):
    for key, df in dfs.items():
        df[col] = key
    return pd.concat(dfs.values())


def concat_nodes(graphs, col):
    return concat({key: g.nodeframe for key, g in graphs.items()}, col)


def concat_edges(graphs, col):
    return concat({key: g.edgeframe for key, g in graphs.items()}, col)


def distest(a):
    a = _series(a)
    data = {
        'Shapiro-Wilk (normal)': shapiro(a),
        'D\'Agostino-Pearson (normal)': normaltest(a),
        'Kolmogorov-Smirnov (normal)': kstest(a, 'norm', norm.fit(a)),
        'Kolmogorov-Smirnov (powerlaw)': kstest(a, 'powerlaw', powerlaw.fit(a)),
        'Kolmogorov-Smirnov (exponential)': kstest(a, 'expon', expon.fit(a)),
    }
    keys = data.keys()
    values = (p for _, p in data.values())
    return pd.DataFrame(values, keys, ['p-value']).round(DEC)


def distest_nodes(g, a):
    return distest(_nf(g, a))


def distest_edges(g, a):
    return distest(_ef(g, a))


def cortest(x, y, max_perm=None):
    r, p = _cortest(x, y, max_perm)
    return round(r, DEC), round(p, DEC)


def cortest_nodes(g, x, y, max_perm=None):
    return cortest(_nf(g, x), _nf(g, y), max_perm)


def cortest_edges(g, x, y, max_perm=None):
    return cortest(_ef(g, x), _ef(g, y), max_perm)


def chitest(x, y, max_perm=None):
    v, p = _chitest(x, y, max_perm)
    return round(v, DEC), round(p, DEC)


def chitest_nodes(g, x, y, max_perm=None):
    return chitest(_nf(g, x), _nf(g, y), max_perm)


def chitest_edges(g, x, y, max_perm=None):
    return chitest(_ef(g, x), _ef(g, y), max_perm)


def sintest(a, mean):
    a = _series(a)
    if len(a) < 2 or _varzero(a):
        return None
    _, p = ttest_1samp(a, mean)
    return round(p, DEC)


def indtest(a, b, max_perm=None):
    result = _indtest(a, b, max_perm)
    if result is not None:
        result = round(result[1], DEC)
    return result


def reltest(a, b, max_perm=None):
    result = _reltest(a, b, max_perm)
    if result is not None:
        result = round(result[1], DEC)
    return result


def reltest_nodes(g, a, b, max_perm=None):
    return reltest(_nf(g, a), _nf(g, b), max_perm)


def reltest_edges(g, a, b, max_perm=None):
    return reltest(_ef(g, a), _ef(g, b), max_perm)


def mixtest(x, y, max_perm=None):
    data = {}
    for X, Y in zip(x, y):
        if Y not in data:
            data[Y] = []
        data[Y].append(X)
    result = {}
    for y1, y2 in combinations(data, 2):
        result[y1, y2] = indtest(data[y1], data[y2], max_perm)
    return result


def mixtest_nodes(g, x, y, max_perm=None):
    return mixtest(_nf(g, x), _nf(g, y), max_perm)


def mixtest_edges(g, x, y, max_perm=None):
    return mixtest(_ef(g, x), _ef(g, y), max_perm)


def linregress(X, y, *args, **kwargs):
    X = (_series(x) for x in X)
    y = _series(y)
    model = OLS(y, X)
    result = model.fit(*args, **kwargs)
    return result.summary()


def linregress_nodes(g, X, y, *args, **kwargs):
    return linregress((_nf(g, x) for x in X), _nf(g, y), *args, **kwargs)


def linregress_edges(g, X, y, *args, **kwargs):
    return linregress((_ef(g, x) for x in X), _ef(g, y), *args, **kwargs)


def logregress(X, y, *args, **kwargs):
    X = (_series(x) for x in X)
    y = _series(y)
    model = Logit(y, X)
    result = model.fit(*args, **kwargs)
    return result.summary()


def logregress_nodes(g, X, y, *args, **kwargs):
    return logregress((_nf(g, x) for x in X), _nf(g, y), *args, **kwargs)


def logregress_edges(g, X, y, *args, **kwargs):
    return logregress((_ef(g, x) for x in X), _ef(g, y), *args, **kwargs)


def intencode(df, col, order=None):
    A = tuple(zip(df[col]))
    encoder = OrdinalEncoder('auto' if order is None else [order])
    A = zip(*encoder.fit_transform(A))
    col += '_order'
    df[col] = next(A)
    return col


def intencode_nodes(g, col, order=None):
    return intencode(g.nodeframe, col, order)


def intencode_edges(g, x, order=None):
    return intencode(g.edgeframe, col, order)


def binencode(df, col):
    A = tuple(zip(df[col]))
    encoder = OneHotEncoder(categories='auto', sparse=False)
    A = zip(*encoder.fit_transform(A))
    cols = encoder.get_feature_names([col])
    for a, col in zip(A, cols):
        df[col] = a
    return tuple(cols)


def binencode_nodes(g, col):
    return binencode(g.nodeframe, col)


def binencode_edges(g, col):
    return binencode(g.edgeframe, col)


def resize_next_plot(width, height):
    plt.figure(figsize=(width / DPI, height / DPI), dpi=DPI)


def resize_all_plots(width, height):
    plt.rcParams['figure.figsize'] = (width / DPI, height / DPI)
    plt.rcParams['figure.dpi'] = DPI


def displot(a):
    sns.distplot(_series(a))


def displot_nodes(g, a):
    displot(_nf(g, a))


def displot_edges(g, a):
    displot(_ef(g, a))


def barplot(a, control=None):
    sns.countplot(x=_series(a), hue=_series(control))


def barplot_nodes(g, a, control=None):
    barplot(_nf(g, a), _nf(g, control))


def barplot_edges(g, a, control=None):
    barplot(_ef(g, a), _ef(g, control))


def linplot(x, y, control=None):
    sns.lineplot(x=_series(x), y=_series(y), hue=_series(control))


def linplot_nodes(g, x, y, control=None):
    linplot(_nf(g, x), _nf(g, y), _nf(g, control))


def linplot_edges(g, x, y, control=None):
    linplot(_ef(g, x), _ef(g, y), _ef(g, control))


def scaplot(x, y, control=None):
    sns.scatterplot(x=_series(x), y=_series(y), hue=_series(control))


def scaplot_nodes(g, x, y, control=None):
    scaplot(_nf(g, x), _nf(g, y), _nf(g, control))


def scaplot_edges(g, x, y, control=None):
    scaplot(_ef(g, x), _ef(g, y), _ef(g, control))


def matplot(cols, control=None):
    cols = tuple(_series(col) for col in (*cols, control))
    for i, col in enumerate(cols):
        if col is not None:
            if col.name is None:
                col.name = i
    df = pd.concat(cols, axis=1)
    cols = tuple(None if col is None else col.name for col in cols)
    sns.pairplot(df, cols[-1], vars=cols[:-1])


def matplot_nodes(g, cols, control=None):
    matplot((_nf(g, col) for col in cols), _nf(g, control))


def matplot_edges(g, cols, control=None):
    matplot((_ef(g, col) for col in cols), _ef(g, control))


def valcount(a, order=None, transpose=False):
    a = _series(a)
    data = pd.DataFrame(a.value_counts(True))
    data = data.round(2)
    if order is not None:
        data = data.reindex(order)
    data.columns = ['All']
    if transpose:
        return data.transpose()
    return data


def valcount_nodes(g, a, order=None, transpose=False):
    return valcount(_nf(g, a), order, transpose)


def valcount_edges(g, a, order=None, transpose=False):
    return valcount(_ef(g, a), order, transpose)


def contable(x, y):
    return pd.crosstab(_series(x), _series(y), margins=True, normalize=True)


def contable_nodes(g, x, y):
    return contable(_nf(g, x), _nf(g, y))


def contable_edges(g, x, y):
    return contable(_ef(g, x), _ef(g, y))


def corplot(x, y):
    observed = pd.crosstab(_series(x), _series(y))
    ca = CA()
    ca.fit(observed)
    ca.plot_coordinates(observed)


def corplot_nodes(g, x, y):
    corplot(_nf(g, x), _nf(g, y))


def corplot_edges(g, x, y):
    corplot(_ef(g, x), _ef(g, y))


def boxplot(x, y, control=None):
    cols = tuple(_series(col) for col in (x, y, control))
    for name, col in zip(('x', 'y', 'control'), cols):
        if col is not None:
            if col.name is None:
                col.name = name
    df = pd.concat(cols, axis=1)
    cols = tuple(None if col is None else col.name for col in cols)
    sns.boxplot(x=cols[0], y=cols[1], hue=cols[2], data=df, orient='h')


def boxplot_nodes(g, x, y, control=None):
    boxplot(_nf(g, x), _nf(g, y), _nf(g, control))


def boxplot_edges(g, x, y, control=None):
    boxplot(_ef(g, x), _ef(g, y), _ef(g, control))


def girvan_newman(g):
    d = 0.0
    linkage = []
    clusters = []

    for C in reversed(tuple(nx.community.girvan_newman(g))):
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

    labels = tuple(g.nodes[n].get('label', str(n)) for n in g.nodes)

    dendrogram(linkage, orientation='right', labels=labels)


def corplot_graph(g, nodes, weight='weight', plot=True):
    other = tuple(m for m in g.nodes if m not in nodes and g.degree(m) > 0)
    nodes = tuple(n for n in nodes if g.degree(n) > 0)

    data = (tuple(g.edges[n, m].get(weight, 1) if g.has_edge(n, m) else 0 for m in other) for n in nodes)
    observed = pd.DataFrame(data, nodes, other)
    ca = CA()
    ca.fit(observed)

    if plot:
        ca.plot_coordinates(observed)

    h = g.subgraph(nodes + other).copy()

    pos = ca.row_coordinates(observed)
    for n, x, y in zip(nodes, pos[0], pos[1]):
        h.nodes[n]['pos'] = (x, y)
        h.nodes[n]['color'] = (76, 116, 172)

    pos = ca.column_coordinates(observed)
    for m, x, y in zip(other, pos[0], pos[1]):
        h.nodes[m]['pos'] = (x, y)
        h.nodes[m]['color'] = (219, 130, 87)

    normalize(h)

    return h


sns.set()
