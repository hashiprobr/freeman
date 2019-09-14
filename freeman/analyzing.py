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


def _log(df, col):
    return df[col.wrapped].apply(lambda x: log(x) + col.shift)


def _value(df, col):
    if isinstance(col, Log):
        return _log(df, col)
    return df[col]


def _items(df, cols):
    data = pd.DataFrame()
    for col in cols:
        if col is not None:
            if isinstance(col, Log):
                data[col.wrapped] = _log(df, col)
            else:
                data[col] = df[col]
    return data


def _varzero(a):
    return isclose(variance(a), 0)


def _product(iterable, size, max_perm):
    for _ in range(max_perm):
        yield choices(iterable, k=size)


def _permutations(iterable, max_perm):
    if hasattr(iterable, '__len__'):
        population = iterable
    else:
        population = list(iterable)
    for _ in range(max_perm):
        yield sample(population, len(population))


def _cortest(x, y, max_perm):
    r, p = pearsonr(x, y)
    if max_perm is not None:
        if max_perm == 0:
            resamples = permutations(y)
        else:
            resamples = _permutations(y, max_perm)
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
    observed = pd.crosstab(pd.Series(x), pd.Series(y))
    chi2, p, _, _ = chi2_contingency(observed)
    n = observed.sum().sum()
    r, k = observed.shape
    phi2 = max(0, chi2 / n - ((k - 1) * (r - 1)) / (n - 1))
    k -= (k - 1)**2 / (n - 1)
    r -= (r - 1)**2 / (n - 1)
    v = sqrt(phi2 / min(k - 1, r - 1))
    if max_perm is not None:
        if max_perm == 0:
            resamples = permutations(y)
        else:
            resamples = _permutations(y, max_perm)
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
    length = len(a)
    if length < 2 or len(b) < 2 or (_varzero(a) and _varzero(b)):
        return None
    t, p = ttest_ind(a, b, equal_var=False)
    if max_perm is not None:
        if max_perm == 0:
            resamples = permutations(chain(a, b))
        else:
            resamples = _permutations(chain(a, b), max_perm)
        above = 0
        total = 0
        for resample in resamples:
            result, _ = _indtest(resample[:length], resample[length:], None)
            if (t < 0 and result <= t) or t == 0 or (t > 0 and result >= t):
                above += 1
            total += 1
        p = 2 * (above / total)
    return t, p


def _reltest(a, b, max_perm):
    length = len(a)
    if length < 2 or length != len(b) or a == b or (_varzero(a) and _varzero(b)):
        return None
    t, p = ttest_rel(a, b)
    if max_perm is not None:
        if max_perm == 0:
            resamples = product([False, True], repeat=length)
        else:
            resamples = _product([False, True], length, max_perm)
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
            result, _ = _reltest(resample_a, resample_b, None)
            if (t < 0 and result <= t) or t == 0 or (t > 0 and result >= t):
                above += 1
            total += 1
        p = 2 * (above / total)
    return t, p


def set_nodeframe(g):
    g.nodeframe = pd.DataFrame()
    g.nodeframe['id'] = [n for n in g.nodes]


def set_edgeframe(g):
    g.edgeframe = pd.DataFrame()
    g.edgeframe['source'] = [n for n, m in g.edges]
    g.edgeframe['target'] = [m for n, m in g.edges]


def set_nodecol(g, col, map):
    g.nodeframe[col] = list(extract_nodes(g, map))


def set_edgecol(g, col, map):
    g.edgeframe[col] = list(extract_edges(g, map))


def concat(dfs, col):
    for key, df in dfs.items():
        df[col] = key
    return pd.concat(dfs.values())


def concat_nodeframes(graphs, col):
    return concat({key: g.nodeframe for key, g in graphs.items()}, col)


def concat_edgeframes(graphs, col):
    return concat({key: g.edgeframe for key, g in graphs.items()}, col)


def distest(df, a):
    data = {
        'Shapiro-Wilk (normal)': shapiro(df[a]),
        'D\'Agostino-Pearson (normal)': normaltest(df[a]),
        'Kolmogorov-Smirnov (normal)': kstest(df[a], 'norm', norm.fit(df[a])),
        'Kolmogorov-Smirnov (powerlaw)': kstest(df[a], 'powerlaw', powerlaw.fit(df[a])),
        'Kolmogorov-Smirnov (exponential)': kstest(df[a], 'expon', expon.fit(df[a])),
    }
    keys = data.keys()
    values = (p for _, p in data.values())
    return pd.DataFrame(values, index=keys, columns=['p-value']).round(DEC)


def distest_nodes(g, a):
    return distest(g.nodeframe, a)


def distest_edges(g, a):
    return distest(g.edgeframe, a)


def cortest(df, x, y, max_perm=None):
    r, p = _cortest(_value(df, x), _value(df, y), max_perm)
    return round(r, DEC), round(p, DEC)


def cortest_nodes(g, x, y, max_perm=None):
    return cortest(g.nodeframe, x, y, max_perm)


def cortest_edges(g, x, y, max_perm=None):
    return cortest(g.edgeframe, x, y, max_perm)


def chitest(df, x, y, max_perm=None):
    v, p = _chitest(df[x], df[y], max_perm)
    return round(v, DEC), round(p, DEC)


def chitest_nodes(g, x, y, max_perm=None):
    return chitest(g.nodeframe, x, y, max_perm)


def chitest_edges(g, x, y, max_perm=None):
    return chitest(g.edgeframe, x, y, max_perm)


def sintest(a, mean):
    if len(a) < 2 or _varzero(a):
        return None
    result = ttest_1samp(a, mean)
    return round(result[1], DEC)


def indtest(a, b, max_perm=None):
    result = _indtest(a, b, max_perm)
    if result is not None:
        result = round(result[1], DEC)
    return result


def reltest(df, a, b, max_perm=None):
    result = _reltest(df[a], df[b], max_perm)
    if result is not None:
        result = round(result[1], DEC)
    return result


def reltest_nodes(g, a, b, max_perm=None):
    return reltest(g.nodeframe, a, b, max_perm)


def reltest_edges(g, a, b, max_perm=None):
    return reltest(g.edgeframe, a, b, max_perm)


def mixtest(df, x, y, max_perm=None):
    data = {}
    for value in df[y]:
        if value not in data:
            data[value] = df[df[y] == value][x]
    results = {}
    for a, b in combinations(data, 2):
        result = _indtest(data[a], data[b], max_perm)
        if result is not None:
            result = round(result[1], DEC)
        results[a, b] = result
    return results


def mixtest_nodes(g, x, y, max_perm=None):
    return mixtest(g.nodeframe, x, y, max_perm)


def mixtest_edges(g, x, y, max_perm=None):
    return mixtest(g.edgeframe, x, y, max_perm)


def linregress(df, X, y, *args, **kwargs):
    dfX = _items(df, X)
    dfy = _value(df, y)
    model = OLS(dfy, dfX)
    result = model.fit(*args, **kwargs)
    return result.summary()


def linregress_nodes(g, X, y, *args, **kwargs):
    return linregress(g.nodeframe, X, y, *args, **kwargs)


def linregress_edges(g, X, y, *args, **kwargs):
    return linregress(g.edgeframe, X, y, *args, **kwargs)


def logregress(df, X, y, *args, **kwargs):
    dfX = _items(df, X)
    dfy = df[y]
    model = Logit(dfy, dfX)
    result = model.fit(*args, **kwargs)
    return result.summary()


def logregress_nodes(g, X, y, *args, **kwargs):
    return logregress(g.nodeframe, X, y, *args, **kwargs)


def logregress_edges(g, X, y, *args, **kwargs):
    return logregress(g.edgeframe, X, y, *args, **kwargs)


def intencode(df, x, order=None):
    dfX = list(zip(df[x]))
    encoder = OrdinalEncoder(categories='auto' if order is None else [order])
    X = zip(*encoder.fit_transform(dfX))
    col = x + '_order'
    df[col] = next(X)
    return col


def intencode_nodes(g, x, order=None):
    return intencode(g.nodeframe, x, order)


def intencode_edges(g, x, order=None):
    return intencode(g.edgeframe, x, order)


def binencode(df, x):
    dfX = list(zip(df[x]))
    encoder = OneHotEncoder(categories='auto', sparse=False)
    X = zip(*encoder.fit_transform(dfX))
    cols = ('{}_{}'.format(x, value) for value in encoder.categories_[0])
    for x, col in zip(X, cols):
        df[col] = x
    return cols


def binencode_nodes(g, x):
    return binencode(g.nodeframe, x)


def binencode_edges(g, x):
    return binencode(g.edgeframe, x)


def resize_next_plot(width, height):
    plt.figure(figsize=(width / DPI, height / DPI), dpi=DPI)


def resize_all_plots(width, height):
    plt.rcParams['figure.figsize'] = (width / DPI, height / DPI)
    plt.rcParams['figure.dpi'] = DPI


def displot(df, x):
    sns.distplot(a=df[x])


def displot_nodes(g, x):
    displot(g.nodeframe, x)


def displot_edges(g, x):
    displot(g.edgeframe, x)


def barplot(df, x, control=None):
    sns.catplot(data=df, x=x, kind='count', hue=control)


def barplot_nodes(g, x, control=None):
    barplot(g.nodeframe, x, control)


def barplot_edges(g, x, control=None):
    barplot(g.edgeframe, x, control)


def linplot(df, x, y, control=None):
    data = _items(df, [x, y, control])
    sns.lineplot(data=data, x=data.columns[0], y=data.columns[1], hue=control)


def linplot_nodes(g, x, y, control=None):
    linplot(g.nodeframe, x, y, control)


def linplot_edges(g, x, y, control=None):
    linplot(g.edgeframe, x, y, control)


def scaplot(df, x, y, control=None):
    data = _items(df, [x, y, control])
    sns.scatterplot(data=data, x=data.columns[0], y=data.columns[1], hue=control)


def scaplot_nodes(g, x, y, control=None):
    scaplot(g.nodeframe, x, y, control)


def scaplot_edges(g, x, y, control=None):
    scaplot(g.edgeframe, x, y, control)


def matplot(df, cols, control=None):
    sns.pairplot(data=_items(df, [*cols, control]), vars=cols, hue=control)


def matplot_nodes(g, cols, control=None):
    matplot(g.nodeframe, cols, control)


def matplot_edges(g, cols, control=None):
    matplot(g.edgeframe, cols, control)


def hexplot(df, x, y):
    sns.jointplot(_value(df, x), _value(df, y), data=df, kind='hex')


def hexplot_nodes(g, x, y):
    hexplot(g.nodeframe, x, y)


def hexplot_edges(g, x, y):
    hexplot(g.edgeframe, x, y)


def valcount(df, x, order=None, transpose=False):
    data = pd.DataFrame(df[x].value_counts(normalize=True))
    data = data.round(2)
    if order is not None:
        data = data.reindex(order)
    data.columns = ['All']
    if transpose:
        return data.transpose()
    return data


def valcount_nodes(g, x, order=None, transpose=False):
    return valcount(g.nodeframe, x, order, transpose)


def valcount_edges(g, x, order=None, transpose=False):
    return valcount(g.edgeframe, x, order, transpose)


def contable(df, x, y):
    return pd.crosstab(df[x], df[y], margins=True, normalize=True)


def contable_nodes(g, x, y):
    return contable(g.nodeframe, x, y)


def contable_edges(g, x, y):
    return contable(g.edgeframe, x, y)


def corplot(df, x, y):
    observed = pd.crosstab(df[y], df[x])
    ca = CA()
    ca.fit(observed)
    ca.plot_coordinates(observed)


def corplot_nodes(g, x, y):
    corplot(g.nodeframe, x, y)


def corplot_edges(g, x, y):
    corplot(g.edgeframe, x, y)


def boxplot(df, x, y, control=None):
    sns.boxplot(data=df, x=x, y=y, orient='h', hue=control)


def boxplot_nodes(g, x, y, control=None):
    boxplot(g.nodeframe, x, y, control)


def boxplot_edges(g, x, y, control=None):
    boxplot(g.edgeframe, x, y, control)


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

    labels = (g.nodes[n].get('label', str(n)) for n in g.nodes)

    dendrogram(linkage, orientation='right', labels=labels)


def corplot_graph(g, nodes, weight='weight', plot=True):
    other = [m for m in g.nodes if m not in nodes and g.degree(m) > 0]
    nodes = [n for n in nodes if g.degree(n) > 0]

    observed = pd.DataFrame([g.edges[n, m].get(weight, 1) if g.has_edge(n, m) else 0 for n in nodes] for m in other)

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
