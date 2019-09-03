import pandas as pd
import seaborn as sns

from math import isclose, log
from random import choices, sample
from itertools import product, permutations, combinations
from scipy.stats import shapiro, normaltest, pearsonr, chi2_contingency, ttest_1samp, ttest_ind, ttest_rel
from statsmodels.api import OLS, Logit
from sklearn.preprocessing import OneHotEncoder
from prince import CA

from .exploring import extract_nodes, extract_edges, Log


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
    return r, p


def _chitest(x, y, max_perm):
    observed = pd.crosstab(y, x)
    c, p, _, _ = chi2_contingency(observed)
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
            if result >= c:
                above += 1
            total += 1
        p = above / total
    return c, p


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
    return t, p


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
    return t, p


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


def nortest(df, a):
    _, sw = shapiro(df[a])
    _, ap = normaltest(df[a])
    index = ['Shapiro-Wilk', 'D\'Agostino-Pearson']
    columns = ['p-value']
    return pd.DataFrame([ap, sw], index=index, columns=columns)


def nortest_nodes(g, a):
    return nortest(g.nodeframe, a)


def nortest_edges(g, a):
    return nortest(g.edgeframe, a)


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
    return t, p


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


def linregress(df, X, y):
    dfX = _items(df, X)
    dfy = _value(df, y)
    model = OLS(dfy, dfX)
    result = model.fit()
    return result.summary()


def linregress_nodes(g, X, y):
    return linregress(g.nodeframe, X, y)


def linregress_edges(g, X, y):
    return linregress(g.edgeframe, X, y)


def logregress(df, X, y):
    dfX = _items(df, X)
    dfy = _value(df, y)
    model = Logit(dfy, dfX)
    result = model.fit_regularized()
    return result.summary()


def logregress_nodes(g, X, y):
    return logregress(g.nodeframe, X, y)


def logregress_edges(g, X, y):
    return logregress(g.edgeframe, X, y)


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


def valcount(df, x):
    return df[x].value_counts(normalize=True)


def valcount_nodes(g, x):
    return valcount(g.nodeframe, x)


def valcount_edges(g, x):
    return valcount(g.edgeframe, x)


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


sns.set()
