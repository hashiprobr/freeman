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
