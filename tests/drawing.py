import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..')))

import unittest

import networkx as nx
import freeman as fm


N = 'Medici'
M = 'Acciaiuoli'


class DrawingTest(unittest.TestCase):
    def with_position(self, g):
        g = g.copy()
        for n in g.nodes:
            g.nodes[n]['pos'] = (0.5, 0.5)
        return g

    def null_graph(self):
        return self.with_position(nx.Graph())
    def empty_graph(self):
        return self.with_position(nx.empty_graph(15))
    def partial_graph(self):
        return self.with_position(nx.florentine_families_graph())
    def wrapped_graph(self):
        return fm.Graph(nx.florentine_families_graph())
    def complete_graph(self):
        return self.with_position(nx.complete_graph(15))

    def null_digraph(self):
        return self.null_graph().to_directed()
    def empty_digraph(self):
        return self.empty_graph().to_directed()
    def partial_digraph(self):
        return self.partial_graph().to_directed()
    def wrapped_digraph(self):
        return self.wrapped_graph().to_directed()
    def complete_digraph(self):
        return self.complete_graph().to_directed()

    def test_interact_null_graph(self):
        fm.interact(self.null_graph())
    def test_interact_empty_graph(self):
        fm.interact(self.empty_graph())
    def test_interact_partial_graph(self):
        fm.interact(self.partial_graph())
    def test_interact_wrapped_graph(self):
        fm.interact(self.wrapped_graph())
    def test_interact_complete_graph(self):
        fm.interact(self.complete_graph())

    def test_interact_null_digraph(self):
        fm.interact(self.null_digraph())
    def test_interact_empty_digraph(self):
        fm.interact(self.empty_digraph())
    def test_interact_partial_digraph(self):
        fm.interact(self.partial_digraph())
    def test_interact_wrapped_digraph(self):
        fm.interact(self.wrapped_digraph())
    def test_interact_complete_digraph(self):
        fm.interact(self.complete_digraph())

    def test_draw_null_graph(self):
        fm.draw(self.null_graph())
    def test_draw_empty_graph(self):
        fm.draw(self.empty_graph())
    def test_draw_partial_graph(self):
        fm.draw(self.partial_graph())
    def test_draw_wrapped_graph(self):
        fm.draw(self.wrapped_graph())
    def test_draw_complete_graph(self):
        fm.draw(self.complete_graph())

    def test_draw_null_digraph(self):
        fm.draw(self.null_digraph())
    def test_draw_empty_digraph(self):
        fm.draw(self.empty_digraph())
    def test_draw_partial_digraph(self):
        fm.draw(self.partial_digraph())
    def test_draw_wrapped_digraph(self):
        fm.draw(self.wrapped_digraph())
    def test_draw_complete_digraph(self):
        fm.draw(self.complete_digraph())

    def with_graph_width(self, g):
        g = g.copy()
        g.graph['width'] = 800
        return g
    def test_interact_graph_with_graph_width(self):
        fm.interact(self.with_graph_width(self.partial_graph()))
    def test_interact_digraph_with_graph_width(self):
        fm.interact(self.with_graph_width(self.partial_digraph()))
    def test_draw_graph_with_graph_width(self):
        fm.draw(self.with_graph_width(self.partial_graph()))
    def test_draw_digraph_with_graph_width(self):
        fm.draw(self.with_graph_width(self.partial_digraph()))

    def with_float_graph_width(self, g):
        g = g.copy()
        g.graph['width'] = 12.5
        return g
    def test_interact_graph_with_float_graph_width(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_width(self.partial_graph()))
    def test_interact_digraph_with_float_graph_width(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_width(self.partial_digraph()))
    def test_draw_graph_with_float_graph_width(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_width(self.partial_graph()))
    def test_draw_digraph_with_float_graph_width(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_width(self.partial_digraph()))

    def with_nonpositive_graph_width(self, g):
        g = g.copy()
        g.graph['width'] = 0
        return g
    def test_interact_graph_with_nonpositive_graph_width(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_graph_width(self.partial_graph()))
    def test_interact_digraph_with_nonpositive_graph_width(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_graph_width(self.partial_digraph()))
    def test_draw_graph_with_nonpositive_graph_width(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_graph_width(self.partial_graph()))
    def test_draw_digraph_with_nonpositive_graph_width(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_graph_width(self.partial_digraph()))

    def with_graph_height(self, g):
        g = g.copy()
        g.graph['height'] = 450
        return g
    def test_interact_graph_with_graph_height(self):
        fm.interact(self.with_graph_height(self.partial_graph()))
    def test_interact_digraph_with_graph_height(self):
        fm.interact(self.with_graph_height(self.partial_digraph()))
    def test_draw_graph_with_graph_height(self):
        fm.draw(self.with_graph_height(self.partial_graph()))
    def test_draw_digraph_with_graph_height(self):
        fm.draw(self.with_graph_height(self.partial_digraph()))

    def with_float_graph_height(self, g):
        g = g.copy()
        g.graph['height'] = 112.5
        return g
    def test_interact_graph_with_float_graph_height(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_height(self.partial_graph()))
    def test_interact_digraph_with_float_graph_height(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_height(self.partial_digraph()))
    def test_draw_graph_with_float_graph_height(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_height(self.partial_graph()))
    def test_draw_digraph_with_float_graph_height(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_height(self.partial_digraph()))

    def with_nonpositive_graph_height(self, g):
        g = g.copy()
        g.graph['height'] = 0
        return g
    def test_interact_graph_with_nonpositive_graph_height(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_graph_height(self.partial_graph()))
    def test_interact_digraph_with_nonpositive_graph_height(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_graph_height(self.partial_digraph()))
    def test_draw_graph_with_nonpositive_graph_height(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_graph_height(self.partial_graph()))
    def test_draw_digraph_with_nonpositive_graph_height(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_graph_height(self.partial_digraph()))

    def with_graph_bottom(self, g):
        g = g.copy()
        g.graph['bottom'] = 0
        return g
    def test_interact_graph_with_graph_bottom(self):
        fm.interact(self.with_graph_bottom(self.partial_graph()))
    def test_interact_digraph_with_graph_bottom(self):
        fm.interact(self.with_graph_bottom(self.partial_digraph()))
    def test_draw_graph_with_graph_bottom(self):
        fm.draw(self.with_graph_bottom(self.partial_graph()))
    def test_draw_digraph_with_graph_bottom(self):
        fm.draw(self.with_graph_bottom(self.partial_digraph()))

    def with_float_graph_bottom(self, g):
        g = g.copy()
        g.graph['bottom'] = 0.5
        return g
    def test_interact_graph_with_float_graph_bottom(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_bottom(self.partial_graph()))
    def test_interact_digraph_with_float_graph_bottom(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_bottom(self.partial_digraph()))
    def test_draw_graph_with_float_graph_bottom(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_bottom(self.partial_graph()))
    def test_draw_digraph_with_float_graph_bottom(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_bottom(self.partial_digraph()))

    def with_negative_graph_bottom(self, g):
        g = g.copy()
        g.graph['bottom'] = -1
        return g
    def test_interact_graph_with_negative_graph_bottom(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_graph_bottom(self.partial_graph()))
    def test_interact_digraph_with_negative_graph_bottom(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_graph_bottom(self.partial_digraph()))
    def test_draw_graph_with_negative_graph_bottom(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_graph_bottom(self.partial_graph()))
    def test_draw_digraph_with_negative_graph_bottom(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_graph_bottom(self.partial_digraph()))

    def with_graph_left(self, g):
        g = g.copy()
        g.graph['left'] = 0
        return g
    def test_interact_graph_with_graph_left(self):
        fm.interact(self.with_graph_left(self.partial_graph()))
    def test_interact_digraph_with_graph_left(self):
        fm.interact(self.with_graph_left(self.partial_digraph()))
    def test_draw_graph_with_graph_left(self):
        fm.draw(self.with_graph_left(self.partial_graph()))
    def test_draw_digraph_with_graph_left(self):
        fm.draw(self.with_graph_left(self.partial_digraph()))

    def with_float_graph_left(self, g):
        g = g.copy()
        g.graph['left'] = 0.5
        return g
    def test_interact_graph_with_float_graph_left(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_left(self.partial_graph()))
    def test_interact_digraph_with_float_graph_left(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_left(self.partial_digraph()))
    def test_draw_graph_with_float_graph_left(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_left(self.partial_graph()))
    def test_draw_digraph_with_float_graph_left(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_left(self.partial_digraph()))

    def with_negative_graph_left(self, g):
        g = g.copy()
        g.graph['left'] = -1
        return g
    def test_interact_graph_with_negative_graph_left(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_graph_left(self.partial_graph()))
    def test_interact_digraph_with_negative_graph_left(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_graph_left(self.partial_digraph()))
    def test_draw_graph_with_negative_graph_left(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_graph_left(self.partial_graph()))
    def test_draw_digraph_with_negative_graph_left(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_graph_left(self.partial_digraph()))

    def with_graph_right(self, g):
        g = g.copy()
        g.graph['right'] = 0
        return g
    def test_interact_graph_with_graph_right(self):
        fm.interact(self.with_graph_right(self.partial_graph()))
    def test_interact_digraph_with_graph_right(self):
        fm.interact(self.with_graph_right(self.partial_digraph()))
    def test_draw_graph_with_graph_right(self):
        fm.draw(self.with_graph_right(self.partial_graph()))
    def test_draw_digraph_with_graph_right(self):
        fm.draw(self.with_graph_right(self.partial_digraph()))

    def with_float_graph_right(self, g):
        g = g.copy()
        g.graph['right'] = 0.5
        return g
    def test_interact_graph_with_float_graph_right(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_right(self.partial_graph()))
    def test_interact_digraph_with_float_graph_right(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_right(self.partial_digraph()))
    def test_draw_graph_with_float_graph_right(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_right(self.partial_graph()))
    def test_draw_digraph_with_float_graph_right(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_right(self.partial_digraph()))

    def with_negative_graph_right(self, g):
        g = g.copy()
        g.graph['right'] = -1
        return g
    def test_interact_graph_with_negative_graph_right(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_graph_right(self.partial_graph()))
    def test_interact_digraph_with_negative_graph_right(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_graph_right(self.partial_digraph()))
    def test_draw_graph_with_negative_graph_right(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_graph_right(self.partial_graph()))
    def test_draw_digraph_with_negative_graph_right(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_graph_right(self.partial_digraph()))

    def with_graph_top(self, g):
        g = g.copy()
        g.graph['top'] = 0
        return g
    def test_interact_graph_with_graph_top(self):
        fm.interact(self.with_graph_top(self.partial_graph()))
    def test_interact_digraph_with_graph_top(self):
        fm.interact(self.with_graph_top(self.partial_digraph()))
    def test_draw_graph_with_graph_top(self):
        fm.draw(self.with_graph_top(self.partial_graph()))
    def test_draw_digraph_with_graph_top(self):
        fm.draw(self.with_graph_top(self.partial_digraph()))

    def with_float_graph_top(self, g):
        g = g.copy()
        g.graph['top'] = 0.5
        return g
    def test_interact_graph_with_float_graph_top(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_top(self.partial_graph()))
    def test_interact_digraph_with_float_graph_top(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_graph_top(self.partial_digraph()))
    def test_draw_graph_with_float_graph_top(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_top(self.partial_graph()))
    def test_draw_digraph_with_float_graph_top(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_graph_top(self.partial_digraph()))

    def with_negative_graph_top(self, g):
        g = g.copy()
        g.graph['top'] = -1
        return g
    def test_interact_graph_with_negative_graph_top(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_graph_top(self.partial_graph()))
    def test_interact_digraph_with_negative_graph_top(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_graph_top(self.partial_digraph()))
    def test_draw_graph_with_negative_graph_top(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_graph_top(self.partial_graph()))
    def test_draw_digraph_with_negative_graph_top(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_graph_top(self.partial_digraph()))

    def without_node_pos(self, g):
        g = g.copy()
        del g.nodes[N]['pos']
        return g
    def test_interact_graph_without_node_pos(self):
        self.assertRaises(KeyError, fm.interact, self.without_node_pos(self.partial_graph()))
    def test_interact_digraph_without_node_pos(self):
        self.assertRaises(KeyError, fm.interact, self.without_node_pos(self.partial_digraph()))
    def test_draw_graph_without_node_pos(self):
        self.assertRaises(KeyError, fm.draw, self.without_node_pos(self.partial_graph()))
    def test_draw_digraph_without_node_pos(self):
        self.assertRaises(KeyError, fm.draw, self.without_node_pos(self.partial_digraph()))

    def with_none_node_pos(self, g):
        g = g.copy()
        g.nodes[N]['pos'] = None
        return g
    def test_interact_graph_with_none_node_pos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_node_pos(self.partial_graph()))
    def test_interact_digraph_with_none_node_pos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_node_pos(self.partial_digraph()))
    def test_draw_graph_with_none_node_pos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_node_pos(self.partial_graph()))
    def test_draw_digraph_with_none_node_pos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_node_pos(self.partial_digraph()))

    def with_short_node_pos(self, g):
        g = g.copy()
        g.nodes[N]['pos'] = (0.5,)
        return g
    def test_interact_graph_with_short_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_node_pos(self.partial_graph()))
    def test_interact_digraph_with_short_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_node_pos(self.partial_digraph()))
    def test_draw_graph_with_short_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_node_pos(self.partial_graph()))
    def test_draw_digraph_with_short_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_node_pos(self.partial_digraph()))

    def with_long_node_pos(self, g):
        g = g.copy()
        g.nodes[N]['pos'] = (0.5, 0.5, 0.5)
        return g
    def test_interact_graph_with_long_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_node_pos(self.partial_graph()))
    def test_interact_digraph_with_long_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_node_pos(self.partial_digraph()))
    def test_draw_graph_with_long_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_node_pos(self.partial_graph()))
    def test_draw_digraph_with_long_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_node_pos(self.partial_digraph()))

    def with_none_x_node_pos(self, g):
        g = g.copy()
        g.nodes[N]['pos'] = (None, 0.5)
        return g
    def test_interact_graph_with_none_x_node_pos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_x_node_pos(self.partial_graph()))
    def test_interact_digraph_with_none_x_node_pos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_x_node_pos(self.partial_digraph()))
    def test_draw_graph_with_none_x_node_pos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_x_node_pos(self.partial_graph()))
    def test_draw_digraph_with_none_x_node_pos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_x_node_pos(self.partial_digraph()))

    def with_none_y_node_pos(self, g):
        g = g.copy()
        g.nodes[N]['pos'] = (0.5, None)
        return g
    def test_interact_graph_with_none_y_node_pos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_y_node_pos(self.partial_graph()))
    def test_interact_digraph_with_none_y_node_pos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_y_node_pos(self.partial_digraph()))
    def test_draw_graph_with_none_y_node_pos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_y_node_pos(self.partial_graph()))
    def test_draw_digraph_with_none_y_node_pos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_y_node_pos(self.partial_digraph()))

    def with_lower_x_node_pos(self, g):
        g = g.copy()
        g.nodes[N]['pos'] = (-0.5, 0.5)
        return g
    def test_interact_graph_with_lower_x_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_x_node_pos(self.partial_graph()))
    def test_interact_digraph_with_lower_x_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_x_node_pos(self.partial_digraph()))
    def test_draw_graph_with_lower_x_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_x_node_pos(self.partial_graph()))
    def test_draw_digraph_with_lower_x_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_x_node_pos(self.partial_digraph()))

    def with_lower_y_node_pos(self, g):
        g = g.copy()
        g.nodes[N]['pos'] = (0.5, -0.5)
        return g
    def test_interact_graph_with_lower_y_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_y_node_pos(self.partial_graph()))
    def test_interact_digraph_with_lower_y_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_y_node_pos(self.partial_digraph()))
    def test_draw_graph_with_lower_y_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_y_node_pos(self.partial_graph()))
    def test_draw_digraph_with_lower_y_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_y_node_pos(self.partial_digraph()))

    def with_upper_x_node_pos(self, g):
        g = g.copy()
        g.nodes[N]['pos'] = (1.5, 0.5)
        return g
    def test_interact_graph_with_upper_x_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_x_node_pos(self.partial_graph()))
    def test_interact_digraph_with_upper_x_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_x_node_pos(self.partial_digraph()))
    def test_draw_graph_with_upper_x_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_x_node_pos(self.partial_graph()))
    def test_draw_digraph_with_upper_x_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_x_node_pos(self.partial_digraph()))

    def with_upper_y_node_pos(self, g):
        g = g.copy()
        g.nodes[N]['pos'] = (0.5, 1.5)
        return g
    def test_interact_graph_with_upper_y_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_y_node_pos(self.partial_graph()))
    def test_interact_digraph_with_upper_y_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_y_node_pos(self.partial_digraph()))
    def test_draw_graph_with_upper_y_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_y_node_pos(self.partial_graph()))
    def test_draw_digraph_with_upper_y_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_y_node_pos(self.partial_digraph()))

    def with_node_size(self, g):
        g = g.copy()
        g.nodes[N]['size'] = 20
        return g
    def test_interact_graph_with_node_size(self):
        fm.interact(self.with_node_size(self.partial_graph()))
    def test_interact_digraph_with_node_size(self):
        fm.interact(self.with_node_size(self.partial_digraph()))
    def test_draw_graph_with_node_size(self):
        fm.draw(self.with_node_size(self.partial_graph()))
    def test_draw_digraph_with_node_size(self):
        fm.draw(self.with_node_size(self.partial_digraph()))

    def with_float_node_size(self, g):
        g = g.copy()
        g.nodes[N]['size'] = 2.5
        return g
    def test_interact_graph_with_float_node_size(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_node_size(self.partial_graph()))
    def test_interact_digraph_with_float_node_size(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_node_size(self.partial_digraph()))
    def test_draw_graph_with_float_node_size(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_node_size(self.partial_graph()))
    def test_draw_digraph_with_float_node_size(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_node_size(self.partial_digraph()))

    def with_nonpositive_node_size(self, g):
        g = g.copy()
        g.nodes[N]['size'] = 0
        return g
    def test_interact_graph_with_nonpositive_node_size(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_node_size(self.partial_graph()))
    def test_interact_digraph_with_nonpositive_node_size(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_node_size(self.partial_digraph()))
    def test_draw_graph_with_nonpositive_node_size(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_node_size(self.partial_graph()))
    def test_draw_digraph_with_nonpositive_node_size(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_node_size(self.partial_digraph()))

    def with_node_style(self, g):
        g = g.copy()
        g.nodes[N]['style'] = 'circle'
        return g
    def test_interact_graph_with_node_style(self):
        fm.interact(self.with_node_style(self.partial_graph()))
    def test_interact_digraph_with_node_style(self):
        fm.interact(self.with_node_style(self.partial_digraph()))
    def test_draw_graph_with_node_style(self):
        fm.draw(self.with_node_style(self.partial_graph()))
    def test_draw_digraph_with_node_style(self):
        fm.draw(self.with_node_style(self.partial_digraph()))

    def with_invalid_node_style(self, g):
        g = g.copy()
        g.nodes[N]['style'] = 'style'
        return g
    def test_interact_graph_with_invalid_node_style(self):
        self.assertRaises(KeyError, fm.interact, self.with_invalid_node_style(self.partial_graph()))
    def test_interact_digraph_with_invalid_node_style(self):
        self.assertRaises(KeyError, fm.interact, self.with_invalid_node_style(self.partial_digraph()))
    def test_draw_graph_with_invalid_node_style(self):
        self.assertRaises(KeyError, fm.draw, self.with_invalid_node_style(self.partial_graph()))
    def test_draw_digraph_with_invalid_node_style(self):
        self.assertRaises(KeyError, fm.draw, self.with_invalid_node_style(self.partial_digraph()))

    def with_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (255, 255, 255)
        return g
    def test_interact_graph_with_node_color(self):
        fm.interact(self.with_node_color(self.partial_graph()))
    def test_interact_digraph_with_node_color(self):
        fm.interact(self.with_node_color(self.partial_digraph()))
    def test_draw_graph_with_node_color(self):
        fm.draw(self.with_node_color(self.partial_graph()))
    def test_draw_digraph_with_node_color(self):
        fm.draw(self.with_node_color(self.partial_digraph()))

    def with_none_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = None
        return g
    def test_interact_graph_with_none_node_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_node_color(self.partial_graph()))
    def test_interact_digraph_with_none_node_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_node_color(self.partial_digraph()))
    def test_draw_graph_with_none_node_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_node_color(self.partial_graph()))
    def test_draw_digraph_with_none_node_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_node_color(self.partial_digraph()))

    def with_short_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (255, 255)
        return g
    def test_interact_graph_with_short_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_node_color(self.partial_graph()))
    def test_interact_digraph_with_short_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_node_color(self.partial_digraph()))
    def test_draw_graph_with_short_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_node_color(self.partial_graph()))
    def test_draw_digraph_with_short_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_node_color(self.partial_digraph()))

    def with_long_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (255, 255, 255, 255)
        return g
    def test_interact_graph_with_long_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_node_color(self.partial_graph()))
    def test_interact_digraph_with_long_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_node_color(self.partial_digraph()))
    def test_draw_graph_with_long_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_node_color(self.partial_graph()))
    def test_draw_digraph_with_long_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_node_color(self.partial_digraph()))

    def with_float_r_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (127.5, 255, 255)
        return g
    def test_interact_graph_with_float_r_node_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_r_node_color(self.partial_graph()))
    def test_interact_digraph_with_float_r_node_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_r_node_color(self.partial_digraph()))
    def test_draw_graph_with_float_r_node_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_r_node_color(self.partial_graph()))
    def test_draw_digraph_with_float_r_node_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_r_node_color(self.partial_digraph()))

    def with_float_g_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (255, 127.5, 255)
        return g
    def test_interact_graph_with_float_g_node_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_g_node_color(self.partial_graph()))
    def test_interact_digraph_with_float_g_node_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_g_node_color(self.partial_digraph()))
    def test_draw_graph_with_float_g_node_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_g_node_color(self.partial_graph()))
    def test_draw_digraph_with_float_g_node_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_g_node_color(self.partial_digraph()))

    def with_float_b_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (255, 255, 127.5)
        return g
    def test_interact_graph_with_float_b_node_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_b_node_color(self.partial_graph()))
    def test_interact_digraph_with_float_b_node_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_b_node_color(self.partial_digraph()))
    def test_draw_graph_with_float_b_node_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_b_node_color(self.partial_graph()))
    def test_draw_digraph_with_float_b_node_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_b_node_color(self.partial_digraph()))

    def with_lower_r_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (-1, 255, 255)
        return g
    def test_interact_graph_with_lower_r_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_r_node_color(self.partial_graph()))
    def test_interact_digraph_with_lower_r_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_r_node_color(self.partial_digraph()))
    def test_draw_graph_with_lower_r_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_r_node_color(self.partial_graph()))
    def test_draw_digraph_with_lower_r_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_r_node_color(self.partial_digraph()))

    def with_lower_g_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (255, -1, 255)
        return g
    def test_interact_graph_with_lower_g_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_g_node_color(self.partial_graph()))
    def test_interact_digraph_with_lower_g_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_g_node_color(self.partial_digraph()))
    def test_draw_graph_with_lower_g_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_g_node_color(self.partial_graph()))
    def test_draw_digraph_with_lower_g_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_g_node_color(self.partial_digraph()))

    def with_lower_b_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (255, 255, -1)
        return g
    def test_interact_graph_with_lower_b_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_b_node_color(self.partial_graph()))
    def test_interact_digraph_with_lower_b_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_b_node_color(self.partial_digraph()))
    def test_draw_graph_with_lower_b_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_b_node_color(self.partial_graph()))
    def test_draw_digraph_with_lower_b_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_b_node_color(self.partial_digraph()))

    def with_upper_r_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (256, 255, 255)
        return g
    def test_interact_graph_with_upper_r_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_r_node_color(self.partial_graph()))
    def test_interact_digraph_with_upper_r_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_r_node_color(self.partial_digraph()))
    def test_draw_graph_with_upper_r_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_r_node_color(self.partial_graph()))
    def test_draw_digraph_with_upper_r_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_r_node_color(self.partial_digraph()))

    def with_upper_g_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (255, 256, 255)
        return g
    def test_interact_graph_with_upper_g_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_g_node_color(self.partial_graph()))
    def test_interact_digraph_with_upper_g_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_g_node_color(self.partial_digraph()))
    def test_draw_graph_with_upper_g_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_g_node_color(self.partial_graph()))
    def test_draw_digraph_with_upper_g_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_g_node_color(self.partial_digraph()))

    def with_upper_b_node_color(self, g):
        g = g.copy()
        g.nodes[N]['color'] = (255, 255, 256)
        return g
    def test_interact_graph_with_upper_b_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_b_node_color(self.partial_graph()))
    def test_interact_digraph_with_upper_b_node_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_b_node_color(self.partial_digraph()))
    def test_draw_graph_with_upper_b_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_b_node_color(self.partial_graph()))
    def test_draw_digraph_with_upper_b_node_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_b_node_color(self.partial_digraph()))

    def with_node_bwidth(self, g):
        g = g.copy()
        g.nodes[N]['bwidth'] = 1
        return g
    def test_interact_graph_with_node_bwidth(self):
        fm.interact(self.with_node_bwidth(self.partial_graph()))
    def test_interact_digraph_with_node_bwidth(self):
        fm.interact(self.with_node_bwidth(self.partial_digraph()))
    def test_draw_graph_with_node_bwidth(self):
        fm.draw(self.with_node_bwidth(self.partial_graph()))
    def test_draw_digraph_with_node_bwidth(self):
        fm.draw(self.with_node_bwidth(self.partial_digraph()))

    def with_float_node_bwidth(self, g):
        g = g.copy()
        g.nodes[N]['bwidth'] = 0.5
        return g
    def test_interact_graph_with_float_node_bwidth(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_node_bwidth(self.partial_graph()))
    def test_interact_digraph_with_float_node_bwidth(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_node_bwidth(self.partial_digraph()))
    def test_draw_graph_with_float_node_bwidth(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_node_bwidth(self.partial_graph()))
    def test_draw_digraph_with_float_node_bwidth(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_node_bwidth(self.partial_digraph()))

    def with_negative_node_bwidth(self, g):
        g = g.copy()
        g.nodes[N]['bwidth'] = -1
        return g
    def test_interact_graph_with_negative_node_bwidth(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_node_bwidth(self.partial_graph()))
    def test_interact_digraph_with_negative_node_bwidth(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_node_bwidth(self.partial_digraph()))
    def test_draw_graph_with_negative_node_bwidth(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_node_bwidth(self.partial_graph()))
    def test_draw_digraph_with_negative_node_bwidth(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_node_bwidth(self.partial_digraph()))

    def with_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (0, 0, 0)
        return g
    def test_interact_graph_with_node_bcolor(self):
        fm.interact(self.with_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_node_bcolor(self):
        fm.interact(self.with_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_node_bcolor(self):
        fm.draw(self.with_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_node_bcolor(self):
        fm.draw(self.with_node_bcolor(self.partial_digraph()))

    def with_none_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = None
        return g
    def test_interact_graph_with_none_node_bcolor(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_none_node_bcolor(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_none_node_bcolor(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_none_node_bcolor(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_node_bcolor(self.partial_digraph()))

    def with_short_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (0, 0)
        return g
    def test_interact_graph_with_short_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_short_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_short_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_short_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_node_bcolor(self.partial_digraph()))

    def with_long_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (0, 0, 0, 0)
        return g
    def test_interact_graph_with_long_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_long_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_long_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_long_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_node_bcolor(self.partial_digraph()))

    def with_float_r_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (127.5, 0, 0)
        return g
    def test_interact_graph_with_float_r_node_bcolor(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_r_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_float_r_node_bcolor(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_r_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_float_r_node_bcolor(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_r_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_float_r_node_bcolor(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_r_node_bcolor(self.partial_digraph()))

    def with_float_g_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (0, 127.5, 0)
        return g
    def test_interact_graph_with_float_g_node_bcolor(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_g_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_float_g_node_bcolor(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_g_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_float_g_node_bcolor(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_g_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_float_g_node_bcolor(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_g_node_bcolor(self.partial_digraph()))

    def with_float_b_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (0, 0, 127.5)
        return g
    def test_interact_graph_with_float_b_node_bcolor(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_b_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_float_b_node_bcolor(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_b_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_float_b_node_bcolor(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_b_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_float_b_node_bcolor(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_b_node_bcolor(self.partial_digraph()))

    def with_lower_r_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (-1, 0, 0)
        return g
    def test_interact_graph_with_lower_r_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_r_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_lower_r_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_r_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_lower_r_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_r_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_lower_r_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_r_node_bcolor(self.partial_digraph()))

    def with_lower_g_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (0, -1, 0)
        return g
    def test_interact_graph_with_lower_g_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_g_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_lower_g_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_g_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_lower_g_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_g_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_lower_g_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_g_node_bcolor(self.partial_digraph()))

    def with_lower_b_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (0, 0, -1)
        return g
    def test_interact_graph_with_lower_b_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_b_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_lower_b_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_b_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_lower_b_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_b_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_lower_b_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_b_node_bcolor(self.partial_digraph()))

    def with_upper_r_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (256, 0, 0)
        return g
    def test_interact_graph_with_upper_r_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_r_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_upper_r_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_r_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_upper_r_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_r_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_upper_r_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_r_node_bcolor(self.partial_digraph()))

    def with_upper_g_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (0, 256, 0)
        return g
    def test_interact_graph_with_upper_g_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_g_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_upper_g_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_g_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_upper_g_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_g_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_upper_g_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_g_node_bcolor(self.partial_digraph()))

    def with_upper_b_node_bcolor(self, g):
        g = g.copy()
        g.nodes[N]['bcolor'] = (0, 0, 256)
        return g
    def test_interact_graph_with_upper_b_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_b_node_bcolor(self.partial_graph()))
    def test_interact_digraph_with_upper_b_node_bcolor(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_b_node_bcolor(self.partial_digraph()))
    def test_draw_graph_with_upper_b_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_b_node_bcolor(self.partial_graph()))
    def test_draw_digraph_with_upper_b_node_bcolor(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_b_node_bcolor(self.partial_digraph()))

    def with_node_labpos(self, g):
        g = g.copy()
        g.nodes[N]['labpos'] = 'middle center'
        return g
    def test_interact_graph_with_node_labpos(self):
        fm.interact(self.with_node_labpos(self.partial_graph()))
    def test_interact_digraph_with_node_labpos(self):
        fm.interact(self.with_node_labpos(self.partial_digraph()))
    def test_draw_graph_with_node_labpos(self):
        fm.draw(self.with_node_labpos(self.partial_graph()))
    def test_draw_digraph_with_node_labpos(self):
        fm.draw(self.with_node_labpos(self.partial_digraph()))

    def with_none_node_labpos(self, g):
        g = g.copy()
        g.nodes[N]['labpos'] = None
        return g
    def test_interact_graph_with_none_node_labpos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_node_labpos(self.partial_graph()))
    def test_interact_digraph_with_none_node_labpos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_node_labpos(self.partial_digraph()))
    def test_draw_graph_with_none_node_labpos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_node_labpos(self.partial_graph()))
    def test_draw_digraph_with_none_node_labpos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_node_labpos(self.partial_digraph()))

    def with_short_node_labpos(self, g):
        g = g.copy()
        g.nodes[N]['labpos'] = 'middle'
        return g
    def test_interact_graph_with_short_node_labpos(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_node_labpos(self.partial_graph()))
    def test_interact_digraph_with_short_node_labpos(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_node_labpos(self.partial_digraph()))
    def test_draw_graph_with_short_node_labpos(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_node_labpos(self.partial_graph()))
    def test_draw_digraph_with_short_node_labpos(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_node_labpos(self.partial_digraph()))

    def with_long_node_labpos(self, g):
        g = g.copy()
        g.nodes[N]['labpos'] = 'middle center labpos'
        return g
    def test_interact_graph_with_long_node_labpos(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_node_labpos(self.partial_graph()))
    def test_interact_digraph_with_long_node_labpos(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_node_labpos(self.partial_digraph()))
    def test_draw_graph_with_long_node_labpos(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_node_labpos(self.partial_graph()))
    def test_draw_digraph_with_long_node_labpos(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_node_labpos(self.partial_digraph()))

    def with_invalid_vpos_node_labpos(self, g):
        g = g.copy()
        g.nodes[N]['labpos'] = 'vpos center'
        return g
    def test_interact_graph_with_invalid_vpos_node_labpos(self):
        self.assertRaises(KeyError, fm.interact, self.with_invalid_vpos_node_labpos(self.partial_graph()))
    def test_interact_digraph_with_invalid_vpos_node_labpos(self):
        self.assertRaises(KeyError, fm.interact, self.with_invalid_vpos_node_labpos(self.partial_digraph()))
    def test_draw_graph_with_invalid_vpos_node_labpos(self):
        self.assertRaises(KeyError, fm.draw, self.with_invalid_vpos_node_labpos(self.partial_graph()))
    def test_draw_digraph_with_invalid_vpos_node_labpos(self):
        self.assertRaises(KeyError, fm.draw, self.with_invalid_vpos_node_labpos(self.partial_digraph()))

    def with_invalid_hpos_node_labpos(self, g):
        g = g.copy()
        g.nodes[N]['labpos'] = 'middle hpos'
        return g
    def test_interact_graph_with_invalid_hpos_node_labpos(self):
        self.assertRaises(KeyError, fm.interact, self.with_invalid_hpos_node_labpos(self.partial_graph()))
    def test_interact_digraph_with_invalid_hpos_node_labpos(self):
        self.assertRaises(KeyError, fm.interact, self.with_invalid_hpos_node_labpos(self.partial_digraph()))
    def test_draw_graph_with_invalid_hpos_node_labpos(self):
        self.assertRaises(KeyError, fm.draw, self.with_invalid_hpos_node_labpos(self.partial_graph()))
    def test_draw_digraph_with_invalid_hpos_node_labpos(self):
        self.assertRaises(KeyError, fm.draw, self.with_invalid_hpos_node_labpos(self.partial_digraph()))

    def with_edge_width(self, g):
        g = g.copy()
        g.edges[N, M]['width'] = 1
        return g
    def test_interact_graph_with_edge_width(self):
        fm.interact(self.with_edge_width(self.partial_graph()))
    def test_interact_digraph_with_edge_width(self):
        fm.interact(self.with_edge_width(self.partial_digraph()))
    def test_draw_graph_with_edge_width(self):
        fm.draw(self.with_edge_width(self.partial_graph()))
    def test_draw_digraph_with_edge_width(self):
        fm.draw(self.with_edge_width(self.partial_digraph()))

    def with_float_edge_width(self, g):
        g = g.copy()
        g.edges[N, M]['width'] = 1.5
        return g
    def test_interact_graph_with_float_edge_width(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_edge_width(self.partial_graph()))
    def test_interact_digraph_with_float_edge_width(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_edge_width(self.partial_digraph()))
    def test_draw_graph_with_float_edge_width(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_edge_width(self.partial_graph()))
    def test_draw_digraph_with_float_edge_width(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_edge_width(self.partial_digraph()))

    def with_nonpositive_edge_width(self, g):
        g = g.copy()
        g.edges[N, M]['width'] = 0
        return g
    def test_interact_graph_with_nonpositive_edge_width(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_edge_width(self.partial_graph()))
    def test_interact_digraph_with_nonpositive_edge_width(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_edge_width(self.partial_digraph()))
    def test_draw_graph_with_nonpositive_edge_width(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_edge_width(self.partial_graph()))
    def test_draw_digraph_with_nonpositive_edge_width(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_edge_width(self.partial_digraph()))

    def with_edge_style(self, g):
        g = g.copy()
        g.edges[N, M]['style'] = 'solid'
        return g
    def test_interact_graph_with_edge_style(self):
        fm.interact(self.with_edge_style(self.partial_graph()))
    def test_interact_digraph_with_edge_style(self):
        fm.interact(self.with_edge_style(self.partial_digraph()))
    def test_draw_graph_with_edge_style(self):
        fm.draw(self.with_edge_style(self.partial_graph()))
    def test_draw_digraph_with_edge_style(self):
        fm.draw(self.with_edge_style(self.partial_digraph()))

    def with_invalid_edge_style(self, g):
        g = g.copy()
        g.edges[N, M]['style'] = 'style'
        return g
    def test_interact_graph_with_invalid_edge_style(self):
        self.assertRaises(KeyError, fm.interact, self.with_invalid_edge_style(self.partial_graph()))
    def test_interact_digraph_with_invalid_edge_style(self):
        self.assertRaises(KeyError, fm.interact, self.with_invalid_edge_style(self.partial_digraph()))
    def test_draw_graph_with_invalid_edge_style(self):
        self.assertRaises(KeyError, fm.draw, self.with_invalid_edge_style(self.partial_graph()))
    def test_draw_digraph_with_invalid_edge_style(self):
        self.assertRaises(KeyError, fm.draw, self.with_invalid_edge_style(self.partial_digraph()))

    def with_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 0, 0)
        return g
    def test_interact_graph_with_edge_color(self):
        fm.interact(self.with_edge_color(self.partial_graph()))
    def test_interact_digraph_with_edge_color(self):
        fm.interact(self.with_edge_color(self.partial_digraph()))
    def test_draw_graph_with_edge_color(self):
        fm.draw(self.with_edge_color(self.partial_graph()))
    def test_draw_digraph_with_edge_color(self):
        fm.draw(self.with_edge_color(self.partial_digraph()))

    def with_none_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = None
        return g
    def test_interact_graph_with_none_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_edge_color(self.partial_graph()))
    def test_interact_digraph_with_none_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_edge_color(self.partial_digraph()))
    def test_draw_graph_with_none_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_edge_color(self.partial_graph()))
    def test_draw_digraph_with_none_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_edge_color(self.partial_digraph()))

    def with_short_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 0)
        return g
    def test_interact_graph_with_short_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_edge_color(self.partial_graph()))
    def test_interact_digraph_with_short_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_short_edge_color(self.partial_digraph()))
    def test_draw_graph_with_short_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_edge_color(self.partial_graph()))
    def test_draw_digraph_with_short_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_short_edge_color(self.partial_digraph()))

    def with_long_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 0, 0, 0.5, 0.5)
        return g
    def test_interact_graph_with_long_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_edge_color(self.partial_graph()))
    def test_interact_digraph_with_long_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_long_edge_color(self.partial_digraph()))
    def test_draw_graph_with_long_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_edge_color(self.partial_graph()))
    def test_draw_digraph_with_long_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_long_edge_color(self.partial_digraph()))

    def with_float_r_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (127.5, 0, 0, 0.5)
        return g
    def test_interact_graph_with_float_r_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_r_edge_color(self.partial_graph()))
    def test_interact_digraph_with_float_r_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_r_edge_color(self.partial_digraph()))
    def test_draw_graph_with_float_r_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_r_edge_color(self.partial_graph()))
    def test_draw_digraph_with_float_r_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_r_edge_color(self.partial_digraph()))

    def with_float_g_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 127.5, 0, 0.5)
        return g
    def test_interact_graph_with_float_g_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_g_edge_color(self.partial_graph()))
    def test_interact_digraph_with_float_g_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_g_edge_color(self.partial_digraph()))
    def test_draw_graph_with_float_g_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_g_edge_color(self.partial_graph()))
    def test_draw_digraph_with_float_g_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_g_edge_color(self.partial_digraph()))

    def with_float_b_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 0, 127.5, 0.5)
        return g
    def test_interact_graph_with_float_b_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_b_edge_color(self.partial_graph()))
    def test_interact_digraph_with_float_b_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_b_edge_color(self.partial_digraph()))
    def test_draw_graph_with_float_b_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_b_edge_color(self.partial_graph()))
    def test_draw_digraph_with_float_b_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_b_edge_color(self.partial_digraph()))

    def with_none_a_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 0, 0, None)
        return g
    def test_interact_graph_with_none_a_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_a_edge_color(self.partial_graph()))
    def test_interact_digraph_with_none_a_edge_color(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_a_edge_color(self.partial_digraph()))
    def test_draw_graph_with_none_a_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_a_edge_color(self.partial_graph()))
    def test_draw_digraph_with_none_a_edge_color(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_a_edge_color(self.partial_digraph()))

    def with_lower_r_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (-1, 0, 0, 0.5)
        return g
    def test_interact_graph_with_lower_r_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_r_edge_color(self.partial_graph()))
    def test_interact_digraph_with_lower_r_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_r_edge_color(self.partial_digraph()))
    def test_draw_graph_with_lower_r_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_r_edge_color(self.partial_graph()))
    def test_draw_digraph_with_lower_r_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_r_edge_color(self.partial_digraph()))

    def with_lower_g_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, -1, 0, 0.5)
        return g
    def test_interact_graph_with_lower_g_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_g_edge_color(self.partial_graph()))
    def test_interact_digraph_with_lower_g_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_g_edge_color(self.partial_digraph()))
    def test_draw_graph_with_lower_g_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_g_edge_color(self.partial_graph()))
    def test_draw_digraph_with_lower_g_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_g_edge_color(self.partial_digraph()))

    def with_lower_b_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 0, -1, 0.5)
        return g
    def test_interact_graph_with_lower_b_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_b_edge_color(self.partial_graph()))
    def test_interact_digraph_with_lower_b_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_b_edge_color(self.partial_digraph()))
    def test_draw_graph_with_lower_b_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_b_edge_color(self.partial_graph()))
    def test_draw_digraph_with_lower_b_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_b_edge_color(self.partial_digraph()))

    def with_lower_a_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 0, 0, -0.5)
        return g
    def test_interact_graph_with_lower_a_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_a_edge_color(self.partial_graph()))
    def test_interact_digraph_with_lower_a_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_a_edge_color(self.partial_digraph()))
    def test_draw_graph_with_lower_a_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_a_edge_color(self.partial_graph()))
    def test_draw_digraph_with_lower_a_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_a_edge_color(self.partial_digraph()))

    def with_upper_r_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (256, 0, 0, 0.5)
        return g
    def test_interact_graph_with_upper_r_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_r_edge_color(self.partial_graph()))
    def test_interact_digraph_with_upper_r_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_r_edge_color(self.partial_digraph()))
    def test_draw_graph_with_upper_r_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_r_edge_color(self.partial_graph()))
    def test_draw_digraph_with_upper_r_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_r_edge_color(self.partial_digraph()))

    def with_upper_g_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 256, 0, 0.5)
        return g
    def test_interact_graph_with_upper_g_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_g_edge_color(self.partial_graph()))
    def test_interact_digraph_with_upper_g_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_g_edge_color(self.partial_digraph()))
    def test_draw_graph_with_upper_g_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_g_edge_color(self.partial_graph()))
    def test_draw_digraph_with_upper_g_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_g_edge_color(self.partial_digraph()))

    def with_upper_b_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 0, 256, 0.5)
        return g
    def test_interact_graph_with_upper_b_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_b_edge_color(self.partial_graph()))
    def test_interact_digraph_with_upper_b_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_b_edge_color(self.partial_digraph()))
    def test_draw_graph_with_upper_b_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_b_edge_color(self.partial_graph()))
    def test_draw_digraph_with_upper_b_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_b_edge_color(self.partial_digraph()))

    def with_upper_a_edge_color(self, g):
        g = g.copy()
        g.edges[N, M]['color'] = (0, 0, 0, 1.5)
        return g
    def test_interact_graph_with_upper_a_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_a_edge_color(self.partial_graph()))
    def test_interact_digraph_with_upper_a_edge_color(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_a_edge_color(self.partial_digraph()))
    def test_draw_graph_with_upper_a_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_a_edge_color(self.partial_graph()))
    def test_draw_digraph_with_upper_a_edge_color(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_a_edge_color(self.partial_digraph()))

    def with_edge_labflip(self, g):
        g = g.copy()
        g.edges[N, M]['labflip'] = False
        return g
    def test_interact_graph_with_edge_labflip(self):
        fm.interact(self.with_edge_labflip(self.partial_graph()))
    def test_interact_digraph_with_edge_labflip(self):
        fm.interact(self.with_edge_labflip(self.partial_digraph()))
    def test_draw_graph_with_edge_labflip(self):
        fm.draw(self.with_edge_labflip(self.partial_graph()))
    def test_draw_digraph_with_edge_labflip(self):
        fm.draw(self.with_edge_labflip(self.partial_digraph()))

    def with_none_edge_labflip(self, g):
        g = g.copy()
        g.edges[N, M]['labflip'] = None
        return g
    def test_interact_graph_with_none_edge_labflip(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_edge_labflip(self.partial_graph()))
    def test_interact_digraph_with_none_edge_labflip(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_edge_labflip(self.partial_digraph()))
    def test_draw_graph_with_none_edge_labflip(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_edge_labflip(self.partial_graph()))
    def test_draw_digraph_with_none_edge_labflip(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_edge_labflip(self.partial_digraph()))

    def with_edge_labdist(self, g):
        g = g.copy()
        g.edges[N, M]['labdist'] = 10
        return g
    def test_interact_graph_with_edge_labdist(self):
        fm.interact(self.with_edge_labdist(self.partial_graph()))
    def test_interact_digraph_with_edge_labdist(self):
        fm.interact(self.with_edge_labdist(self.partial_digraph()))
    def test_draw_graph_with_edge_labdist(self):
        fm.draw(self.with_edge_labdist(self.partial_graph()))
    def test_draw_digraph_with_edge_labdist(self):
        fm.draw(self.with_edge_labdist(self.partial_digraph()))

    def with_float_edge_labdist(self, g):
        g = g.copy()
        g.edges[N, M]['labdist'] = 2.5
        return g
    def test_interact_graph_with_float_edge_labdist(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_edge_labdist(self.partial_graph()))
    def test_interact_digraph_with_float_edge_labdist(self):
        self.assertRaises(TypeError, fm.interact, self.with_float_edge_labdist(self.partial_digraph()))
    def test_draw_graph_with_float_edge_labdist(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_edge_labdist(self.partial_graph()))
    def test_draw_digraph_with_float_edge_labdist(self):
        self.assertRaises(TypeError, fm.draw, self.with_float_edge_labdist(self.partial_digraph()))

    def with_negative_edge_labdist(self, g):
        g = g.copy()
        g.edges[N, M]['labdist'] = -1
        return g
    def test_interact_graph_with_negative_edge_labdist(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_edge_labdist(self.partial_graph()))
    def test_interact_digraph_with_negative_edge_labdist(self):
        self.assertRaises(ValueError, fm.interact, self.with_negative_edge_labdist(self.partial_digraph()))
    def test_draw_graph_with_negative_edge_labdist(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_edge_labdist(self.partial_graph()))
    def test_draw_digraph_with_negative_edge_labdist(self):
        self.assertRaises(ValueError, fm.draw, self.with_negative_edge_labdist(self.partial_digraph()))

    def with_edge_labfrac(self, g):
        g = g.copy()
        g.edges[N, M]['labfrac'] = 0.5
        return g
    def test_interact_graph_with_edge_labfrac(self):
        fm.interact(self.with_edge_labfrac(self.partial_graph()))
    def test_interact_digraph_with_edge_labfrac(self):
        fm.interact(self.with_edge_labfrac(self.partial_digraph()))
    def test_draw_graph_with_edge_labfrac(self):
        fm.draw(self.with_edge_labfrac(self.partial_graph()))
    def test_draw_digraph_with_edge_labfrac(self):
        fm.draw(self.with_edge_labfrac(self.partial_digraph()))

    def with_none_edge_labfrac(self, g):
        g = g.copy()
        g.edges[N, M]['labfrac'] = None
        return g
    def test_interact_graph_with_none_edge_labfrac(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_edge_labfrac(self.partial_graph()))
    def test_interact_digraph_with_none_edge_labfrac(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_edge_labfrac(self.partial_digraph()))
    def test_draw_graph_with_none_edge_labfrac(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_edge_labfrac(self.partial_graph()))
    def test_draw_digraph_with_none_edge_labfrac(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_edge_labfrac(self.partial_digraph()))

    def with_lower_edge_labfrac(self, g):
        g = g.copy()
        g.edges[N, M]['labfrac'] = -0.5
        return g
    def test_interact_graph_with_lower_edge_labfrac(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_edge_labfrac(self.partial_graph()))
    def test_interact_digraph_with_lower_edge_labfrac(self):
        self.assertRaises(ValueError, fm.interact, self.with_lower_edge_labfrac(self.partial_digraph()))
    def test_draw_graph_with_lower_edge_labfrac(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_edge_labfrac(self.partial_graph()))
    def test_draw_digraph_with_lower_edge_labfrac(self):
        self.assertRaises(ValueError, fm.draw, self.with_lower_edge_labfrac(self.partial_digraph()))

    def with_upper_edge_labfrac(self, g):
        g = g.copy()
        g.edges[N, M]['labfrac'] = 1.5
        return g
    def test_interact_graph_with_upper_edge_labfrac(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_edge_labfrac(self.partial_graph()))
    def test_interact_digraph_with_upper_edge_labfrac(self):
        self.assertRaises(ValueError, fm.interact, self.with_upper_edge_labfrac(self.partial_digraph()))
    def test_draw_graph_with_upper_edge_labfrac(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_edge_labfrac(self.partial_graph()))
    def test_draw_digraph_with_upper_edge_labfrac(self):
        self.assertRaises(ValueError, fm.draw, self.with_upper_edge_labfrac(self.partial_digraph()))

    def test_interact_graph_with_physics(self):
        fm.interact(self.partial_graph(), True)
    def test_interact_digraph_with_physics(self):
        fm.interact(self.partial_digraph(), True)
    def test_interact_graph_with_none_physics(self):
        self.assertRaises(TypeError, fm.interact, self.partial_graph(), None)
    def test_interact_digraph_with_none_physics(self):
        self.assertRaises(TypeError, fm.interact, self.partial_digraph(), None)

    def test_draw_graph_with_toolbar(self):
        fm.draw(self.partial_graph(), True)
    def test_draw_digraph_with_toolbar(self):
        fm.draw(self.partial_digraph(), True)
    def test_draw_graph_with_none_toolbar(self):
        self.assertRaises(TypeError, fm.draw, self.partial_graph(), None)
    def test_draw_digraph_with_none_toolbar(self):
        self.assertRaises(TypeError, fm.draw, self.partial_digraph(), None)

    def test_animation_with_width(self):
        fm.Animation(width=800)
    def test_animation_with_float_width(self):
        self.assertRaises(TypeError, fm.Animation, width=12.5)
    def test_animation_with_nonpositive_width(self):
        self.assertRaises(ValueError, fm.Animation, width=0)

    def test_animation_with_height(self):
        fm.Animation(height=450)
    def test_animation_with_float_height(self):
        self.assertRaises(TypeError, fm.Animation, height=112.5)
    def test_animation_with_nonpositive_height(self):
        self.assertRaises(ValueError, fm.Animation, height=0)

    def test_animation(self):
        a = fm.Animation()
        self.assertRaises(ValueError, a.play)
    def test_animation_with_one_graph(self):
        a = fm.Animation()
        a.rec(self.partial_graph())
        self.assertRaises(ValueError, a.play)
    def test_animation_with_one_digraph(self):
        a = fm.Animation()
        a.rec(self.partial_digraph())
        self.assertRaises(ValueError, a.play)
    def test_animation_with_two_graphs(self):
        a = fm.Animation()
        a.rec(self.partial_graph())
        a.rec(self.partial_graph())
        a.play()
    def test_animation_with_two_digraphs(self):
        a = fm.Animation()
        a.rec(self.partial_digraph())
        a.rec(self.partial_digraph())
        a.play()


if __name__ == '__main__':
    unittest.main()
