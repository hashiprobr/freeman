from wrapt import ObjectProxy

from .drawing import *
from .exploring import *
from .moving import *
from .analyzing import *
from .simulating import *


def load(path, key='random', *args, **kwargs):
    g = nx.read_gml(path, label='id')

    if isinstance(g, nx.MultiGraph):
        raise NetworkXError('freeman does not support multigraphs')

    free = []
    for n in g.nodes:
        if 'x' not in g.nodes[n] or 'y' not in g.nodes[n]:
            free.append(n)

    if len(free) > 0 and len(free) < g.number_of_nodes():
        raise ValueError('some nodes have position, but others do not: ' + ', '.join(str(n) for n in free))

    if free:
        move(g, key, *args, **kwargs)
    else:
        for n in g.nodes:
            x = assert_numeric(g.nodes[n]['x'])
            y = assert_numeric(g.nodes[n]['y'])
            g.nodes[n]['pos'] = (x, y)
            del g.nodes[n]['x']
            del g.nodes[n]['y']

        normalize(g)

    for n in g.nodes:
        if 'border' in g.nodes[n]:
            value = g.nodes[n]['border']
            if value != 0 and value != 1:
                raise ValueError('node border must be binary')
            g.nodes[n]['border'] = bool(value)

    for n, m in g.edges:
        if 'labflip' in g.edges[n, m]:
            value = g.edges[n, m]['labflip']
            if value != 0 and value != 1:
                raise ValueError('edge labflip must be binary')
            g.edges[n, m]['labflip'] = bool(value)

    return Graph(g)


def dyads(g, ordered=False):
    if ordered:
        return permutations(g.nodes, 2)
    return combinations(g.nodes, 2)


def triads(g, ordered=False):
    if ordered:
        return permutations(g.nodes, 3)
    return combinations(g.nodes, 3)


def set_each_node(g, key, map, filter=None):
    for n in g.nodes:
        if filter is None or filter(n):
            g.nodes[n][key] = extract_node(g, n, map)


def set_each_edge(g, key, map, filter=None):
    for n, m in g.edges:
        if filter is None or filter(n, m):
            g.edges[n, m][key] = extract_edge(g, n, m, map)


def set_all_nodes(g, key, value, filter=None):
    for n in g.nodes:
        if filter is None or filter(n):
            g.nodes[n][key] = value


def set_all_edges(g, key, value, filter=None):
    for n, m in g.edges:
        if filter is None or filter(n, m):
            g.edges[n, m][key] = value


def unset_nodes(g, key, filter=None):
    for n in g.nodes:
        if (filter is None or filter(n)) and key in g.nodes[n]:
            del g.nodes[n][key]


def unset_edges(g, key, filter=None):
    for n, m in g.edges:
        if (filter is None or filter(n, m)) and key in g.edges[n, m]:
            del g.edges[n, m][key]


def skin_seaborn(g):
    g.graph['width'] = 450
    g.graph['height'] = 450
    g.graph['bottom'] = 0
    g.graph['left'] = 0
    g.graph['right'] = 0
    g.graph['top'] = 0

    set_all_nodes(g, 'size', 10)
    set_all_nodes(g, 'style', 'circle')
    set_all_nodes(g, 'border', False)
    set_all_nodes(g, 'labpos', 'hover')

    set_all_edges(g, 'width', 1)
    set_all_edges(g, 'style', 'solid')
    set_all_edges(g, 'color', (135, 135, 138))
    unset_edges(g, 'label')


def colorize_communities(g, C):
    map = {}
    for i, c in enumerate(C):
        for n in c:
            map[n] = i

    colorize_nodes(g, map)


def stack_and_track(graphs, targets=None):
    nodes = set.intersection(*(set(g.nodes) for g in graphs))

    if targets is None:
        targets = nodes

    h = Graph(nx.DiGraph())

    for j, n in enumerate(nodes):
        prev = None

        for i, g in enumerate(graphs):
            curr = i * len(nodes) + j

            h.add_node(curr)
            h.nodes[curr].update(g.nodes[n])

            if prev is not None and n in targets:
                h.add_edge(prev, curr)

            prev = curr

    return h


class Graph(ObjectProxy):
    def __init__(self, g):
        super().__init__(g)
        self._nodeframe = None
        self._edgeframe = None

    @property
    def nodeframe(self):
        if self._nodeframe is None:
            set_nodeframe(self)
        return self._nodeframe

    @nodeframe.setter
    def nodeframe(self, nodeframe):
        self._nodeframe = nodeframe

    @property
    def edgeframe(self):
        if self._edgeframe is None:
            set_edgeframe(self)
        return self._edgeframe

    @edgeframe.setter
    def edgeframe(self, edgeframe):
        self._edgeframe = edgeframe

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

    def interact(self, path=None, physics=False):
        interact(self, path, physics)
    def draw(self, toolbar=False):
        draw(self, toolbar)

    def label_nodes(self, map=None, ndigits=2):
        label_nodes(self, map, ndigits)
    def label_edges(self, map=None, ndigits=2):
        label_edges(self, map, ndigits)
    def colorize_nodes(self, map=None):
        colorize_nodes(self, map)
    def colorize_edges(self, map=None):
        colorize_edges(self, map)
    def scale_nodes_size(self, map, lower=None, upper=None):
        scale_nodes_size(self, map, lower, upper)
    def scale_edges_width(self, map, lower=None, upper=None):
        scale_edges_width(self, map, lower, upper)
    def scale_nodes_dark(self, map, lower=None, upper=None, hue=None):
        scale_nodes_dark(self, map, lower, upper, hue)
    def scale_edges_alpha(self, map, lower=None, upper=None, hue=None):
        scale_edges_alpha(self, map, lower, upper, hue)
    def heat_nodes(self, map, lower=None, upper=None, middle=None):
        heat_nodes(self, map, lower, upper, middle)
    def heat_edges(self, map, lower=None, upper=None, middle=None):
        heat_edges(self, map, lower, upper, middle)

    def scatter(self, xmap, ymap):
        scatter(self, xmap, ymap)
    def move(self, key, *args, **kwargs):
        move(self, key, *args, **kwargs)
    def move_inverse(self, key, weight, *args, **kwargs):
        move_inverse(self, key, weight, *args, **kwargs)
    def move_complement(self, key, *args, **kwargs):
        move_complement(self, key, *args, **kwargs)

    def set_nodecol(self, col, map):
        set_nodecol(self, col, map)
    def set_edgecol(self, col, map):
        set_edgecol(self, col, map)
    def set_nodecols(self, maps):
        set_nodecols(self, maps)
    def set_edgecols(self, maps):
        set_edgecols(self, maps)
    def distest_nodes(self, a):
        return distest_nodes(self, a)
    def distest_edges(self, a):
        return distest_edges(self, a)
    def cortest_nodes(self, x, y, max_perm=None):
        return cortest_nodes(self, x, y, max_perm)
    def cortest_edges(self, x, y, max_perm=None):
        return cortest_edges(self, x, y, max_perm)
    def chitest_nodes(self, x, y, max_perm=None):
        return chitest_nodes(self, x, y, max_perm)
    def chitest_edges(self, x, y, max_perm=None):
        return chitest_edges(self, x, y, max_perm)
    def reltest_nodes(self, a, b, max_perm=None):
        return reltest_nodes(self, a, b, max_perm)
    def reltest_edges(self, a, b, max_perm=None):
        return reltest_edges(self, a, b, max_perm)
    def mixtest_nodes(self, x, y, max_perm=None):
        return mixtest_nodes(self, x, y, max_perm)
    def mixtest_edges(self, x, y, max_perm=None):
        return mixtest_edges(self, x, y, max_perm)
    def linregress_nodes(self, X, y, *args, **kwargs):
        return linregress_nodes(self, X, y, *args, **kwargs)
    def linregress_edges(self, X, y, *args, **kwargs):
        return linregress_edges(self, X, y, *args, **kwargs)
    def logregress_nodes(self, X, y, *args, **kwargs):
        return logregress_nodes(self, X, y, *args, **kwargs)
    def logregress_edges(self, X, y, *args, **kwargs):
        return logregress_edges(self, X, y, *args, **kwargs)
    def intencode_nodes(self, x, order=None):
        return intencode_nodes(self, x, order)
    def intencode_edges(self, x, order=None):
        return intencode_edges(self, x, order)
    def binencode_nodes(self, x):
        return binencode_nodes(self, x)
    def binencode_edges(self, x):
        return binencode_edges(self, x)
    def displot_nodes(self, x):
        displot_nodes(self, x)
    def displot_edges(self, x):
        displot_edges(self, x)
    def barplot_nodes(self, x, control=None):
        barplot_nodes(self, x, control)
    def barplot_edges(self, x, control=None):
        barplot_edges(self, x, control)
    def linplot_nodes(self, x, y, control=None):
        linplot_nodes(self, x, y, control)
    def linplot_edges(self, x, y, control=None):
        linplot_edges(self, x, y, control)
    def scaplot_nodes(self, x, y, control=None):
        scaplot_nodes(self, x, y, control)
    def scaplot_edges(self, x, y, control=None):
        scaplot_edges(self, x, y, control)
    def matplot_nodes(self, cols, control=None):
        matplot_nodes(self, cols, control)
    def matplot_edges(self, cols, control=None):
        matplot_edges(self, cols, control)
    def hexplot_nodes(self, x, y):
        hexplot_nodes(self, x, y)
    def hexplot_edges(self, x, y):
        hexplot_edges(self, x, y)
    def valcount_nodes(self, x, order=None, transpose=False):
        return valcount_nodes(self, x, order, transpose)
    def valcount_edges(self, x, order=None, transpose=False):
        return valcount_edges(self, x, order, transpose)
    def contable_nodes(self, x, y):
        return contable_nodes(self, x, y)
    def contable_edges(self, x, y):
        return contable_edges(self, x, y)
    def corplot_nodes(self, x, y):
        corplot_nodes(self, x, y)
    def corplot_edges(self, x, y):
        corplot_edges(self, x, y)
    def boxplot_nodes(self, x, y, control=None):
        boxplot_nodes(self, x, y, control)
    def boxplot_edges(self, x, y, control=None):
        boxplot_edges(self, x, y, control)
    def girvan_newman(self):
        girvan_newman(self)
    def corplot_graph(self, nodes, weight='weight'):
        return corplot_graph(self, nodes, weight)

    def dyads(self, ordered=False):
        return dyads(self, ordered)
    def triads(self, ordered=False):
        return triads(self, ordered)
    def set_each_node(self, key, map, filter=None):
        set_each_node(self, key, map, filter)
    def set_each_edge(self, key, map, filter=None):
        set_each_edge(self, key, map, filter)
    def set_all_nodes(self, key, value, filter=None):
        set_all_nodes(self, key, value, filter)
    def set_all_edges(self, key, value, filter=None):
        set_all_edges(self, key, value, filter)
    def unset_nodes(self, key, filter=None):
        unset_nodes(self, key, filter)
    def unset_edges(self, key, filter=None):
        unset_edges(self, key, filter)
    def skin_seaborn(self):
        skin_seaborn(self)
    def colorize_communities(self, C):
        colorize_communities(self, C)
