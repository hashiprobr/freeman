import pandas as pd
import seaborn as sns

from math import isclose
from random import choices, sample
from itertools import product, permutations, combinations
from scipy.stats import pearsonr, chi2_contingency, ttest_1samp, ttest_ind, ttest_rel
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from prince import CA

from .exploring import extract_nodes, extract_edges


def _merge(X, y, Xmap, ymap):
    if Xmap is None:
        maps = {}
    else:
        maps = {x: xmap for x, xmap in zip(X, Xmap)}
    maps[y] = ymap
    return maps


def _filter(maps):
    cols = list(maps.keys())
    for col in cols:
        if maps[col] is None:
            del maps[col]
    return maps


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


def cortest(df, x, y, max_perm=None):
    return _cortest(df[x], df[y], max_perm)


def cortest_nodes(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_nodecols(g, maps)
    return cortest(g.nodeframe, x, y, max_perm)


def cortest_edges(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_edgecols(g, maps)
    return cortest(g.edgeframe, x, y, max_perm)


def chitest(df, x, y, max_perm=None):
    return _chitest(df[x], df[y], max_perm)


def chitest_nodes(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_nodecols(g, maps)
    return chitest(g.nodeframe, x, y, max_perm)


def chitest_edges(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_edgecols(g, maps)
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


def reltest_nodes(g, a, b, amap=None, bmap=None, max_perm=None):
    maps = _filter({
        a: amap,
        b: bmap,
    })
    if maps:
        set_nodecols(g, maps)
    return reltest(g.nodeframe, a, b, max_perm)


def reltest_edges(g, a, b, amap=None, bmap=None, max_perm=None):
    maps = _filter({
        a: amap,
        b: bmap,
    })
    if maps:
        set_edgecols(g, maps)
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


def mixtest_nodes(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_nodecols(g, maps)
    return mixtest(g.nodeframe, x, y, max_perm)


def mixtest_edges(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_edgecols(g, maps)
    return mixtest(g.edgeframe, x, y, max_perm)


def linregress(df, X, y):
    dfX = list(zip(*(df[x] for x in X)))
    model = LinearRegression()
    model.fit(dfX, df[y])
    return [coef for coef in model.coef_], model.score(dfX, df[y])


def linregress_nodes(g, X, y, Xmap=None, ymap=None):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        set_nodecols(g, maps)
    return linregress(g.nodeframe, X, y)


def linregress_edges(g, X, y, Xmap=None, ymap=None):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        set_edgecols(g, maps)
    return linregress(g.edgeframe, X, y)


def logregress(df, X, y, max_iter=100):
    dfX = list(zip(*(df[x] for x in X)))
    model = LogisticRegression(solver='lbfgs', max_iter=max_iter, multi_class='auto')
    model.fit(dfX, df[y])
    return {class_: [coef for coef in coef_] for class_, coef_ in zip(model.classes_, model.coef_)}, model.score(dfX, df[y])


def logregress_nodes(g, X, y, Xmap=None, ymap=None, max_iter=100):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        set_nodecols(g, maps)
    return logregress(g.nodeframe, X, y, max_iter)


def logregress_edges(g, X, y, Xmap=None, ymap=None, max_iter=100):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        set_edgecols(g, maps)
    return logregress(g.edgeframe, X, y, max_iter)


def encode(df, X):
    dfX = list(zip(*(df[x] for x in X)))
    encoder = OneHotEncoder(categories='auto', sparse=False)
    X = zip(*encoder.fit_transform(dfX))
    cols = encoder.get_feature_names()
    for col, x in zip(cols, X):
        df[col] = x
    return cols


def encode_nodes(g, X, Xmap=None):
    if Xmap is not None:
        set_nodecols(g, {x: xmap for x, xmap in zip(X, Xmap)})
    return encode(g.nodeframe, X)


def encode_edges(g, X, Xmap=None):
    if Xmap is not None:
        set_edgecols(g, {x: xmap for x, xmap in zip(X, Xmap)})
    return encode(g.edgeframe, X)


def displot(df, x):
    sns.distplot(a=df[x])


def displot_nodes(g, x, xmap=None):
    if xmap is not None:
        set_nodecol(g, x, xmap)
    displot(g.nodeframe, x)


def displot_edges(g, x, xmap=None):
    if xmap is not None:
        set_edgecol(g, x, xmap)
    displot(g.edgeframe, x)


def barplot(df, x, control=None):
    sns.catplot(data=df, x=x, kind='count', hue=control)


def barplot_nodes(g, x, xmap=None, control=None):
    if xmap is not None:
        set_nodecol(g, x, xmap)
    barplot(g.nodeframe, x, control)


def barplot_edges(g, x, xmap=None, control=None):
    if xmap is not None:
        set_edgecol(g, x, xmap)
    barplot(g.edgeframe, x, control)


def scaplot(df, x, y, control=None):
    sns.scatterplot(data=df, x=x, y=y, hue=control)


def scaplot_nodes(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_nodecols(g, maps)
    scaplot(g.nodeframe, x, y, control)


def scaplot_edges(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_edgecols(g, maps)
    scaplot(g.edgeframe, x, y, control)


def matplot(df, cols, control=None):
    sns.pairplot(data=df, vars=cols, hue=control)


def matplot_nodes(g, cols, maps=None, control=None):
    if maps is not None:
        set_nodecols(g, {col: map for col, map in zip(cols, maps)})
    matplot(g.nodeframe, cols, control)


def matplot_edges(g, cols, maps=None, control=None):
    if maps is not None:
        set_edgecols(g, {col: map for col, map in zip(cols, maps)})
    matplot(g.edgeframe, cols, control)


def contable(df, x, y):
    return pd.crosstab(df[y], df[x], margins=True)


def contable_nodes(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_nodecols(g, maps)
    return contable(g.nodeframe, x, y)


def contable_edges(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_edgecols(g, maps)
    return contable(g.edgeframe, x, y)


def corplot(df, x, y):
    observed = pd.crosstab(df[y], df[x])
    ca = CA()
    ca.fit(observed)
    ca.plot_coordinates(observed)


def corplot_nodes(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_nodecols(g, maps)
    corplot(g.nodeframe, x, y)


def corplot_edges(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_edgecols(g, maps)
    corplot(g.edgeframe, x, y)


def boxplot(df, x, y, control=None):
    sns.boxplot(data=df, x=x, y=y, orient='h', hue=control)


def boxplot_nodes(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_nodecols(g, maps)
    boxplot(g.nodeframe, x, y, control)


def boxplot_edges(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        set_edgecols(g, maps)
    boxplot(g.edgeframe, x, y, control)
