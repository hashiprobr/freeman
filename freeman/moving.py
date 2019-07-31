import networkx

from math import isclose

from .exploring import assert_numeric, extract_node


def step_layout(g, ego=None, iterations=1, weight='weight'):
    before = networkx.get_node_attributes(g, 'pos')

    fixed = None if ego is None else [ego]

    return networkx.spring_layout(g, pos=before, fixed=fixed, iterations=iterations, weight=weight)


LAYOUTS = {
    'bipartite': networkx.bipartite_layout,
    'circular': networkx.circular_layout,
    'kamada_kawai': networkx.kamada_kawai_layout,
    'planar': networkx.planar_layout,
    'random': networkx.random_layout,
    'shell': networkx.shell_layout,
    'spring': networkx.spring_layout,
    'spectral': networkx.spectral_layout,
    'step': step_layout,
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


def scatter(g, xmap, ymap):
    for n in g.nodes:
        x = assert_numeric(extract_node(g, n, xmap))
        y = assert_numeric(extract_node(g, n, ymap))
        g.nodes[n]['pos'] = (x, y)

    normalize(g)


def move(g, key, *args, **kwargs):
    try:
        layout = LAYOUTS[key]
    except KeyError:
        raise KeyError('layout key must be one of the following: ' + ', '.join(['"{}"'.format(k) for k in LAYOUTS]))

    after = layout(g, *args, **kwargs)

    for n, pos in after.items():
        g.nodes[n]['pos'] = (pos[0], pos[1])

    normalize(g)


def move_copy(g, h, key, *args, **kwargs):
    move(h, key, *args, **kwargs)

    for n in g.nodes:
        g.nodes[n]['pos'] = h.nodes[n]['pos']


def move_inverse(g, key, weight, *args, **kwargs):
    h = g.copy()
    for n, m in h.edges:
        if weight in g.edges[n, m]:
            h.edges[n, m][weight] = 1 / g.edges[n, m][weight]

    move_copy(g, h, key, *args, weight=weight, **kwargs)


def move_negative(g, key, weight, *args, **kwargs):
    h = g.copy()
    for n, m in h.edges:
        if weight in g.edges[n, m]:
            h.edges[n, m][weight] = -g.edges[n, m][weight]

    move_copy(g, h, key, *args, weight=weight, **kwargs)


def move_complement(g, key, *args, **kwargs):
    h = networkx.complement(g)
    for n in h.nodes:
        h.nodes[n].update(g.nodes[n])

    move_copy(g, h, key, *args, **kwargs)


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
