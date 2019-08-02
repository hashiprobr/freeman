import pandas as pd
import seaborn as sns

from scipy.stats import chi2_contingency, pearsonr, ttest_ind
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


def chisquare(df, rows, cols):
    observed = pd.crosstab(df[rows], df[cols])
    _, p, _, expected = chi2_contingency(observed)
    return pd.DataFrame(expected), p


def chisquare_nodes(g, rows, cols, rmap=None, cmap=None):
    maps = _filter({
        rows: rmap,
        cols: cmap,
    })
    if maps:
        save_nodes(g, maps)
    return chisquare(g.graph['nodeframe'], rows, cols)


def chisquare_edges(g, rows, cols, rmap=None, cmap=None):
    maps = _filter({
        rows: rmap,
        cols: cmap,
    })
    if maps:
        save_edges(g, maps)
    return chisquare(g.graph['edgeframe'], rows, cols)


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


def student(df, rows, cols):
    _, p = ttest_ind(x, y)
    return p


def student_nodes(g, rows, cols, rmap=None, cmap=None):
    maps = _filter({
        rows: rmap,
        cols: cmap,
    })
    if maps:
        save_nodes(g, maps)
    return student(g.graph['nodeframe'], rows, cols)


def student_edges(g, rows, cols, rmap=None, cmap=None):
    maps = _filter({
        rows: rmap,
        cols: cmap,
    })
    if maps:
        save_edges(g, maps)
    return student(g.graph['edgeframe'], rows, cols)


def linregress(df, X, y):
    dfX = zip(*(df[x] for x in X))
    model = LinearRegression()
    model.fit(dfX, df[y])
    return [coef for coef in model.coef_], model.score(X, y)


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
    dfX = zip(*(df[x] for x in X))
    model = LogisticRegression(solver='lbfgs', max_iter=max_iter, multi_class='auto')
    model.fit(dfX, df[y])
    return [coef for coef in model.coef_], model.score(X, y)


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
    for col, x in zip(encoder.get_feature_names(), X):
        df[col] = x


def encode_nodes(g, X, Xmap=None):
    if Xmap is not None:
        save_nodes(g, {x: xmap for x, xmap in zip(X, Xmap)})
    encode(g.graph['nodeframe'], X)


def encode_edges(g, X, Xmap=None):
    if Xmap is not None:
        save_edges(g, {x: xmap for x, xmap in zip(X, Xmap)})
    encode(g.graph['edgeframe'], X)


def barplot(df, group, hue):
    sns.catplot(x=df[group], hue=df[hue], kind='count')


def barplot_nodes(g, group, hue, groupmap=None, huemap=None):
    maps = _filter({
        group: groupmap,
        hue: huemap,
    })
    if maps:
        save_nodes(g, maps)
    barplot(g.graph['nodeframe'], group, hue)


def barplot_edges(g, group, hue, groupmap=None, huemap=None):
    maps = _filter({
        group: groupmap,
        hue: huemap,
    })
    if maps:
        save_edges(g, maps)
    barplot(g.graph['edgeframe'], group, hue)


def scatterplot(df, x, y, control):
    sns.scatterplot(df[x], df[y], hue=control)


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


def pairplot(df, cols, control):
    sns.pairplot(df[cols], hue=control)


def pairplot_nodes(g, cols, maps=None, control=None):
    if maps is not None:
        save_nodes(g, {col: map for col, xmap in zip(cols, maps)})
    pairplot(g.graph['nodeframe'], cols, control)


def pairplot_edges(g, cols, maps=None, control=None):
    if maps is not None:
        save_edges(g, {col: map for col, xmap in zip(cols, maps)})
    pairplot(g.graph['edgeframe'], cols, control)


def jointplot(df, x, y):
    sns.jointplot(df[x], df[y], kind='hex')


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
    sns.catplot(x, y, hue=control, kind="box")


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
