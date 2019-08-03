import pandas as pd
import seaborn as sns

from random import sample
from itertools import permutations, combinations
from scipy.stats import pearsonr, chi2_contingency, ttest_ind
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import OneHotEncoder

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


def _permutations(iterable, max_perm):
    for _ in range(max_perm):
        yield sample(iterable, len(iterable))


def _correlation(x, y, max_perm):
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
            result, _ = _correlation(x, pd.Series(resample), None)
            if (r < 0 and result <= r) or r == 0 or (r > 0 and result >= r):
                above += 1
            total += 1
        p = 2 * (above / total)
    return r, p


def _chisquared(x, y, max_perm):
    observed = pd.crosstab(x, y)
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
            result, _ = _chisquared(x, pd.Series(resample), None)
            if result >= c:
                above += 1
            total += 1
        p = above / total
    return c, p


def _student(a, b, max_perm):
    d = abs(a.mean() - b.mean())
    if a.size < 2 or b.size < 2 or a.var() == 0 or b.var() == 0:
        p = None
    else:
        _, p = ttest_ind(a, b)
    if p is not None and max_perm is not None:
        size = a.size
        original = list(pd.concat([a, b]))
        if max_perm == 0:
            resamples = permutations(original)
        else:
            resamples = _permutations(original, max_perm)
        above = 0
        total = 0
        for resample in resamples:
            result, _ = _student(pd.Series(resample[:size]), pd.Series(resample[size:]), None)
            if result >= d:
                above += 1
            total += 1
        p = above / total
    return d, p


def initialize_nodes(g):
    data = {
        'node': list(g.nodes),
    }
    g.nodeframe = pd.DataFrame(data)


def initialize_edges(g):
    data = {
        'source': [n for n, m in g.edges],
        'target': [m for n, m in g.edges],
    }
    g.edgeframe = pd.DataFrame(data)


def save_nodes(g, maps):
    for col, map in maps.items():
        g.nodeframe[col] = list(extract_nodes(g, map))


def save_edges(g, maps):
    for col, map in maps.items():
        g.edgeframe[col] = list(extract_edges(g, map))


def concat(dfs, col):
    for value, df in dfs.items():
        df[col] = value
    return pd.concat(dfs.values())


def concat_nodes(graphs, col):
    return concat({value: g.nodeframe for value, g in graphs.items()}, col)


def concat_edges(graphs, col):
    return concat({value: g.edgeframe for value, g in graphs.items()}, col)


def correlation(df, x, y, max_perm):
    return _correlation(df[x], df[y], max_perm)


def correlation_nodes(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    return correlation(g.nodeframe, x, y, max_perm)


def correlation_edges(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    return correlation(g.edgeframe, x, y, max_perm)


def chisquared(df, x, y, max_perm):
    return _chisquared(df[x], df[y], max_perm)


def chisquared_nodes(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    return chisquared(g.nodeframe, x, y, max_perm)


def chisquared_edges(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    return chisquared(g.edgeframe, x, y, max_perm)


def student(df, a, b, max_perm):
    return _student(df[a], df[b], max_perm)


def student_nodes(g, a, b, amap=None, bmap=None, max_perm=None):
    maps = _filter({
        a: amap,
        b: bmap,
    })
    if maps:
        save_nodes(g, maps)
    return student(g.nodeframe, a, b, max_perm)


def student_edges(g, a, b, amap=None, bmap=None, max_perm=None):
    maps = _filter({
        a: amap,
        b: bmap,
    })
    if maps:
        save_edges(g, maps)
    return student(g.edgeframe, a, b, max_perm)


def pairstudent(df, x, y, max_perm):
    data = {}
    for value in df[x]:
        if value not in data:
            data[value] = df[df[x] == value][y]
    result = {}
    for a, b in combinations(data, 2):
        if data[a].empty or data[b].empty:
            result[a, b] = None
        else:
            result[a, b] = _student(data[a], data[b], max_perm)
    return result


def pairstudent_nodes(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    return pairstudent(g.nodeframe, x, y, max_perm)


def pairstudent_edges(g, x, y, xmap=None, ymap=None, max_perm=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    return pairstudent(g.edgeframe, x, y, max_perm)


def linregress(df, X, y):
    dfX = list(zip(*(df[x] for x in X)))
    model = LinearRegression()
    model.fit(dfX, df[y])
    return [coef for coef in model.coef_], model.score(dfX, df[y])


def linregress_nodes(g, X, y, Xmap=None, ymap=None):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        save_nodes(g, maps)
    return linregress(g.nodeframe, X, y)


def linregress_edges(g, X, y, Xmap=None, ymap=None):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        save_edges(g, maps)
    return linregress(g.edgeframe, X, y)


def logregress(df, X, y, max_iter):
    dfX = list(zip(*(df[x] for x in X)))
    model = LogisticRegression(solver='lbfgs', max_iter=max_iter, multi_class='auto')
    model.fit(dfX, df[y])
    return {class_: [coef for coef in coef_] for class_, coef_ in zip(model.classes_, model.coef_)}, model.score(dfX, df[y])


def logregress_nodes(g, X, y, Xmap=None, ymap=None, max_iter=100):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        save_nodes(g, maps)
    return logregress(g.nodeframe, X, y, max_iter)


def logregress_edges(g, X, y, Xmap=None, ymap=None, max_iter=100):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        save_edges(g, maps)
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
        save_nodes(g, {x: xmap for x, xmap in zip(X, Xmap)})
    return encode(g.nodeframe, X)


def encode_edges(g, X, Xmap=None):
    if Xmap is not None:
        save_edges(g, {x: xmap for x, xmap in zip(X, Xmap)})
    return encode(g.edgeframe, X)


def distplot(df, a):
    sns.distplot(a=df[a])


def distplot_nodes(g, a, amap=None):
    if amap is not None:
        save_nodes(g, {a: amap})
    distplot(g.nodeframe, a)


def distplot_edges(g, a, amap=None):
    if amap is not None:
        save_edges(g, {a: amap})
    distplot(g.edgeframe, a)


def barplot(df, x, control):
    sns.catplot(data=df, x=x, kind='count', hue=control)


def barplot_nodes(g, x, xmap=None, control=None):
    if xmap is not None:
        save_nodes(g, {x: xmap})
    barplot(g.nodeframe, x, control)


def barplot_edges(g, x, xmap=None, control=None):
    if xmap is not None:
        save_edges(g, {x: xmap})
    barplot(g.edgeframe, x, control)


def scatterplot(df, x, y, control):
    sns.scatterplot(data=df, x=x, y=y, hue=control)


def scatterplot_nodes(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    scatterplot(g.nodeframe, x, y, control)


def scatterplot_edges(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    scatterplot(g.edgeframe, x, y, control)


def pairplot(df, vars, control):
    sns.pairplot(data=df, vars=vars, hue=control)


def pairplot_nodes(g, vars, maps=None, control=None):
    if maps is not None:
        save_nodes(g, {col: map for col, map in zip(vars, maps)})
    pairplot(g.nodeframe, vars, control)


def pairplot_edges(g, vars, maps=None, control=None):
    if maps is not None:
        save_edges(g, {col: map for col, map in zip(vars, maps)})
    pairplot(g.edgeframe, vars, control)


def jointplot(df, x, y):
    sns.jointplot(x=df[x], y=df[y], kind='hex')


def jointplot_nodes(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    jointplot(g.nodeframe, x, y)


def jointplot_edges(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    jointplot(g.edgeframe, x, y)


def boxplot(df, x, y, control):
    sns.boxplot(data=df, x=x, y=y, hue=control)


def boxplot_nodes(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    boxplot(g.nodeframe, x, y, control)


def boxplot_edges(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    boxplot(g.edgeframe, x, y, control)
