'''Module responsible for transforming graph data into :ref:`visual attributes <visual-attributes>`.


Data maps
---------

Given a graph **g** and a node **n** of this graph, a *node map*, as the name
implies, maps this node to a value. This map can have one of the four types
below.

===================================  =
:func:`Log <freeman.exploring.Log>`  If **map** is a logarithm wrapper, the value is
                                     **log(w + s)**, where **w** is the value recursively
                                     mapped from **n** by **map.wrapped** and **s** is
                                     **map.shift**.

*str*                                If **map** is a string, the value is **g.nodes[n][map]**.

*dict*                               If **map** is a dictionary, the value is **map[n]**.

*callable*                           If **map** is callable, the value is **map(n)**.
===================================  =

Given a graph **g** and an edge **(n, m)** of this graph, an *edge map*, as the
name implies, maps this edge to a value. This map can have one of the four types
below.

===================================  =
:func:`Log <freeman.exploring.Log>`  If **map** is a logarithm wrapper, the value is
                                     **log(w + s)**, where **w** is the value recursively
                                     mapped from **(n, m)** by **map.wrapped** and **s** is
                                     **map.shift**.

*str*                                If **map** is a string, the value is **g.edges[n, m][map]**.

*dict*                               If **map** is a dictionary, the value is **map[n, m]**.

*callable*                           If **map** is callable, the value is **map(n, m)**.
===================================  =
'''
import networkx as nx

from math import isclose, isinf, log
from statistics import mean
from colorsys import rgb_to_hsv, hsv_to_rgb

from .drawing import get_node_label


def _stringify(value, ndigits):
    if isinstance(value, float):
        if isinf(value):
            return '∞'
        value = round(value, ndigits)
    return str(value)


def _transform(h, s, v):
    sr, sg, sb = hsv_to_rgb(h, s, v)

    r = round(sr * 255)
    g = round(sg * 255)
    b = round(sb * 255)

    return r, g, b


def _assert_fraction(value):
    value = assert_numeric(value)
    if value < 0 or value > 1:
        raise ValueError('value must be between 0 and 1')
    return value


def _assert_bounds(iterable, lower, upper):
    values = list(assert_numerics(iterable))

    if lower is None:
        lower = min(values)
    else:
        lower = assert_numeric(lower)
        if any(value < lower for value in values):
            raise ValueError('lower must be below all values')

    if upper is None:
        upper = max(values)
    else:
        upper = assert_numeric(upper)
        if any(value > upper for value in values):
            raise ValueError('upper must be above all values')

    return values, lower, upper


def _assert_reference(values, lower, upper, middle):
    if middle is None:
        middle = mean(values)
    else:
        middle = assert_numeric(middle)
        if middle < lower or middle > upper:
            raise ValueError('middle must be between lower and upper')

    return middle


def _assert_hsv(color):
    if not isinstance(color, (tuple, list)):
        raise TypeError('color must be a tuple or list')
    if len(color) != 3:
        raise ValueError('color must have exactly three elements')
    if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
        raise TypeError('all color elements must be integers')
    if color[0] < 0 or color[0] > 255 or color[1] < 0 or color[1] > 255 or color[2] < 0 or color[2] > 255:
        raise ValueError('all color elements must be between 0 and 255')

    sr = color[0] / 255
    sg = color[1] / 255
    sb = color[2] / 255

    return rgb_to_hsv(sr, sg, sb)


def assert_numeric(value):
    if not isinstance(value, (int, float)):
        raise TypeError('value must be numeric')
    return value


def assert_numerics(values):
    return (assert_numeric(value) for value in values)


def extract_node(g, n, map):
    if isinstance(map, Log):
        return log(extract_node(g, n, map.wrapped) + map.shift)
    if isinstance(map, str):
        return g.nodes[n][map]
    if isinstance(map, dict):
        return map[n]
    if callable(map):
        return map(n)
    raise TypeError('map must be a string, a dictionary, or a callable')


def extract_edge(g, n, m, map):
    if isinstance(map, Log):
        return log(extract_edge(g, n, m, map.wrapped) + map.shift)
    if isinstance(map, str):
        return g.edges[n, m][map]
    if isinstance(map, dict):
        return map[n, m]
    if callable(map):
        return map(n, m)
    raise TypeError('map must be a string, a dictionary, or a callable')


def extract_nodes(g, map):
    return (extract_node(g, n, map) for n in g.nodes)


def extract_edges(g, map):
    return (extract_edge(g, n, m, map) for n, m in g.edges)


def label_nodes(g, map=None, ndigits=2):
    if map is None:
        labels = (str(n) for n in g.nodes)
    else:
        labels = [_stringify(extract_node(g, n, map), ndigits) for n in g.nodes]

    for n, label in zip(g.nodes, labels):
        g.nodes[n]['label'] = label


def label_edges(g, map=None, ndigits=2):
    if map is None:
        labels = (str((n, m)) for n, m in g.edges)
    else:
        labels = [_stringify(extract_edge(g, n, m, map), ndigits) for n, m in g.edges]

    for (n, m), label in zip(g.edges, labels):
        g.edges[n, m]['label'] = label


def color_borders(g, dark=0.5):
    f = 1 - _assert_fraction(dark)

    for n in g.nodes:
        if 'color' in g.nodes[n]:
            h, s, v = _assert_hsv(g.nodes[n]['color'])
        else:
            h, s, v = 0, 0, 1

        g.nodes[n]['bcolor'] = _transform(h, s, f * v)


def color_nodes(g, map=None, dark=0):
    if map is None:
        groups = list(zip(g.nodes))
    else:
        groups = {}
        for n in g.nodes:
            value = extract_node(g, n, map)
            if value not in groups:
                groups[value] = []
            groups[value].append(n)
        groups = [groups[value] for value in sorted(groups)]

    h = 0
    s = 1 / len(groups)
    v = 1 - _assert_fraction(dark)
    for group in groups:
        color = _transform(h, 1, v)
        for n in group:
            g.nodes[n]['color'] = color
        h += s


def color_edges(g, map=None, dark=0.5):
    if map is None:
        groups = list(zip(g.edges))
    else:
        groups = {}
        for n, m in g.edges:
            value = extract_edge(g, n, m, map)
            if value not in groups:
                groups[value] = []
            groups[value].append((n, m))
        groups = [groups[value] for value in sorted(groups)]

    h = 0
    s = 1 / len(groups)
    v = 1 - _assert_fraction(dark)
    for group in groups:
        color = _transform(h, 1, v)
        for n, m in group:
            g.edges[n, m]['color'] = color
        h += s


def color_community_nodes(g, C, dark=0):
    h = 0
    s = 1 / len(C)
    v = 1 - _assert_fraction(dark)
    for c in C:
        color = _transform(h, 1, v)
        for n in c:
            g.nodes[n]['color'] = color
        h += s


def color_community_edges(g, C, dark=0.5, alpha=0.5):
    h = 0
    s = 1 / len(C)
    v = 1 - _assert_fraction(dark)
    colors = {}
    for c in C:
        color = _transform(h, 1, v)
        for n in c:
            colors[n] = color
        h += s

    alpha = _assert_fraction(alpha)
    for n, m in g.edges:
        color = colors[n]
        if color != colors[m]:
            color = (0, 0, 0, alpha)
        g.edges[n, m]['color'] = color


def scale_nodes_size(g, map, lower=None, upper=None):
    values, lower, upper = _assert_bounds(extract_nodes(g, map), lower, upper)

    for n, value in zip(g.nodes, values):
        if isclose(lower, upper):
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        g.nodes[n]['size'] = 5 + round(sc * 45)


def scale_edges_width(g, map, lower=None, upper=None):
    values, lower, upper = _assert_bounds(extract_edges(g, map), lower, upper)

    for (n, m), value in zip(g.edges, values):
        if isclose(lower, upper):
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        g.edges[n, m]['width'] = 1 + round(sc * 9)


def scale_nodes_dark(g, map, lower=None, upper=None, color=None):
    values, lower, upper = _assert_bounds(extract_nodes(g, map), lower, upper)

    for n, value in zip(g.nodes, values):
        if isclose(lower, upper):
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        if color is None:
            c = 255 - round(sc * 255)
            g.nodes[n]['color'] = (c, c, c)
        else:
            h, _, _ = _assert_hsv(color)
            g.nodes[n]['color'] = _transform(h, sc, 1)


def scale_edges_alpha(g, map, lower=None, upper=None, color=None):
    values, lower, upper = _assert_bounds(extract_edges(g, map), lower, upper)

    for (n, m), value in zip(g.edges, values):
        if isclose(lower, upper):
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        if color is None:
            g.edges[n, m]['color'] = (0, 0, 0, sc)
        else:
            h, _, _ = _assert_hsv(color)
            g.edges[n, m]['color'] = (*_transform(h, 1, 1), sc)


def heat_nodes(g, map, lower=None, upper=None, middle=None, classic=False):
    values, lower, upper = _assert_bounds(extract_nodes(g, map), lower, upper)

    middle = _assert_reference(values, lower, upper, middle)

    for n, value in zip(g.nodes, values):
        if isclose(lower, upper):
            g.nodes[n]['color'] = (255, 255, 255)
        else:
            if value < middle:
                sc = (value - lower) / (middle - lower)
                if classic:
                    h = (2 / 3) - sc * (1 / 3)
                    s = 1
                else:
                    h = 2 / 3
                    s = 1 - sc
                g.nodes[n]['color'] = _transform(h, s, 1)
            else:
                sc = (value - middle) / (upper - middle)
                if classic:
                    h = (1 / 3) - sc * (1 / 3)
                    s = 1
                else:
                    h = 0
                    s = sc
                g.nodes[n]['color'] = _transform(h, s, 1)


def heat_edges(g, map, lower=None, upper=None, middle=None, classic=False):
    values, lower, upper = _assert_bounds(extract_edges(g, map), lower, upper)

    middle = _assert_reference(values, lower, upper, middle)

    for (n, m), value in zip(g.edges, values):
        if isclose(lower, upper):
            g.edges[n, m]['color'] = (255, 255, 255, 0)
        else:
            if value < middle:
                sc = (value - lower) / (middle - lower)
                if classic:
                    h = (2 / 3) - sc * (1 / 3)
                    a = 1
                else:
                    h = 2 / 3
                    a = 1 - sc
                g.edges[n, m]['color'] = (*_transform(h, 1, 1), a)
            else:
                sc = (value - middle) / (upper - middle)
                if classic:
                    h = (1 / 3) - sc * (1 / 3)
                    a = 1
                else:
                    h = 0
                    a = sc
                g.edges[n, m]['color'] = (*_transform(h, 1, 1), a)


def stack_and_track(graphs, subjects=[]):
    union = set.union(*(set(g.nodes) for g in graphs))

    step = 1 / len(graphs)

    h = nx.DiGraph()

    for j, n in enumerate(union):
        prev = None

        frac = step

        for i, g in enumerate(graphs):
            if g.has_node(n):
                curr = i * len(union) + j

                h.add_node(curr)
                h.nodes[curr].update(g.nodes[n])
                h.nodes[curr]['id'] = n

                label = get_node_label(h, curr)
                if label is not None:
                    h.nodes[curr]['label'] = '{} ({})'.format(label, i + 1)

                color = h.nodes[curr].get('color', (255, 255, 255))
                hue, sat, val = _assert_hsv(color)
                h.nodes[curr]['color'] = _transform(hue, frac * sat, 1 - frac * (1 - val))

                bcolor = h.nodes[curr].get('bcolor', (0, 0, 0))
                hue, sat, val = _assert_hsv(bcolor)
                h.nodes[curr]['bcolor'] = _transform(hue, frac * sat, 1 - frac * (1 - val))

                if prev is not None and n in subjects:
                    h.add_edge(prev, curr)
                    h.edges[prev, curr]['color'] = (0, 0, 0, (orig + frac) / 2)

                prev = curr

                orig = frac

            frac += step

    return h


class Log:
    '''A Log is a logarithm wrapper for an object.
    '''
    def __init__(self, wrapped, shift=0):
        self.wrapped = wrapped

        self.shift = shift
