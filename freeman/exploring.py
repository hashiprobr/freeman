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
            raise TypeError('scale value must be numeric')
        vs.append(value)

    if vlim is None:
        vlim = (min(vs), max(vs))
    else:
        if not isinstance(vlim, tuple):
            raise TypeError('scale vlim must be a tuple')
        if len(vlim) != 2:
            raise ValueError('scale vlim must have exactly two elements')
        if (not isinstance(vlim[0], int) and not isinstance(vlim[0], float)) or (not isinstance(vlim[1], int) and not isinstance(vlim[1], float)):
            raise TypeError('both scale vlim elements must be numeric')
    if vlim[0] >= vlim[1]:
        raise TypeError('scale vlim minimum must be smaller than maximum')

    if not isinstance(slim, tuple):
        raise TypeError('scale slim must be a tuple')
    if len(slim) != 2:
        raise ValueError('scale slim must have exactly two elements')
    if not isinstance(slim[0], int) or not isinstance(slim[1], int):
        raise TypeError('both scale slim elements must be integers')
    if slim[0] >= slim[1]:
        raise TypeError('scale slim minimum must be smaller than maximum')

    for n, value in zip(g.nodes, vs):
        size = (value - vlim[0]) / (vlim[1] - vlim[0])
        g.nodes[n]['size'] = int(size * (slim[1] - slim[0]) + slim[0])
