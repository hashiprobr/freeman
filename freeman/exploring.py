def extract_nodes(g, key, filter=None):
    for n in g.nodes:
        if filter is None or filter(n):
            if isinstance(key, str):
                yield g.nodes[n][key]
            elif isinstance(key, dict):
                yield key[n]
            elif callable(key):
                yield key(n)
            else:
                raise TypeError('key must be a string, a dictionary, or a callable')


def extract_edges(g, key, filter=None):
    for n, m in g.edges:
        if filter is None or filter(n, m):
            if isinstance(key, str):
                yield g.edges[n, m][key]
            elif isinstance(key, dict):
                yield key[n, m]
            elif callable(key):
                yield key(n, m)
            else:
                raise TypeError('key must be a string, a dictionary, or a callable')
