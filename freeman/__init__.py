from itertools import permutations, combinations
from wrapt import ObjectProxy

from .drawing import *
from .exploring import *
from .moving import *
from .analyzing import *


def load(path, key='random', *args, **kwargs):
    g = networkx.read_gml(path, label='id')

    if isinstance(g, networkx.MultiGraph):
        raise NetworkXError('freeman does not support multigraphs')

    free = []
    for n in g.nodes:
        if 'x' not in g.nodes[n] or 'y' not in g.nodes[n]:
            free.append(n)

    if len(free) > 0 and len(free) < g.number_of_nodes():
        raise ValueError('some nodes have position, but others do not: ' + ', '.join([str(n) for n in free]))

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

    for n, m in g.edges:
        if 'labflip' in g.edges[n, m]:
            value = g.edges[n, m]['labflip']

            if value == 0 or value == 1:
                g.edges[n, m]['labflip'] = bool(value)
            else:
                raise ValueError('labflip must be binary')

    return FreemanGraph(g)


def dyads(g, ordered=False):
    if ordered:
        return permutations(g.nodes, 2)
    return combinations(g.nodes, 2)


def triads(g, ordered=False):
    if ordered:
        return permutations(g.nodes, 3)
    return combinations(g.nodes, 3)


def copy_node(g, h, n):
    if not h.has_node(n):
        raise ValueError('second graph must have the node')
    if not g.has_node(n):
        g.add_node(n)
    g.nodes[n].update(h.nodes[n])


def copy_edge(g, h, n, m):
    if not h.has_edge(n, m):
        raise ValueError('second graph must have the edge')
    if not g.has_edge(n, m):
        g.add_edge(n, m)
    g.edges[n, m].update(h.edges[n, m])


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


class FreemanGraph(ObjectProxy):
    def interact(self, path=None, physics=False):
        interact(self, path, physics)
    def draw(self, toolbar=False):
        draw(self, toolbar)

    def extract_nodes(self, map, filter=None):
        return extract_nodes(self, map, filter)
    def extract_edges(self, map, filter=None):
        return extract_edges(self, map, filter)
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
    def scale_nodes_alpha(self, map, lower=None, upper=None, hue=None):
        scale_nodes_alpha(self, map, lower, upper, hue)
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
    def move_negative(self, key, weight, *args, **kwargs):
        move_negative(self, key, weight, *args, **kwargs)
    def move_complement(self, key, *args, **kwargs):
        move_complement(self, key, *args, **kwargs)

    def save_nodes(self, maps):
        save_nodes(self, maps)
    def save_edges(self, maps):
        save_edges(self, maps)
    def chisquare_nodes(self, rows, cols, rmap=None, cmap=None):
        return chisquare_nodes(self, rows, cols, rmap, cmap)
    def chisquare_edges(self, rows, cols, rmap=None, cmap=None):
        return chisquare_edges(self, rows, cols, rmap, cmap)
    def correlation_nodes(self, x, y, xmap=None, ymap=None):
        return correlation_nodes(self, x, y, xmap, ymap)
    def correlation_edges(self, x, y, xmap=None, ymap=None):
        return correlation_edges(self, x, y, xmap, ymap)
    def student_nodes(self, rows, cols, rmap=None, cmap=None):
        return student_nodes(self, rows, cols, rmap, cmap)
    def student_edges(self, rows, cols, rmap=None, cmap=None):
        return student_edges(self, rows, cols, rmap, cmap)
    def linregress_nodes(self, X, y, Xmap=None, ymap=None):
        return linregress_nodes(self, X, y, Xmap, ymap)
    def linregress_edges(self, X, y, Xmap=None, ymap=None):
        return linregress_edges(self, X, y, Xmap, ymap)
    def logregress_nodes(self, X, y, Xmap=None, ymap=None, max_iter=100):
        return logregress_nodes(self, X, y, Xmap, ymap)
    def logregress_edges(self, X, y, Xmap=None, ymap=None, max_iter=100):
        return logregress_edges(self, X, y, Xmap, ymap)
    def encode_nodes(self, X, Xmap=None):
        encode_nodes(self, X, Xmap)
    def encode_edges(self, X, Xmap=None):
        encode_edges(self, X, Xmap)
    def barplot_nodes(self, group, hue, groupmap=None, huemap=None):
        barplot_nodes(self, group, hue, groupmap, huemap)
    def barplot_edges(self, group, hue, groupmap=None, huemap=None):
        barplot_edges(self, group, hue, groupmap, huemap)
    def scatterplot_nodes(self, x, y, xmap=None, ymap=None, control=None):
        scatterplot_nodes(self, x, y, xmap, ymap, control)
    def scatterplot_edges(self, x, y, xmap=None, ymap=None, control=None):
        scatterplot_edges(self, x, y, xmap, ymap, control)
    def pairplot_nodes(self, cols, maps=None, control=None):
        pairplot_nodes(self, cols, maps, control)
    def pairplot_edges(self, cols, maps=None, control=None):
        pairplot_edges(self, cols, maps, control)
    def jointplot_nodes(self, x, y, xmap=None, ymap=None):
        jointplot_nodes(self, x, y, xmap, ymap)
    def jointplot_edges(self, x, y, xmap=None, ymap=None):
        jointplot_edges(self, x, y, xmap, ymap)
    def boxplot_nodes(self, x, y, xmap=None, ymap=None, control=None):
        boxplot_nodes(self, x, y, xmap, ymap, control)
    def boxplot_edges(self, x, y, xmap=None, ymap=None, control=None):
        boxplot_edges(self, x, y, xmap, ymap, control)

    def dyads(self, ordered=False):
        return dyads(self, ordered)
    def triads(self, ordered=False):
        return triads(self, ordered)
    def copy_node(self, h, n):
        copy_node(self, h, n)
    def copy_edge(self, h, n, m):
        copy_edge(self, h, n, m)
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
