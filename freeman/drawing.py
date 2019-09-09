import os
import plotly

import networkx as nx

from math import isclose, sqrt, cos, sin
from IPython.display import display
from networkx import NetworkXError
from pyvis.network import Network


CACHE_DIR = '__fmcache__'

NODE_STYLES = {
    'circle': 'dot',
    'star': 'star',
    'square': 'square',
    'diamond': 'diamond',
    'triangle-up': 'triangle',
    'triangle-down': 'triangleDown',
}

EDGE_SCALE = 0.4
EDGE_SPACE = 5
EDGE_SIZE = 10
EDGE_ANGLE = 0.3

EDGE_STYLES = {
    'solid': False,
    'dot': [3, 3],
    'dash': [10, 8],
    'dashdot': [10, 3, 2, 3],
}


graph_width = 800
graph_height = 450
graph_bottom = 0
graph_left = 0
graph_right = 0
graph_top = 0

node_size = 20
node_style = 'circle'
node_border = True
node_color = (255, 255, 255)
node_labpos = 'middle center'

edge_width = 1
edge_style = 'solid'
edge_color = (0, 0, 0)
edge_labflip = False
edge_labdist = 10
edge_labfrac = 0.5


def _scale(dx, dy, width, height, size):
    d = (dx * width)**2 + (dy * height)**2

    if isclose(d, 0):
        return dx, dy

    s = sqrt(size**2 / d)

    return s * dx, s * dy


def _rotate(dx, dy, width, height, angle):
    dx *= width
    dy *= height

    rx = dx * cos(angle) - dy * sin(angle)
    ry = dx * sin(angle) + dy * cos(angle)

    return rx / width, ry / height


def _correct(c):
    sc = c / 255

    if sc > 0.03928:
        return ((sc + 0.055) / 1.055)**2.4

    return sc / 12.92


def _convert(color):
    r = color[0]
    g = color[1]
    b = color[2]

    if len(color) == 4:
        a = color[3]

        return 'rgba({}, {}, {}, {})'.format(r, g, b, a)

    return 'rgb({}, {}, {})'.format(r, g, b)


def _build_graph_key(g):
    width = g.graph['width'] if 'width' in g.graph else graph_width
    if not isinstance(width, int):
        raise TypeError('graph width must be an integer')
    if width <= 0:
        raise ValueError('graph width must be positive')

    height = g.graph['height'] if 'height' in g.graph else graph_height
    if not isinstance(height, int):
        raise TypeError('graph height must be an integer')
    if height <= 0:
        raise ValueError('graph height must be positive')

    bottom = g.graph['bottom'] if 'bottom' in g.graph else graph_bottom
    if not isinstance(bottom, int):
        raise TypeError('graph bottom must be an integer')
    if bottom < 0:
        raise ValueError('graph bottom must be non-negative')

    left = g.graph['left'] if 'left' in g.graph else graph_left
    if not isinstance(left, int):
        raise TypeError('graph left must be an integer')
    if left < 0:
        raise ValueError('graph left must be non-negative')

    right = g.graph['right'] if 'right' in g.graph else graph_right
    if not isinstance(right, int):
        raise TypeError('graph right must be an integer')
    if right < 0:
        raise ValueError('graph right must be non-negative')

    top = g.graph['top'] if 'top' in g.graph else graph_top
    if not isinstance(top, int):
        raise TypeError('graph top must be an integer')
    if top < 0:
        raise ValueError('graph top must be non-negative')

    return width, height, bottom, left, right, top


def _build_node_key(g, n):
    size = g.nodes[n]['size'] if 'size' in g.nodes[n] else node_size
    if not isinstance(size, int):
        raise TypeError('node size must be an integer')
    if size <= 0:
        raise ValueError('node size must be positive')

    style = g.nodes[n]['style'] if 'style' in g.nodes[n] else node_style
    if style not in NODE_STYLES:
        raise ValueError('node style must be one of the following: ' + ', '.join('"{}"'.format(s) for s in NODE_STYLES))

    border = g.nodes[n]['border'] if 'border' in g.nodes[n] else node_border
    if not isinstance(border, bool):
        raise TypeError('node border must be a boolean')

    color = g.nodes[n]['color'] if 'color' in g.nodes[n] else node_color
    if not isinstance(color, tuple):
        raise TypeError('node color must be a tuple')
    if len(color) != 3:
        raise ValueError('node color must have exactly three elements')
    if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
        raise TypeError('all node color elements must be integers')
    if color[0] < 0 or color[0] > 255 or color[1] < 0 or color[1] > 255 or color[2] < 0 or color[2] > 255:
        raise ValueError('all node color elements must be between 0 and 255')

    labpos = g.nodes[n]['labpos'] if 'labpos' in g.nodes[n] else node_labpos
    if not isinstance(labpos, str):
        raise TypeError('node labpos must be a string')
    if labpos != 'hover':
        words = labpos.split(' ')
        if len(words) != 2:
            raise TypeError('node labpos must be "hover" or a vertical position and an horizontal position separated by a space')
        vpos = ['bottom', 'middle', 'top']
        if words[0] not in vpos:
            raise ValueError('node vertical position must be one of the following: ' + ', '.join('"{}"'.format(v) for v in vpos))
        hpos = ['left', 'center', 'right']
        if words[1] not in hpos:
            raise ValueError('node horizontal position must be one of the following: ' + ', '.join('"{}"'.format(h) for h in hpos))

    return size, style, border, color, labpos


def _build_edge_key(g, n, m):
    n_size = g.nodes[n]['size'] if 'size' in g.nodes[n] else node_size
    m_size = g.nodes[m]['size'] if 'size' in g.nodes[m] else node_size

    width = g.edges[n, m]['width'] if 'width' in g.edges[n, m] else edge_width
    if not isinstance(width, int):
        raise TypeError('edge width must be an integer')
    if width <= 0:
        raise ValueError('edge width must be positive')

    style = g.edges[n, m]['style'] if 'style' in g.edges[n, m] else edge_style
    if style not in EDGE_STYLES:
        raise ValueError('edge style must be one of the following: ' + ', '.join('"{}"'.format(s) for s in EDGE_STYLES))

    color = g.edges[n, m]['color'] if 'color' in g.edges[n, m] else edge_color
    if not isinstance(color, tuple):
        raise TypeError('edge color must be a tuple')
    if len(color) != 3 and len(color) != 4:
        raise ValueError('edge color must have three or four elements')
    if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
        raise TypeError('the first three edge color elements must be integers')
    if len(color) == 4 and not isinstance(color[3], float):
        raise TypeError('the fourth edge color element must be a float')
    if color[0] < 0 or color[0] > 255 or color[1] < 0 or color[1] > 255 or color[2] < 0 or color[2] > 255:
        raise ValueError('the first three edge color elements must be between 0 and 255')
    if len(color) == 4 and (color[3] < 0 or color[3] > 1):
        raise ValueError('the fourth edge color element must be between 0 and 1')

    labflip = g.edges[n, m]['labflip'] if 'labflip' in g.edges[n, m] else edge_labflip
    if not isinstance(labflip, bool):
        raise TypeError('edge labflip must be a boolean')

    labdist = g.edges[n, m]['labdist'] if 'labdist' in g.edges[n, m] else edge_labdist
    if not isinstance(labdist, int):
        raise TypeError('edge labdist must be an integer')
    if labdist < 0:
        raise ValueError('edge labdist must be non-negative')

    labfrac = g.edges[n, m]['labfrac'] if 'labfrac' in g.edges[n, m] else edge_labfrac
    if not isinstance(labfrac, float):
        raise TypeError('edge labfrac must be a float')
    if labfrac < 0 or labfrac > 1:
        raise ValueError('edge labfrac must be between 0 and 1')

    return n_size, m_size, width, style, color, labflip, labdist, labfrac


def _build_node_trace(size, style, border, color, labpos):
    if labpos == 'hover':
        hoverinfo = 'text'
        mode = 'markers'
    else:
        hoverinfo = 'none'
        mode = 'markers+text'

    fontcolor = (0, 0, 0)

    if labpos == 'middle center':
        r = _correct(color[0])
        g = _correct(color[1])
        b = _correct(color[2])

        if (0.2126 * r + 0.7152 * g + 0.0722 * b + 0.05)**2 < 0.0525:
            fontcolor = (255, 255, 255)

    return {
        'x': [],
        'y': [],
        'text': [],
        'textposition': 'middle center' if labpos == 'hover' else labpos,
        'hoverinfo': hoverinfo,
        'mode': mode,
        'marker': {
            'size': size,
            'symbol': style,
            'color': _convert(color),
            'line': {
                'width': int(border),
                'color': 'rgb(0, 0, 0)',
            },
        },
        'textfont': {
            'color': _convert(fontcolor),
        },
    }


def _build_node_label_trace(width, height, bottom, left, right, top):
    return {
        'x': [0.5, -left / width, 1 + right / width, 0.5],
        'y': [-bottom / height, 0.5, 0.5, 1 + top / height],
        'hoverinfo': 'none',
        'mode': 'markers',
        'marker': {
            'size': 0,
            'color': 'rgba(255, 255, 255, 0.0)',
            'line': {
                'width': 0,
                'color': 'rgba(255, 255, 255, 0.0)',
            },
        },
    }


def _build_edge_trace(width, style, color):
    return {
        'x': [],
        'y': [],
        'hoverinfo': 'none',
        'mode': 'lines',
        'line': {
            'width': width,
            'dash': style,
            'color': _convert(color),
        },
    }


def _build_edge_label_trace():
    return {
        'x': [],
        'y': [],
        'text': [],
        'textposition': 'middle center',
        'hoverinfo': 'none',
        'mode': 'text',
        'textfont': {
            'color': 'rgb(0, 0, 0)',
        },
    }


def _build_layout(width, height):
    return {
        'showlegend': False,
        'width': width,
        'height': height,
        'margin': {
            'b': 0,
            'l': 0,
            'r': 0,
            't': 0,
        },
        'xaxis': {
            'showgrid': False,
            'zeroline': False,
            'showticklabels': False,
        },
        'yaxis': {
            'showgrid': False,
            'zeroline': False,
            'showticklabels': False,
        },
    }


def _add_node(g, n, node_trace):
    x, y = g.nodes[n]['pos']
    text = g.nodes[n]['label'] if 'label' in g.nodes[n] else None

    node_trace['x'].append(x)
    node_trace['y'].append(y)
    node_trace['text'].append(text)


def _add_edge(g, n, m, edge_trace, edge_label_trace, width, height, n_size, m_size, nm_width, labflip, labdist, labfrac):
    x0, y0 = g.nodes[n]['pos']
    x1, y1 = g.nodes[m]['pos']

    # parameters estimated from screenshots
    width = 0.9 * width - 24
    height = 0.9 * height - 24

    ratio = width / height
    dx = (y0 - y1) / ratio
    dy = (x1 - x0) * ratio

    if isinstance(g, nx.DiGraph) and g.has_edge(m, n):
        edge_space = max(0, min(EDGE_SPACE, n_size - 2, m_size - 2))
        sx, sy = _scale(dx, dy, width, height, edge_space / 2)
        x0 += sx
        y0 += sy
        x1 += sx
        y1 += sy

    edge_trace['x'].extend([x0, x1, None])
    edge_trace['y'].extend([y0, y1, None])

    if labflip:
        dx = -dx
        dy = -dy
    sx, sy = _scale(dx, dy, width, height, labdist + nm_width / 2)
    edge_label_trace['x'].append(x0 + labfrac * (x1 - x0) + sx)
    edge_label_trace['y'].append(y0 + labfrac * (y1 - y0) + sy)
    edge_label_trace['text'].append(g.edges[n, m]['label'] if 'label' in g.edges[n, m] else None)

    if isinstance(g, nx.DiGraph):
        dx = x0 - x1
        dy = y0 - y1

        radius = m_size / 2
        sx, sy = _scale(dx, dy, width, height, radius)
        x0 = x1 + sx
        y0 = y1 + sy
        edge_size = max(1, min(EDGE_SIZE, m_size))
        sx, sy = _scale(dx, dy, width, height, edge_size)

        rx, ry = _rotate(sx, sy, width, height, -EDGE_ANGLE)
        x1 = x0 + rx
        y1 = y0 + ry
        edge_trace['x'].extend([x0, x1, None])
        edge_trace['y'].extend([y0, y1, None])

        if not g.has_edge(m, n):
            rx, ry = _rotate(sx, sy, width, height, EDGE_ANGLE)
            x1 = x0 + rx
            y1 = y0 + ry
            edge_trace['x'].extend([x0, x1, None])
            edge_trace['y'].extend([y0, y1, None])


def interact(g, path=None, physics=False):
    local_width, local_height, local_bottom, local_left, local_right, local_top = _build_graph_key(g)
    dx = local_left + local_right
    dy = local_bottom + local_top
    network = Network(
        height='{}px'.format(local_height + dy),
        width='{}px'.format(local_width + dx),
        directed=isinstance(g, nx.DiGraph),
        notebook=True,
        bgcolor='#ffffff',
        font_color='#000000',
        layout=None,
    )

    dx = local_left - dx // 2
    dy = local_top - dy // 2
    for n in g.nodes:
        border_color = 'rgb(0, 0, 0)'
        size, style, border, color, _ = _build_node_key(g, n)
        options = {
            'borderWidth': int(border),
            'borderWidthSelected': 1,
            'color': {
                'border': border_color,
                'background': _convert(color),
                'highlight': {
                    'border': border_color,
                    'background': _convert(color),
                },
                'hover': {
                    'border': border_color,
                    'background': _convert(color),
                },
            },
            'label': ' ',
            'labelHighlightBold': False,
            'physics': physics,
            'shape': NODE_STYLES[style],
            'size': size // 2,
            'x': round((g.nodes[n]['pos'][0] - 0.5) * (0.9 * local_width - 24)) + dx,
            'y': round((0.5 - g.nodes[n]['pos'][1]) * (0.9 * local_height - 24)) + dy,
        }
        label = g.nodes[n]['label'] if 'label' in g.nodes[n] else None
        if label:
            options['title'] = label
        network.add_node(n, **options)

    for n, m in g.edges:
        if n != m:
            _, _, width, style, color, _, _, _ = _build_edge_key(g, n, m)
            options = {
                'color': {
                    'color': _convert(color),
                    'highlight': _convert(color),
                    'hover': _convert(color),
                },
                'dashes': EDGE_STYLES[style],
                'labelHighlightBold': False,
                'selectionWidth': 0,
                'width': width,
            }
            label = g.edges[n, m]['label'] if 'label' in g.edges[n, m] else None
            if label:
                options['title'] = label
            network.add_edge(n, m, **options)
            if network.directed:
                network.edges[-1]['arrows'] = {
                    'to': {
                        'scaleFactor': EDGE_SCALE,
                    },
                }

    if path is None:
        if not os.path.exists(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        path = os.path.join(CACHE_DIR, '{}.html'.format(id(g)))

    iframe = network.show(path)

    display(iframe)


def draw(g, toolbar=False):
    local_width, local_height, local_bottom, local_left, local_right, local_top = _build_graph_key(g)
    local_width += local_left + local_right
    local_height += local_bottom + local_top

    node_traces = {}
    node_label_trace = _build_node_label_trace(local_width, local_height, local_bottom, local_left, local_right, local_top)
    for n in g.nodes:
        size, style, border, color, labpos = _build_node_key(g, n)
        key = (size, style, border, color, labpos)
        if key not in node_traces:
            node_traces[key] = _build_node_trace(size, style, border, color, labpos)
        _add_node(g, n, node_traces[key])

    edge_traces = {}
    edge_label_trace = _build_edge_label_trace()
    for n, m in g.edges:
        if n != m:
            n_size, m_size, width, style, color, labflip, labdist, labfrac = _build_edge_key(g, n, m)
            key = (width, style, color)
            if key not in edge_traces:
                edge_traces[key] = _build_edge_trace(width, style, color)
            _add_edge(g, n, m, edge_traces[key], edge_label_trace, local_width, local_height, n_size, m_size, width, labflip, labdist, labfrac)

    data = list(edge_traces.values())
    data.extend(node_traces.values())
    data.append(edge_label_trace)
    data.append(node_label_trace)

    layout = _build_layout(local_width, local_height)
    if isinstance(g, nx.DiGraph):
        layout['xaxis']['fixedrange'] = True
        layout['yaxis']['fixedrange'] = True

    figure = {
        'data': data,
        'layout': layout,
    }

    plotly.offline.iplot(figure, config={'displayModeBar': toolbar}, show_link=False)


class Animation:
    def __init__(self):
        self.graphs = []

    def __enter__(self):
        self.erase()
        return self

    def __exit__(self, type, value, traceback):
        self.play()

    def erase(self):
        self.graphs.clear()

    def rec(self, g):
        self.graphs.append(g.copy())

    def render(self, g, h, local_width, local_height):
        _, _, local_bottom, local_left, local_right, local_top = _build_graph_key(g)
        local_width += local_left + local_right
        local_height += local_bottom + local_top

        node_traces = []
        node_label_trace = _build_node_label_trace(local_width, local_height, local_bottom, local_left, local_right, local_top)
        for n in h.nodes:
            if g.has_node(n):
                size, style, border, color, labpos = _build_node_key(g, n)
                node_trace = _build_node_trace(size, style, border, color, labpos)
                _add_node(g, n, node_trace)
            else:
                size, style, _, _, labpos = _build_node_key(h, n)
                node_trace = _build_node_trace(size, style, False, (255, 255, 255, 0.0), labpos)
                _add_node(h, n, node_trace)
            node_traces.append(node_trace)

        edge_traces = []
        edge_label_trace = _build_edge_label_trace()
        for n, m in h.edges:
            if n != m:
                if g.has_edge(n, m):
                    n_size, m_size, width, style, color, labflip, labdist, labfrac = _build_edge_key(g, n, m)
                    edge_trace = _build_edge_trace(width, style, color)
                    _add_edge(g, n, m, edge_trace, edge_label_trace, local_width, local_height, n_size, m_size, width, labflip, labdist, labfrac)
                else:
                    n_size, m_size, width, style, _, labflip, labdist, labfrac = _build_edge_key(h, n, m)
                    edge_trace = _build_edge_trace(width, style, (255, 255, 255, 0.0))
                    _add_edge(h, n, m, edge_trace, edge_label_trace, local_width, local_height, n_size, m_size, width, labflip, labdist, labfrac)
                edge_traces.append(edge_trace)

        data = edge_traces
        data.extend(node_traces)
        data.append(edge_label_trace)
        data.append(node_label_trace)

        frame = {
            'data': data,
        }

        return frame

    def play(self, width=None, height=None):
        if width is None:
            width = graph_width
        if not isinstance(width, int):
            raise TypeError('animation width must be an integer')
        if width <= 0:
            raise ValueError('animation width must be positive')

        if height is None:
            height = graph_height
        if not isinstance(height, int):
            raise TypeError('animation height must be an integer')
        if height <= 0:
            raise ValueError('animation height must be positive')

        if len(self.graphs) < 2:
            raise NetworkXError('animation must have at least two graphs')

        last = self.graphs[-1]
        number_of_nodes = last.number_of_nodes()
        number_of_edges = last.number_of_edges()

        h = False

        for g in self.graphs[:-1]:
            if g.number_of_nodes() != number_of_nodes or g.number_of_edges() != number_of_edges:
                h = True

        h = nx.compose_all(self.graphs) if h else None

        frames = []

        for i, g in enumerate(self.graphs):
            if h is None:
                frames.append(self.render(g, g, width, height))
            else:
                if g != last:
                    next = self.graphs[i + 1]
                    for n in next.nodes:
                        h.nodes[n].update(next.nodes[n])
                    for n, m in next.edges:
                        h.edges[n, m].update(next.edges[n, m])

                frames.append(self.render(g, h, width, height))

        steps = []

        for index, frame in enumerate(frames):
            frame['name'] = index

            step = {
                'args': [[index], {'frame': {'redraw': False}, 'mode': 'immediate'}],
                'label': '',
                'method': 'animate',
            }

            steps.append(step)

        # parameters estimated from screenshots
        width = 1.05 * width + 72
        height = 1.00 * height + 76

        layout = _build_layout(width, height)
        layout.update({
            'updatemenus': [
                {
                    'buttons': [
                        {
                            'args': [None, {'frame': {'redraw': False}, 'fromcurrent': True}],
                            'label': 'Play',
                            'method': 'animate',
                        },
                        {
                            'args': [[None], {'frame': {'redraw': False}, 'mode': 'immediate'}],
                            'label': 'Pause',
                            'method': 'animate',
                        },
                    ],
                    'showactive': True,
                    'type': 'buttons',
                },
            ],
            'sliders': [
                {
                    'currentvalue': {'visible': False},
                    'steps': steps,
                },
            ],
        })

        figure = {
            'data': frames[0]['data'],
            'layout': layout,
            'frames': frames,
        }

        plotly.offline.iplot(figure, config={'staticPlot': True}, show_link=False)


plotly.offline.init_notebook_mode(connected=True)
