import pandas as pd
import seaborn as sns

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


def _initialize_nodes(g):
    data = {
        'node': list(g.nodes),
    }
    g.graph['nodeframe'] = pd.DataFrame(data)


def _initialize_edges(g):
    data = {
        'source': [n for n, m in g.edges],
        'target': [m for n, m in g.edges],
    }
    g.graph['edgeframe'] = pd.DataFrame(data)


def save_nodes(g, maps):
    if 'nodeframe' not in g.graph:
        _initialize_nodes(g)
    for col, map in maps.items():
        g.graph['nodeframe'][col] = list(extract_nodes(g, map))


def save_edges(g, maps):
    if 'edgeframe' not in g.graph:
        _initialize_edges(g)
    for col, map in maps.items():
        g.graph['edgeframe'][col] = list(extract_edges(g, map))


def concat(dfs, col):
    for value, df in dfs.items():
        df[col] = value
    return pd.concat(dfs.values())


def concat_nodes(graphs, col):
    return concat({value: g.graph['nodeframe'] for value, g in graphs.items()}, col)


def concat_edges(graphs, col):
    return concat({value: g.graph['edgeframe'] for value, g in graphs.items()}, col)


def correlation(df, x, y):
    return pearsonr(df[x], df[y])


def correlation_nodes(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    return correlation(g.graph['nodeframe'], x, y)


def correlation_edges(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    return correlation(g.graph['edgeframe'], x, y)


def chisquared(df, rows, cols):
    observed = pd.crosstab(df[rows], df[cols])
    c, p, _, _ = chi2_contingency(observed)
    return c, p


def chisquared_nodes(g, rows, cols, rmap=None, cmap=None):
    maps = _filter({
        rows: rmap,
        cols: cmap,
    })
    if maps:
        save_nodes(g, maps)
    return chisquared(g.graph['nodeframe'], rows, cols)


def chisquared_edges(g, rows, cols, rmap=None, cmap=None):
    maps = _filter({
        rows: rmap,
        cols: cmap,
    })
    if maps:
        save_edges(g, maps)
    return chisquared(g.graph['edgeframe'], rows, cols)


def student(df, a, b):
    d = abs(df[a].mean() - df[b].mean())
    _, p = ttest_ind(df[a], df[b])
    return d, p


def student_nodes(g, a, b, amap=None, bmap=None):
    maps = _filter({
        a: amap,
        b: bmap,
    })
    if maps:
        save_nodes(g, maps)
    return student(g.graph['nodeframe'], a, b)


def student_edges(g, a, b, amap=None, bmap=None):
    maps = _filter({
        a: amap,
        b: bmap,
    })
    if maps:
        save_edges(g, maps)
    return student(g.graph['edgeframe'], a, b)


def linregress(df, X, y):
    dfX = list(zip(*(df[x] for x in X)))
    model = LinearRegression()
    model.fit(dfX, df[y])
    return [coef for coef in model.coef_], model.score(dfX, df[y])


def linregress_nodes(g, X, y, Xmap=None, ymap=None):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        save_nodes(g, maps)
    return linregress(g.graph['nodeframe'], X, y)


def linregress_edges(g, X, y, Xmap=None, ymap=None):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        save_edges(g, maps)
    return linregress(g.graph['edgeframe'], X, y)


def logregress(df, X, y, max_iter):
    dfX = list(zip(*(df[x] for x in X)))
    model = LogisticRegression(solver='lbfgs', max_iter=max_iter, multi_class='auto')
    model.fit(dfX, df[y])
    return {class_: [coef for coef in coef_] for class_, coef_ in zip(model.classes_, model.coef_)}, model.score(dfX, df[y])


def logregress_nodes(g, X, y, Xmap=None, ymap=None, max_iter=100):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        save_nodes(g, maps)
    return logregress(g.graph['nodeframe'], X, y, max_iter)


def logregress_edges(g, X, y, Xmap=None, ymap=None, max_iter=100):
    maps = _filter(_merge(X, y, Xmap, ymap))
    if maps:
        save_edges(g, maps)
    return logregress(g.graph['edgeframe'], X, y, max_iter)


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
    return encode(g.graph['nodeframe'], X)


def encode_edges(g, X, Xmap=None):
    if Xmap is not None:
        save_edges(g, {x: xmap for x, xmap in zip(X, Xmap)})
    return encode(g.graph['edgeframe'], X)


def distplot(df, a):
    sns.distplot(a=df[a])


def distplot_nodes(g, a, amap=None):
    if amap is not None:
        save_nodes(g, {a: amap})
    distplot(g.graph['nodeframe'], a)


def distplot_edges(g, a, amap=None):
    if amap is not None:
        save_edges(g, {a: amap})
    distplot(g.graph['edgeframe'], a)


def barplot(df, x, control):
    sns.catplot(data=df, x=x, kind='count', hue=control)


def barplot_nodes(g, x, xmap=None, control=None):
    if xmap is not None:
        save_nodes(g, {x: xmap})
    barplot(g.graph['nodeframe'], x, control)


def barplot_edges(g, x, xmap=None, control=None):
    if xmap is not None:
        save_edges(g, {x: xmap})
    barplot(g.graph['edgeframe'], x, control)


def scatterplot(df, x, y, control):
    sns.scatterplot(data=df, x=x, y=y, hue=control)


def scatterplot_nodes(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    scatterplot(g.graph['nodeframe'], x, y, control)


def scatterplot_edges(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    scatterplot(g.graph['edgeframe'], x, y, control)


def pairplot(df, vars, control):
    sns.pairplot(data=df, vars=vars, hue=control)


def pairplot_nodes(g, vars, maps=None, control=None):
    if maps is not None:
        save_nodes(g, {col: map for col, map in zip(vars, maps)})
    pairplot(g.graph['nodeframe'], vars, control)


def pairplot_edges(g, vars, maps=None, control=None):
    if maps is not None:
        save_edges(g, {col: map for col, map in zip(vars, maps)})
    pairplot(g.graph['edgeframe'], vars, control)


def jointplot(df, x, y):
    sns.jointplot(x=df[x], y=df[y], kind='hex')


def jointplot_nodes(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    jointplot(g.graph['nodeframe'], x, y)


def jointplot_edges(g, x, y, xmap=None, ymap=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    jointplot(g.graph['edgeframe'], x, y)


def boxplot(df, x, y, control):
    sns.boxplot(data=df, x=x, y=y, hue=control)


def boxplot_nodes(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_nodes(g, maps)
    boxplot(g.graph['nodeframe'], x, y, control)


def boxplot_edges(g, x, y, xmap=None, ymap=None, control=None):
    maps = _filter({
        x: xmap,
        y: ymap,
    })
    if maps:
        save_edges(g, maps)
    boxplot(g.graph['edgeframe'], x, y, control)
