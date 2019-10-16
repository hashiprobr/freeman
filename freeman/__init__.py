from random import random, uniform
from wrapt import ObjectProxy

from .drawing import *
from .exploring import *
from .moving import *
from .analyzing import *
from .simulating import *


def _parse(value):
    if isinstance(value, str):
        line = value.strip()
        if line.startswith('rgb(') or line.startswith('rgba('):
            if not line.endswith(')'):
                raise ValueError('rgb and rgba must end with \')\'')
            length = line.find('(')
            phrase = line[(length + 1):-1]
            if phrase.find('(') != -1 or phrase.find(')') != -1:
                raise ValueError('rgb and rgba must have only one \'(\' and only one \')\'')

            words = phrase.split(',')
            if len(words) != length:
                if length == 3:
                    raise ValueError('rgb must have three components')
                else:
                    raise ValueError('rgba must have four components')

            r = int(words[0])
            g = int(words[1])
            b = int(words[2])
            if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
                raise ValueError('rgb channels must be between 0 and 255')
            if length == 4:
                a = float(words[3])
                if a < 0 or a > 1:
                    raise ValueError('rgba alpha must be between 0 and 1')
                return (r, g, b, a)
            else:
                return (r, g, b)

    return value


def load(path):
    g = nx.read_gml(path, 'id')

    keys = list(g.graph)
    for key in keys:
        if key.startswith('node_'):
            suffix = key[5:]
            for n in g.nodes:
                if suffix not in g.nodes[n]:
                    g.nodes[n][suffix] = g.graph[key]
            del g.graph[key]
        if key.startswith('edge_'):
            suffix = key[5:]
            for n, m in g.edges:
                if suffix not in g.edges[n, m]:
                    g.edges[n, m][suffix] = g.graph[key]
            del g.graph[key]

    for n in g.nodes:
        for key in g.nodes[n]:
            g.nodes[n][key] = _parse(g.nodes[n][key])

        if 'pos' in g.nodes[n]:
            warn('node pos is not allowed in file, ignoring')
        if 'x' in g.nodes[n]:
            x = g.nodes[n]['x']
            del g.nodes[n]['x']
        else:
            x = None
        if 'y' in g.nodes[n]:
            y = g.nodes[n]['y']
            del g.nodes[n]['y']
        else:
            y = None
        g.nodes[n]['pos'] = (x, y)

    for n, m in g.edges:
        for key in g.edges[n, m]:
            g.edges[n, m][key] = _parse(g.edges[n, m][key])

        if 'labflip' in g.edges[n, m]:
            value = g.edges[n, m]['labflip']
            if value != 0 and value != 1:
                raise ValueError('edge labflip must be binary')
            g.edges[n, m]['labflip'] = bool(value)

    return Graph(g)


def init(g):
    X = []
    Y = []
    for n in g.nodes:
        x = None
        y = None
        if 'pos' in g.nodes[n]:
            pos = g.nodes[n]['pos']
            if isinstance(pos, (tuple, list)):
                if len(pos) == 2:
                    if pos[0] is not None:
                        if isinstance(pos[0], (int, float)):
                            x = pos[0]
                        else:
                            warn('node x must be numeric, ignoring')
                    if pos[1] is not None:
                        if isinstance(pos[1], (int, float)):
                            y = pos[1]
                        else:
                            warn('node y must be numeric, ignoring')
                else:
                    warn('node pos must have exactly two elements, ignoring')
            else:
                warn('node pos must be a tuple or list, ignoring')
        X.append(x)
        Y.append(y)

    Xnum = [x for x in X if x is not None]
    if Xnum:
        xmin = min(Xnum)
        xmax = max(Xnum)
        if isclose(xmin, xmax):
            xmin -= abs(xmin)
            xmax += abs(xmax)
        for i, x in enumerate(X):
            if X[i] is None:
                X[i] = uniform(xmin, xmax)
    else:
        X = [random() for x in X]

    Ynum = [y for y in Y if y is not None]
    if Ynum:
        ymin = min(Ynum)
        ymax = max(Ynum)
        if isclose(ymin, ymax):
            ymin -= abs(ymin)
            ymax += abs(ymax)
        for i, y in enumerate(Y):
            if Y[i] is None:
                Y[i] = uniform(ymin, ymax)
    else:
        Y = [random() for y in Y]

    for n, x, y in zip(g.nodes, X, Y):
        g.nodes[n]['pos'] = (x, y)


def dyads(g, ordered=False):
    if ordered:
        return permutations(g.nodes, 2)
    return combinations(g.nodes, 2)


def triads(g, ordered=False):
    if ordered:
        return permutations(g.nodes, 3)
    return combinations(g.nodes, 3)


def flip_existence(g, n, m):
    if g.has_edge(n, m):
        g.remove_edge(n, m)
    else:
        g.add_edge(n, m)


def flip_direction(g, n, m):
    if not isinstance(g, nx.DiGraph):
        raise TypeError('graph must be directed')
    if not g.has_edge(n, m):
        raise ValueError('original edge must exist')
    if g.has_edge(m, n):
        raise ValueError('opposite edge must not exist')
    g.add_edge(m, n)
    g.edges[m, n].update(g.edges[n, m])
    g.remove_edge(n, m)


def set_each_node(g, key, map):
    values = list(extract_nodes(g, map))
    for n, value in zip(g.nodes, values):
        g.nodes[n][key] = value


def set_each_edge(g, key, map):
    values = list(extract_edges(g, map))
    for (n, m), value in zip(g.edges, values):
        g.edges[n, m][key] = value


def set_all_nodes(g, key, value, filter=None):
    if filter is None:
        nodes = g.nodes
    else:
        nodes = [n for n in g.nodes if filter(n)]
    for n in nodes:
        g.nodes[n][key] = value


def set_all_edges(g, key, value, filter=None):
    if filter is None:
        edges = g.edges
    else:
        edges = [(n, m) for n, m in g.edges if filter(n, m)]
    for n, m in edges:
        g.edges[n, m][key] = value


def unset_nodes(g, key):
    for n in g.nodes:
        if key in g.nodes[n]:
            del g.nodes[n][key]


def unset_edges(g, key):
    for n, m in g.edges:
        if key in g.edges[n, m]:
            del g.edges[n, m][key]


def convert_nodes(g, source, target, map):
    values = [map[g.nodes[n][source]] for n in g.nodes]
    for n, value in zip(g.nodes, values):
        g.nodes[n][target] = value


def convert_edges(g, source, target, map):
    values = [map[g.edges[n, m][source]] for n, m in g.edges]
    for (n, m), value in zip(g.edges, values):
        g.edges[n, m][target] = value


def skin_seaborn(g, nodes=[]):
    g.graph['width'] = 450
    g.graph['height'] = 450
    g.graph['bottom'] = 0
    g.graph['left'] = 0
    g.graph['right'] = 0
    g.graph['top'] = 0

    set_all_nodes(g, 'size', 10)
    set_all_nodes(g, 'style', 'circle')
    set_all_nodes(g, 'color', (76, 116, 172))
    set_all_nodes(g, 'color', (219, 130, 87), lambda n: n not in nodes)
    set_all_nodes(g, 'bwidth', 0)
    set_all_nodes(g, 'labpos', 'hover')

    set_all_edges(g, 'width', 1)
    set_all_edges(g, 'style', 'solid')
    set_all_edges(g, 'color', (135, 135, 138))
    unset_edges(g, 'label')


def skin_pyvis(g):
    set_all_nodes(g, 'size', 50)
    set_all_nodes(g, 'style', 'circle')
    set_all_nodes(g, 'color', (151, 194, 252))
    set_all_nodes(g, 'bwidth', 1)
    set_all_nodes(g, 'bcolor', (43, 124, 233))

    set_all_edges(g, 'width', 1)
    set_all_edges(g, 'style', 'solid')
    set_all_edges(g, 'color', (43, 124, 233))


def concat_nodes(graphs, key):
    dataframes = {}
    for value, g in graphs.items():
        df = g.nodeframe.copy()
        df['node'] = g.nodes
        dataframes[value] = df
    return concat(dataframes, key)


def concat_edges(graphs, key):
    dataframes = {}
    for value, g in graphs.items():
        df = g.edgeframe.copy()
        df['edge'] = g.edges
        dataframes[value] = df
    return concat(dataframes, key)


class Graph(ObjectProxy):
    def interact(self, physics=False, path=None):
        '''Object-oriented wrapper for :func:`interact <freeman.drawing.interact>`.'''
        interact(self, physics, path)
    def draw(self, toolbar=False):
        '''Object-oriented wrapper for :func:`draw <freeman.drawing.draw>`.'''
        draw(self, toolbar)

    def extract_nodes(self, map):
        return extract_nodes(self, map)
    def extract_edges(self, map):
        return extract_edges(self, map)
    def label_nodes(self, map=None, ndigits=2):
        label_nodes(self, map, ndigits)
    def label_edges(self, map=None, ndigits=2):
        label_edges(self, map, ndigits)
    def color_borders(self, dark=0.5):
        color_borders(self, dark)
    def color_nodes(self, map=None, dark=0):
        color_nodes(self, map, dark)
    def color_edges(self, map=None, dark=0.5):
        color_edges(self, map, dark)
    def color_community_nodes(self, C, dark=0):
        color_community_nodes(self, C, dark)
    def color_community_edges(self, C, dark=0.5, alpha=0.5):
        color_community_edges(self, C, dark, alpha)
    def scale_nodes_size(self, map, lower=None, upper=None):
        scale_nodes_size(self, map, lower, upper)
    def scale_edges_width(self, map, lower=None, upper=None):
        scale_edges_width(self, map, lower, upper)
    def scale_nodes_dark(self, map, lower=None, upper=None, hue=None):
        scale_nodes_dark(self, map, lower, upper, hue)
    def scale_edges_alpha(self, map, lower=None, upper=None, hue=None):
        scale_edges_alpha(self, map, lower, upper, hue)
    def heat_nodes(self, map, lower=None, upper=None, middle=None, classic=False):
        heat_nodes(self, map, lower, upper, middle, classic)
    def heat_edges(self, map, lower=None, upper=None, middle=None, classic=False):
        heat_edges(self, map, lower, upper, middle, classic)

    def scatter(self, xmap, ymap):
        scatter(self, xmap, ymap)
    def move(self, key, *args, **kwargs):
        move(self, key, *args, **kwargs)
    def move_inverse(self, key, weight, *args, **kwargs):
        move_inverse(self, key, weight, *args, **kwargs)
    def move_complement(self, key, *args, **kwargs):
        move_complement(self, key, *args, **kwargs)

    def set_nodedata(self, key, map):
        self.nodeframe[key] = list(extract_nodes(self, map))
    def set_edgedata(self, key, map):
        self.edgeframe[key] = list(extract_edges(self, map))
    def assign_nodes(self, other, key):
        assign(self.nodeframe, other.nodeframe, key)
    def assign_edges(self, other, key):
        assign(self.edgeframe, other.edgeframe, key)
    def distest_nodes(self, x):
        return distest(self.nodeframe, x)
    def distest_edges(self, x):
        return distest(self.edgeframe, x)
    def cortest_nodes(self, x, y, max_perm=None):
        return cortest(self.nodeframe, x, y, max_perm)
    def cortest_edges(self, x, y, max_perm=None):
        return cortest(self.edgeframe, x, y, max_perm)
    def chitest_nodes(self, x, y, max_perm=None):
        return chitest(self.nodeframe, x, y, max_perm)
    def chitest_edges(self, x, y, max_perm=None):
        return chitest(self.edgeframe, x, y, max_perm)
    def reltest_nodes(self, a, b, max_perm=None):
        return reltest(self.nodeframe, a, b, max_perm)
    def reltest_edges(self, a, b, max_perm=None):
        return reltest(self.edgeframe, a, b, max_perm)
    def mixtest_nodes(self, x, y, max_perm=None):
        return mixtest(self.nodeframe, x, y, max_perm)
    def mixtest_edges(self, x, y, max_perm=None):
        return mixtest(self.edgeframe, x, y, max_perm)
    def linregress_nodes(self, X, y, *args, **kwargs):
        return linregress(self.nodeframe, X, y, *args, **kwargs)
    def linregress_edges(self, X, y, *args, **kwargs):
        return linregress(self.edgeframe, X, y, *args, **kwargs)
    def logregress_nodes(self, X, y, *args, **kwargs):
        return logregress(self.nodeframe, X, y, *args, **kwargs)
    def logregress_edges(self, X, y, *args, **kwargs):
        return logregress(self.edgeframe, X, y, *args, **kwargs)
    def intencode_nodes(self, x, order=None):
        return intencode(self.nodeframe, x, order)
    def intencode_edges(self, x, order=None):
        return intencode(self.edgeframe, x, order)
    def binencode_nodes(self, x):
        return binencode(self.nodeframe, x)
    def binencode_edges(self, x):
        return binencode(self.edgeframe, x)
    def displot_nodes(self, x):
        displot(self.nodeframe, x)
    def displot_edges(self, x):
        displot(self.edgeframe, x)
    def barplot_nodes(self, x, control=None):
        barplot(self.nodeframe, x, control)
    def barplot_edges(self, x, control=None):
        barplot(self.edgeframe, x, control)
    def linplot_nodes(self, x, y, control=None):
        linplot(self.nodeframe, x, y, control)
    def linplot_edges(self, x, y, control=None):
        linplot(self.edgeframe, x, y, control)
    def scaplot_nodes(self, x, y, control=None):
        scaplot(self.nodeframe, x, y, control)
    def scaplot_edges(self, x, y, control=None):
        scaplot(self.edgeframe, x, y, control)
    def matplot_nodes(self, X, control=None):
        matplot(self.nodeframe, X, control)
    def matplot_edges(self, X, control=None):
        matplot(self.edgeframe, X, control)
    def valcount_nodes(self, x, order=None, transpose=False):
        return valcount(self.nodeframe, x, order, transpose)
    def valcount_edges(self, x, order=None, transpose=False):
        return valcount(self.edgeframe, x, order, transpose)
    def contable_nodes(self, x, y):
        return contable(self.nodeframe, x, y)
    def contable_edges(self, x, y):
        return contable(self.edgeframe, x, y)
    def corplot_twomode(self, nodes, weight='weight'):
        corplot_twomode(self, nodes, weight)
    def analyze_to_move(self, nodes, weight='weight'):
        analyze_to_move(self, nodes, weight)
    def corplot_nodes(self, x, y):
        corplot(self.nodeframe, x, y)
    def corplot_edges(self, x, y):
        corplot(self.edgeframe, x, y)
    def boxplot_nodes(self, x, y, control=None):
        boxplot(self.nodeframe, x, y, control)
    def boxplot_edges(self, x, y, control=None):
        boxplot(self.edgeframe, x, y, control)
    def girvan_newman(self):
        girvan_newman(self)

    def __init__(self, g):
        super().__init__(g.copy())
        init(self)
    def dyads(self, ordered=False):
        return dyads(self, ordered)
    def triads(self, ordered=False):
        return triads(self, ordered)
    def flip_existence(self, n, m):
        flip_existence(self, n, m)
    def flip_direction(self, n, m):
        flip_direction(self, n, m)
    def set_each_node(self, key, map):
        set_each_node(self, key, map)
    def set_each_edge(self, key, map):
        set_each_edge(self, key, map)
    def set_all_nodes(self, key, value, filter=None):
        set_all_nodes(self, key, value, filter)
    def set_all_edges(self, key, value, filter=None):
        set_all_edges(self, key, value, filter)
    def unset_nodes(self, key):
        unset_nodes(self, key)
    def unset_edges(self, key):
        unset_edges(self, key)
    def convert_nodes(self, source, target, map):
        convert_nodes(self, source, target, map)
    def convert_edges(self, source, target, map):
        convert_edges(self, source, target, map)
    def skin_seaborn(self, other=[]):
        skin_seaborn(self, other)
    def skin_pyvis(self):
        skin_pyvis(self)

    def copy(self):
        return Graph(self.__wrapped__.copy())
    def to_undirected(self):
        return Graph(self.__wrapped__.to_undirected())
    def to_directed(self):
        return Graph(self.__wrapped__.to_directed())
    def subgraph(self, nodes):
        return Graph(self.__wrapped__.subgraph(nodes))
    def edge_subgraph(self, edges):
        return Graph(self.__wrapped__.edge_subgraph(edges))
    def reverse(self):
        return Graph(self.__wrapped__.reverse())

    @property
    def nodeframe(self):
        if not hasattr(self, '_nodeframe'):
            self._nodeframe = pd.DataFrame()
        self._nodeframe = self._nodeframe.reindex(self.nodes, copy=False)
        return self._nodeframe

    @property
    def edgeframe(self):
        if not hasattr(self, '_edgeframe'):
            self._edgeframe = pd.DataFrame()
        self._edgeframe = self._edgeframe.reindex(self.edges, copy=False)
        return self._edgeframe
