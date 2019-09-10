import pandas as pd
import seaborn as sns
import networkx as nx

from math import isclose, sqrt, log
from random import choices, sample
from itertools import product, permutations, combinations
from scipy.stats import shapiro, normaltest, kstest, norm, lognorm, powerlaw, expon, pearsonr, chi2_contingency, ttest_1samp, ttest_ind, ttest_rel
from scipy.cluster.hierarchy import dendrogram
from statsmodels.api import OLS, Logit
from sklearn.preprocessing import OneHotEncoder
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


def _product(iterable, size, max_perm):
    for _ in range(max_perm):
        yield choices(iterable, k=size)


def _permutations(iterable, max_perm):
    for _ in range(max_perm):
        yield sample(iterable, len(iterable))


def _cortest(x, y, max_perm):
    r, p = pearsonr(x, y)
    if max_perm is not None:
        original = list(y)
        if max_perm == 0:
            resamples = permutations(original)
        else:
            resamples = _permutations(original, max_perm)
        above = 0
        total = 0
        for resample in resamples:
            result, _ = _cortest(x, pd.Series(resample), None)
            if (r < 0 and result <= r) or r == 0 or (r > 0 and result >= r):
                above += 1
            total += 1
        p = 2 * (above / total)
    return r, round(p, DEC)


def _chitest(x, y, max_perm):
    observed = pd.crosstab(y, x)
    chi2, p, _, _ = chi2_contingency(observed)
    n = observed.sum().sum()
    r, k = observed.shape
    phi2 = chi2 / n
    phi2 = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    k -= (k - 1)**2 / (n - 1)
    r -= (r - 1)**2 / (n - 1)
    v = sqrt(phi2 / min(k - 1, r - 1))
    if max_perm is not None:
        original = list(y)
        if max_perm == 0:
            resamples = permutations(original)
        else:
            resamples = _permutations(original, max_perm)
        above = 0
        total = 0
        for resample in resamples:
            result, _ = _chitest(x, pd.Series(resample), None)
            if result >= v:
                above += 1
            total += 1
        p = above / total
    return v, round(p, DEC)


def _indtest(a, b, max_perm):
    if a.size < 2 or b.size < 2 or (isclose(a.var(), 0) and isclose(b.var(), 0)):
        return None
    t, p = ttest_ind(a, b, equal_var=False)
    if max_perm is not None:
        size = a.size
        original = list(pd.concat([a, b]))
        if max_perm == 0:
            resamples = permutations(original)
        else:
            resamples = _permutations(original, max_perm)
        above = 0
        total = 0
        for resample in resamples:
            result, _ = _indtest(pd.Series(resample[:size]), pd.Series(resample[size:]), None)
            if (t < 0 and result <= t) or t == 0 or (t > 0 and result >= t):
                above += 1
            total += 1
        p = 2 * (above / total)
    return t, round(p, DEC)


def _reltest(a, b, max_perm):
    size = a.size
    if size < 2 or size != b.size or a.equals(b) or (isclose(a.var(), 0) and isclose(b.var(), 0)):
        return None
    t, p = ttest_rel(a, b)
    if max_perm is not None:
        if max_perm == 0:
            resamples = product([False, True], repeat=size)
        else:
            resamples = _product([False, True], size, max_perm)
        above = 0
        total = 0
        for resample in resamples:
            la = []
            lb = []
            for i, keep in enumerate(resample):
                if keep:
                    la.append(a[i])
                    lb.append(b[i])
                else:
                    la.append(b[i])
                    lb.append(a[i])
            result, _ = _reltest(pd.Series(la), pd.Series(lb), None)
            if (t < 0 and result <= t) or t == 0 or (t > 0 and result >= t):
                above += 1
            total += 1
        p = 2 * (above / total)
    return t, round(p, DEC)


def set_nodeframe(g):
    data = {
        'node': list(g.nodes),
    }
    g.nodeframe = pd.DataFrame(data)


def set_edgeframe(g):
    data = {
        'source': [n for n, m in g.edges],
        'target': [m for n, m in g.edges],
    }
    g.edgeframe = pd.DataFrame(data)


def set_nodecol(g, col, map):
    g.nodeframe[col] = list(extract_nodes(g, map))


def set_edgecol(g, col, map):
    g.edgeframe[col] = list(extract_edges(g, map))


def set_nodecols(g, maps):
    for col, map in maps.items():
        set_nodecol(g, col, map)


def set_edgecols(g, maps):
    for col, map in maps.items():
        set_edgecol(g, col, map)


def concat(dfs, col):
    for value, df in dfs.items():
        df[col] = value
    return pd.concat(dfs.values())


def concat_nodeframes(graphs, col):
    return concat({value: g.nodeframe for value, g in graphs.items()}, col)


def concat_edgeframes(graphs, col):
    return concat({value: g.edgeframe for value, g in graphs.items()}, col)


def distest(df, a):
    data = {
        'Shapiro-Wilk (normal)': shapiro(df[a]),
        'D\'Agostino-Pearson (normal)': normaltest(df[a]),
        'Kolmogorov-Smirnov (normal)': kstest(df[a], 'norm', norm.fit(df[a])),
        'Kolmogorov-Smirnov (lognormal)': kstest(df[a], 'lognorm', lognorm.fit(df[a])),
        'Kolmogorov-Smirnov (powerlaw)': kstest(df[a], 'powerlaw', powerlaw.fit(df[a])),
        'Kolmogorov-Smirnov (exponential)': kstest(df[a], 'expon', expon.fit(df[a])),
    }
    keys = data.keys()
    values = [p for _, p in data.values()]
    return pd.DataFrame(values, index=keys, columns=['p-value']).round(DEC)


def distest_nodes(g, a):
    return distest(g.nodeframe, a)


def distest_edges(g, a):
    return distest(g.edgeframe, a)


def cortest(df, x, y, max_perm=None):
    return _cortest(_value(df, x), _value(df, y), max_perm)


def cortest_nodes(g, x, y, max_perm=None):
    return cortest(g.nodeframe, x, y, max_perm)


def cortest_edges(g, x, y, max_perm=None):
    return cortest(g.edgeframe, x, y, max_perm)


def chitest(df, x, y, max_perm=None):
    return _chitest(df[x], df[y], max_perm)


def chitest_nodes(g, x, y, max_perm=None):
    return chitest(g.nodeframe, x, y, max_perm)


def chitest_edges(g, x, y, max_perm=None):
    return chitest(g.edgeframe, x, y, max_perm)


def sintest(a, mean):
    a = pd.Series(a)
    if a.size < 2 or isclose(a.var(), 0):
        return None
    t, p = ttest_1samp(a, mean)
    return t, round(p, DEC)


def indtest(a, b, max_perm=None):
    return _indtest(pd.Series(a), pd.Series(b), max_perm)


def reltest(df, a, b, max_perm=None):
    return _reltest(df[a], df[b], max_perm)


def reltest_nodes(g, a, b, max_perm=None):
    return reltest(g.nodeframe, a, b, max_perm)


def reltest_edges(g, a, b, max_perm=None):
    return reltest(g.edgeframe, a, b, max_perm)


def mixtest(df, x, y, max_perm=None):
    data = {}
    for value in df[y]:
        if value not in data:
            data[value] = df[df[y] == value][x]
    result = {}
    for a, b in combinations(data, 2):
        result[a, b] = _indtest(data[a], data[b], max_perm)
    return result


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
    dfy = _value(df, y)
    model = Logit(dfy, dfX)
    result = model.fit_regularized(*args, **kwargs)
    return result.summary()


def logregress_nodes(g, X, y, *args, **kwargs):
    return logregress(g.nodeframe, X, y, *args, **kwargs)


def logregress_edges(g, X, y, *args, **kwargs):
    return logregress(g.edgeframe, X, y, *args, **kwargs)


def encode(df, X):
    dfX = list(zip(*(df[x] for x in X)))
    encoder = OneHotEncoder(categories='auto', sparse=False)
    X = zip(*encoder.fit_transform(dfX))
    cols = list(encoder.get_feature_names())
    for col, x in zip(cols, X):
        df[col] = x
    return cols


def encode_nodes(g, X):
    return encode(g.nodeframe, X)


def encode_edges(g, X):
    return encode(g.edgeframe, X)


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

    labels = [g.nodes[n]['label'] if 'label' in g.nodes[n] else str(n) for n in g.nodes]

    dendrogram(linkage, orientation='right', labels=labels)


def corplot_graph(g, nodes):
    other = [m for m in g.nodes if m not in nodes and g.degree(m) > 0]
    nodes = [n for n in nodes if g.degree(n) > 0]

    data = {}
    for m in other:
        data[m] = [1 if g.has_edge(n, m) else 0 for n in nodes]
    df = pd.DataFrame(data)

    ca = CA()
    ca.fit(df)
    ca.plot_coordinates(df)

    h = g.subgraph(nodes + other).copy()

    pos = ca.row_coordinates(df)
    for n, x, y in zip(nodes, pos[0], pos[1]):
        h.nodes[n]['pos'] = (x, y)
        h.nodes[n]['color'] = (76, 116, 172)

    pos = ca.column_coordinates(df)
    for m, x, y in zip(other, pos[0], pos[1]):
        h.nodes[m]['pos'] = (x, y)
        h.nodes[m]['color'] = (219, 130, 87)

    normalize(h)

    return h


sns.set()
