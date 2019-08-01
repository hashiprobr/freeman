from math import isclose, isinf
from statistics import mean
from colorsys import hsv_to_rgb


def _stringify(value, ndigits):
    if isinstance(value, float):
        if isinf(value):
            return '∞'

        value = round(value, ndigits)

    return str(value)


def _transform(h, s, v):
    sr, sg, sb = hsv_to_rgb(h, s, v)

    return round(sr * 255), round(sg * 255), round(sb * 255)


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


def _assert_color(component):
    if not isinstance(component, int) and not isinstance(component, float):
        raise TypeError('component must be numeric')
    if component < 0 or component > 1:
        raise ValueError('component must be between 0 and 1')


def _assert_reference(values, lower, upper, middle):
    if middle is None:
        middle = mean(values)
    else:
        middle = assert_numeric(middle)
        if middle < lower or middle > upper:
            raise ValueError('middle must be between lower and upper')

    return middle


def assert_numeric(value):
    if not isinstance(value, int) and not isinstance(value, float):
        raise TypeError('value must be numeric')
    return value


def assert_numerics(values):
    for value in values:
        yield assert_numeric(value)


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


def extract_nodes(g, map, filter=None):
    for n in g.nodes:
        if filter is None or filter(n):
            yield extract_node(g, n, map)


def extract_edges(g, map, filter=None):
    for n, m in g.edges:
        if filter is None or filter(n, m):
            yield extract_edge(g, n, m, map)


def label_nodes(g, map=None, ndigits=2):
    for n in g.nodes:
        if map is None:
            g.nodes[n]['label'] = str(n)
        else:
            value = extract_node(g, n, map)

            g.nodes[n]['label'] = _stringify(value, ndigits)


def label_edges(g, map=None, ndigits=2):
    for n, m in g.edges:
        if map is None:
            g.edges[n, m]['label'] = '({}, {})'.format(n, m)
        else:
            value = extract_edge(g, n, m, map)

            g.edges[n, m]['label'] = _stringify(value, ndigits)


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
        color = _transform(h, 1, 1)
        for n in group:
            g.nodes[n]['color'] = color
        h += s


def colorize_edges(g, map=None):
    if map is None:
        groups = [[(n, m)] for n, m in g.edges]
    else:
        groups = {}
        for n, m in g.edges:
            value = extract_edge(g, n, m, map)
            if value in groups:
                groups[value].append((n, m))
            else:
                groups[value] = [(n, m)]
        groups = groups.values()

    h = 0
    s = 1 / len(groups)
    for group in groups:
        color = _transform(h, 1, 1)
        for n, m in group:
            g.edges[n, m]['color'] = color
        h += s


def scale_nodes_size(g, map, lower=None, upper=None):
    values, lower, upper = _assert_limits(extract_nodes(g, map), lower, upper)

    for n, value in zip(g.nodes, values):
        if isclose(lower, upper):
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        g.nodes[n]['size'] = 5 + round(sc * 45)


def scale_edges_width(g, map, lower=None, upper=None):
    values, lower, upper = _assert_limits(extract_edges(g, map), lower, upper)

    for (n, m), value in zip(g.edges, values):
        if isclose(lower, upper):
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        g.edges[n, m]['width'] = 1 + round(sc * 9)


def scale_nodes_alpha(g, map, lower=None, upper=None, hue=None):
    values, lower, upper = _assert_limits(extract_nodes(g, map), lower, upper)

    for n, value in zip(g.nodes, values):
        if isclose(lower, upper):
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        if hue is None:
            c = 255 - round(sc * 255)
            g.nodes[n]['color'] = (c, c, c)
        else:
            _assert_color(hue)
            g.nodes[n]['color'] = _transform(hue, sc, 1)


def scale_edges_alpha(g, map, lower=None, upper=None, hue=None):
    values, lower, upper = _assert_limits(extract_edges(g, map), lower, upper)

    for (n, m), value in zip(g.edges, values):
        if isclose(lower, upper):
            sc = 0.5
        else:
            sc = (value - lower) / (upper - lower)

        if hue is None:
            g.edges[n, m]['color'] = (0, 0, 0, sc)
        else:
            _assert_color(hue)
            sr, sg, sb = _transform(hue, 1, 1)
            g.edges[n, m]['color'] = (sr, sg, sb, sc)


def heat_nodes(g, map, lower=None, upper=None, middle=None):
    values, lower, upper = _assert_limits(extract_nodes(g, map), lower, upper)

    middle = _assert_reference(values, lower, upper, middle)

    for n, value in zip(g.nodes, values):
        if isclose(lower, upper):
            g.nodes[n]['color'] = (255, 255, 255)
        else:
            if value < middle:
                sc = (value - lower) / (middle - lower)
                c = round(sc * 255)
                g.nodes[n]['color'] = (c, c, 255)
            else:
                sc = (value - middle) / (upper - middle)
                c = 255 - round(sc * 255)
                g.nodes[n]['color'] = (255, c, c)


def heat_edges(g, map, lower=None, upper=None, middle=None):
    values, lower, upper = _assert_limits(extract_edges(g, map), lower, upper)

    middle = _assert_reference(values, lower, upper, middle)

    for (n, m), value in zip(g.edges, values):
        if isclose(lower, upper):
            g.edges[n, m]['color'] = (255, 255, 255)
        else:
            if value < middle:
                sc = (value - lower) / (middle - lower)
                g.edges[n, m]['color'] = (0, 0, 255, 1 - sc)
            else:
                sc = (value - middle) / (upper - middle)
                g.edges[n, m]['color'] = (255, 0, 0, sc)
