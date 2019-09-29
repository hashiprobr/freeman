import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..')))

import unittest

import networkx as nx
import freeman as fm


N = 'Medici'


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

    def with_float_graph_width(self, g):
        g = g.copy()
        g.graph['width'] = 1.5
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

    def with_float_graph_height(self, g):
        g = g.copy()
        g.graph['height'] = 1.5
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
        del g.node[N]['pos']
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
        g.node[N]['pos'] = None
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
        g.node[N]['pos'] = (0,)
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
        g.node[N]['pos'] = (0, 0, 0, 0)
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
        g.node[N]['pos'] = (None, 0)
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
        g.node[N]['pos'] = (0, None)
        return g
    def test_interact_graph_with_none_y_node_pos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_y_node_pos(self.partial_graph()))
    def test_interact_digraph_with_none_y_node_pos(self):
        self.assertRaises(TypeError, fm.interact, self.with_none_y_node_pos(self.partial_digraph()))
    def test_draw_graph_with_none_y_node_pos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_y_node_pos(self.partial_graph()))
    def test_draw_digraph_with_none_y_node_pos(self):
        self.assertRaises(TypeError, fm.draw, self.with_none_y_node_pos(self.partial_digraph()))

    def with_minusone_x_node_pos(self, g):
        g = g.copy()
        g.node[N]['pos'] = (-1, 0)
        return g
    def test_interact_graph_with_minusone_x_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_minusone_x_node_pos(self.partial_graph()))
    def test_interact_digraph_with_minusone_x_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_minusone_x_node_pos(self.partial_digraph()))
    def test_draw_graph_with_minusone_x_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_minusone_x_node_pos(self.partial_graph()))
    def test_draw_digraph_with_minusone_x_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_minusone_x_node_pos(self.partial_digraph()))

    def with_minusone_y_node_pos(self, g):
        g = g.copy()
        g.node[N]['pos'] = (0, -1)
        return g
    def test_interact_graph_with_minusone_y_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_minusone_y_node_pos(self.partial_graph()))
    def test_interact_digraph_with_minusone_y_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_minusone_y_node_pos(self.partial_digraph()))
    def test_draw_graph_with_minusone_y_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_minusone_y_node_pos(self.partial_graph()))
    def test_draw_digraph_with_minusone_y_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_minusone_y_node_pos(self.partial_digraph()))

    def with_two_x_node_pos(self, g):
        g = g.copy()
        g.node[N]['pos'] = (2, 0)
        return g
    def test_interact_graph_with_two_x_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_two_x_node_pos(self.partial_graph()))
    def test_interact_digraph_with_two_x_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_two_x_node_pos(self.partial_digraph()))
    def test_draw_graph_with_two_x_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_two_x_node_pos(self.partial_graph()))
    def test_draw_digraph_with_two_x_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_two_x_node_pos(self.partial_digraph()))

    def with_two_y_node_pos(self, g):
        g = g.copy()
        g.node[N]['pos'] = (0, 2)
        return g
    def test_interact_graph_with_two_y_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_two_y_node_pos(self.partial_graph()))
    def test_interact_digraph_with_two_y_node_pos(self):
        self.assertRaises(ValueError, fm.interact, self.with_two_y_node_pos(self.partial_digraph()))
    def test_draw_graph_with_two_y_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_two_y_node_pos(self.partial_graph()))
    def test_draw_digraph_with_two_y_node_pos(self):
        self.assertRaises(ValueError, fm.draw, self.with_two_y_node_pos(self.partial_digraph()))

    def with_node_size(self, g):
        g = g.copy()
        g.node[N]['size'] = 20
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
        g.node[N]['size'] = 1.5
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
        g.node[N]['size'] = 0
        return g
    def test_interact_graph_with_nonpositive_node_size(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_node_size(self.partial_graph()))
    def test_interact_digraph_with_nonpositive_node_size(self):
        self.assertRaises(ValueError, fm.interact, self.with_nonpositive_node_size(self.partial_digraph()))
    def test_draw_graph_with_nonpositive_node_size(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_node_size(self.partial_graph()))
    def test_draw_digraph_with_nonpositive_node_size(self):
        self.assertRaises(ValueError, fm.draw, self.with_nonpositive_node_size(self.partial_digraph()))


if __name__ == '__main__':
    unittest.main()
