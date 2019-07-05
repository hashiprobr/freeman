import networkx

from math import isclose

from .exploring import extract_nodes


LAYOUTS = {
    'bipartite': networkx.bipartite_layout,
    'circular': networkx.circular_layout,
    'kamada_kawai': networkx.kamada_kawai_layout,
    'planar': networkx.planar_layout,
    'random': networkx.random_layout,
    'shell': networkx.shell_layout,
    'spring': networkx.spring_layout,
    'spectral': networkx.spectral_layout,
}


def normalize(g):
    if g.number_of_nodes() == 0:
        return

    xs = []
    ys = []
    for n in g.nodes:
        pos = g.nodes[n]['pos']
        xs.append(pos[0])
        ys.append(pos[1])

    xmin = min(xs)
    xmax = max(xs) - xmin
    ymin = min(ys)
    ymax = max(ys) - ymin

    for n in g.nodes:
        pos = g.nodes[n]['pos']
        x = 0.5 if isclose(xmax, 0) else (pos[0] - xmin) / xmax
        y = 0.5 if isclose(ymax, 0) else (pos[1] - ymin) / ymax
        g.nodes[n]['pos'] = (x, y)


def scatter(g, xkey, ykey):
    xs = extract_nodes(g, xkey)
    ys = extract_nodes(g, ykey)

    for n, x, y in zip(g.nodes, xs, ys):
        if not isinstance(x, int) and not isinstance(x, float):
            raise TypeError('non-numeric x in node ' + str(n))
        if not isinstance(y, int) and not isinstance(y, float):
            raise TypeError('non-numeric y in node ' + str(n))

        g.nodes[n]['pos'] = (x, y)

    normalize(g)


def move(g, key='random', *args, **kwargs):
    try:
        layout = LAYOUTS[key]
    except KeyError:
        raise KeyError('layout key must be one of the following: ' + ', '.join(['"{}"'.format(k) for k in LAYOUTS]))

    after = layout(g, *args, **kwargs)

    for n, pos in after.items():
        g.nodes[n]['pos'] = (pos[0], pos[1])

    normalize(g)


def attract(g, weight='weight', iterations=50, ego=None):
    before = networkx.get_node_attributes(g, 'pos')

    fixed = None if ego is None else [ego]

    move(g, key='spring', pos=before, fixed=fixed, iterations=iterations, weight=weight)


def attract_inverse(g, weight, iterations=50):
    h = g.copy()
    for n, m in h.edges:
        if weight in g.edges:
            h.edges[n, m][weight] = 1 / g.edges[n, m][weight]

    attract(h, weight, iterations=iterations)
    for n in g.nodes:
        g.nodes[n]['pos'] = h.nodes[n]['pos']


def attract_negative(g, weight, iterations=50):
    h = g.copy()
    for n, m in h.edges:
        if weight in g.edges:
            h.edges[n, m][weight] = -g.edges[n, m][weight]

    attract(h, weight, iterations=iterations)
    for n in g.nodes:
        g.nodes[n]['pos'] = h.nodes[n]['pos']


def attract_complement(g, iterations=50):
    h = networkx.complement(g)
    for n in h.nodes:
        h.nodes[n]['pos'] = g.nodes[n]['pos']

    attract(h, iterations=iterations)
    for n in g.nodes:
        g.nodes[n]['pos'] = h.nodes[n]['pos']


def movement(g, h):
    num_nodes = g.number_of_nodes()
    if num_nodes != h.number_of_nodes():
        raise ValueError('the graphs must have the same number of nodes')

    u = networkx.DiGraph()

    for n, (n1, n2) in enumerate(zip(g.nodes, h.nodes)):
        m = n + num_nodes
        u.add_node(n)
        u.nodes[n].update(g.nodes[n1])
        u.add_node(m)
        u.nodes[m].update(h.nodes[n2])
        u.add_edge(n, m)

    return u
