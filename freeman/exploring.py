from math import isclose
from statistics import mean
from colorsys import hsv_to_rgb


def assert_numeric(value):
    if not isinstance(value, int) and not isinstance(value, float):
        raise TypeError('value must be numeric')
    return value


def extract_node(g, n, map):
    if isinstance(map, str):
        return g.nodes[n][map]
    if isinstance(map, dict):
        return map[n]
    if callable(map):
        return map(n)
    raise TypeError('map must be a string, a dictionary, or a callable')


def extract_edge(g, n, m, map):
    if isinstance(map, str):
        return g.edges[n, m][map]
    if isinstance(map, dict):
        return map[n, m]
    if callable(map):
        return map(n, m)
    raise TypeError('map must be a string, a dictionary, or a callable')


def assert_numerics(values):
    for value in values:
        yield assert_numeric(value)


def extract_nodes(g, map, filter=None):
    for n in g.nodes:
        if filter is None or filter(n):
            yield extract_node(g, n, map)


def extract_edges(g, map, filter=None):
    for n, m in g.edges:
        if filter is None or filter(n, m):
            yield extract_edge(g, n, m, map)


def colorize_nodes(g, map=None):
    if map is None:
        groups = [[n] for n in g.nodes]
    else:
        groups = {}
        for n in g.nodes:
            value = extract_node(g, n, map)
            if value in groups:
                groups[value].append(n)
            else:
                groups[value] = [n]
        groups = groups.values()

    h = 0
    s = 1 / len(groups)
    for group in groups:
        sr, sg, sb = hsv_to_rgb(h, 1, 1)
        color = (round(sr * 255), round(sg * 255), round(sb * 255))
        for n in group:
            g.nodes[n]['color'] = color
        h += s


def _assert_limits(values, lower, upper):
    values = list(assert_numerics(values))

    if lower is None:
        lower = min(values)
    else:
        lower = assert_numeric(lower)
        if any(value < lower for value in values):
            raise ValueError('lower bound must be below all values')

    if upper is None:
        upper = max(values)
    else:
        upper = assert_numeric(upper)
        if any(value > upper for value in values):
            raise ValueError('upper bound must be above all values')

    return values, lower, upper


def scale_nodes_size(g, map=None, lower=None, upper=None):
    values, lower, upper = _assert_limits(extract_nodes(g, map), lower, upper)

    for n, value in zip(g.nodes, values):
        if lower == upper:
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        g.nodes[n]['size'] = 5 + round(sc * 45)


def scale_nodes_alpha(g, map=None, lower=None, upper=None, hue=None):
    values, lower, upper = _assert_limits(extract_nodes(g, map), lower, upper)

    for n, value in zip(g.nodes, values):
        if lower == upper:
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        if hue is None:
            c = 255 - round(sc * 255)
            g.nodes[n]['color'] = (c, c, c)
        else:
            if not isinstance(hue, int) and not isinstance(hue, float):
                raise TypeError('hue must be numeric')
            if hue < 0 or hue > 1:
                raise ValueError('hue must be between 0 and 1')

            sr, sg, sb = hsv_to_rgb(hue, sc, 1)
            g.nodes[n]['color'] = (round(sr * 255), round(sg * 255), round(sb * 255))
