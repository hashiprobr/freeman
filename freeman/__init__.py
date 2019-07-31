from itertools import permutations, combinations

from .drawing import *
from .moving import *
from .exploring import *


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
            x = g.nodes[n]['x']
            if not isinstance(x, int) and not isinstance(x, float):
                raise TypeError('non-numeric x in node ' + str(n))
            y = g.nodes[n]['y']
            if not isinstance(y, int) and not isinstance(y, float):
                raise TypeError('non-numeric y in node ' + str(n))

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
                raise ValueError('non-binary labflip in edge ({}, {})'.format(n, m))

    return g


def dyads(g, ordered=False):
    if ordered:
        generator = permutations(g, 2)
    else:
        generator = combinations(g, 2)

    for n, m in generator:
        yield n, m


def triads(g, ordered=False):
    if ordered:
        generator = permutations(g, 3)
    else:
        generator = combinations(g, 3)

    for n, m, l in generator:
        yield n, m, l


def copy_node(g, h, n):
    if not g.has_node(n):
        g.add_node(n)
    g.nodes[n].update(h.nodes[n])


def copy_edge(g, h, n, m):
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
