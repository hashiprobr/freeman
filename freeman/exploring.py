from math import isclose


def extract_node(g, n, key):
    if isinstance(key, str):
        return g.nodes[n][key]
    if isinstance(key, dict):
        return key[n]
    if callable(key):
        return key(n)
    return TypeError('key must be a string, a dictionary, or a callable')


def extract_edge(g, n, m, key):
    if isinstance(key, str):
        return g.edges[n, m][key]
    if isinstance(key, dict):
        return key[n, m]
    if callable(key):
        return key(n, m)
    return TypeError('key must be a string, a dictionary, or a callable')


def extract_nodes(g, key, filter=None):
    for n in g.nodes:
        if filter is None or filter(n):
            yield extract_node(g, n, key)


def extract_edges(g, key, filter=None):
    for n, m in g.edges:
        if filter is None or filter(n, m):
            yield extract_edge(g, n, m, key)


def scale_nodes(g, key, vlim=None, slim=(5, 50)):
    vs = []
    for n in g.nodes:
        value = extract_node(g, n, key)
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('node scale value must be numeric')
        vs.append(value)

    if vlim is None:
        vlim = (min(vs), max(vs))
    else:
        if not isinstance(vlim, tuple):
            raise TypeError('node scale vlim must be a tuple')
        if len(vlim) != 2:
            raise ValueError('node scale vlim must have exactly two elements')
        if (not isinstance(vlim[0], int) and not isinstance(vlim[0], float)) or (not isinstance(vlim[1], int) and not isinstance(vlim[1], float)):
            raise TypeError('both node scale vlim elements must be numeric')
        if vlim[0] > vlim[1]:
            raise ValueError('node scale vlim minimum must be smaller than maximum')
    if isclose(vlim[0], vlim[1]):
        raise ValueError('node scale vlim minimum and maximum are too close')

    if not isinstance(slim, tuple):
        raise TypeError('node scale slim must be a tuple')
    if len(slim) != 2:
        raise ValueError('node scale slim must have exactly two elements')
    if not isinstance(slim[0], int) or not isinstance(slim[1], int):
        raise TypeError('both node scale slim elements must be integers')
    if slim[0] > slim[1]:
        raise ValueError('node scale slim minimum must be smaller than maximum')
    if isclose(slim[0], slim[1]):
        raise ValueError('node scale slim minimum and maximum are too close')

    for n, value in zip(g.nodes, vs):
        scale = (value - vlim[0]) / (vlim[1] - vlim[0])
        g.nodes[n]['size'] = round(scale * (slim[1] - slim[0]) + slim[0])


def scale_edges(g, key, vlim=None, slim=(1, 10)):
    vs = []
    for n, m in g.edges:
        value = extract_edge(g, n, m, key)
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('edge scale value must be numeric')
        vs.append(value)

    if vlim is None:
        vlim = (min(vs), max(vs))
    else:
        if not isinstance(vlim, tuple):
            raise TypeError('edge scale vlim must be a tuple')
        if len(vlim) != 2:
            raise ValueError('edge scale vlim must have exactly two elements')
        if (not isinstance(vlim[0], int) and not isinstance(vlim[0], float)) or (not isinstance(vlim[1], int) and not isinstance(vlim[1], float)):
            raise TypeError('both edge scale vlim elements must be numeric')
        if vlim[0] > vlim[1]:
            raise ValueError('edge scale vlim minimum must be smaller than maximum')
    if isclose(vlim[0], vlim[1]):
        raise ValueError('edge scale vlim minimum and maximum are too close')

    if not isinstance(slim, tuple):
        raise TypeError('edge scale slim must be a tuple')
    if len(slim) != 2:
        raise ValueError('edge scale slim must have exactly two elements')
    if not isinstance(slim[0], int) or not isinstance(slim[1], int):
        raise TypeError('both edge scale slim elements must be integers')
    if slim[0] > slim[1]:
        raise ValueError('edge scale slim minimum must be smaller than maximum')
    if isclose(slim[0], slim[1]):
        raise ValueError('edge scale slim minimum and maximum are too close')

    for (n, m), value in zip(g.edges, vs):
        scale = (value - vlim[0]) / (vlim[1] - vlim[0])
        g.edges[n, m]['width'] = round(scale * (slim[1] - slim[0]) + slim[0])
