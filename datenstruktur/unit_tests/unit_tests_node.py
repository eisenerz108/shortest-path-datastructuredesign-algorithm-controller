import os
import sys
import unittest

sys.path.append(os.path.dirname(__file__) + "/../../")  # Go to parent directory.

from datenstruktur.graph import DirectedGraph, Graph, create_graph
from datenstruktur.node import Node


class TestNode(unittest.TestCase):
    def test_init__(self):
        """Tests the Node constructor regarding the label attribute."""
        node_none = Node(None)
        node_str = Node("A")
        node_list = Node([0, 1, 2])
        node_num_int = Node(4)
        node_num_float = Node(4.0)

        self.assertEqual(type(node_none.label), type(None))
        self.assertEqual(node_str.label, "A")
        self.assertEqual(type(node_list.label), list)
        self.assertEqual(node_num_int.label, 4)
        self.assertEqual(node_num_float.label, 4.0)

    def test_str__(self):
        """Tests the string representation of the Node."""
        self.assertEqual(str(Node("ABC")), "ABC")
        self.assertNotEqual(str(Node("ABC")), "ABCD")

    def test_hash__(self):
        """Tests the custom hash function of the Node."""
        pass

    def test_info(self):
        """Tests the info property with different variable types."""
        node_without_info = Node("no_info_node_label")
        node_with_info = Node("info_node_label")
        node_with_info.info = ("Text", 2, [3])

        self.assertEqual(node_without_info.info, None)
        self.assertEqual(node_with_info.info, ("Text", 2, [3]))
        self.assertEqual(node_with_info.info[0], "Text")
        self.assertEqual(node_with_info.info[1], 2)
        self.assertEqual(node_with_info.info[2], [3])

    def test_degrees(self):
        """Tests the various degree properties for all graphs."""
        g_uu = create_graph()
        g_ud = create_graph(directed=True)
        # TODO: Implement tests for bipartite graphs.

        # Tests for undirected, unweighted graph.
        A, B, C = g_uu.add_nodes(["A", "B", "C"])
        g_uu.add_edge(A, B)
        g_uu.add_edge(B, C)

        self.assertEqual(A.degree, 1)
        self.assertEqual(A.in_degree, 1)
        self.assertEqual(A.out_degree, 1)

        self.assertEqual(B.degree, 2)
        self.assertEqual(B.in_degree, 2)
        self.assertEqual(B.out_degree, 2)

        self.assertEqual(C.degree, 1)
        self.assertEqual(C.in_degree, 1)
        self.assertEqual(C.out_degree, 1)

        # Tests for directed, unweighted graph.
        A, B, C = g_ud.add_nodes(["A", "B", "C"])
        g_ud.add_edge(A, B)
        g_ud.add_edge(B, C)

        self.assertEqual(A.degree, 1)
        self.assertEqual(A.in_degree, 0)
        self.assertEqual(A.out_degree, 1)

        self.assertEqual(B.degree, 2)
        self.assertEqual(B.in_degree, 1)
        self.assertEqual(B.out_degree, 1)

        self.assertEqual(C.degree, 1)
        self.assertEqual(C.in_degree, 1)
        self.assertEqual(C.out_degree, 0)

        # TODO: Tests for undirected, weighted graph.

        # TODO: Tests for directed, weighted graph.

    def test_visited(self):
        """Tests the visited property."""
        pass

    def test_visited_setter(self):
        """Tests the visited property's setter."""
        pass

    def test_get_neighbours(self):
        """Tests getting a list of neighbours including the case of self-loop."""
        g = create_graph()

        D, E, F, G = g.add_nodes(["D", "E", "F", "G"])
        g.add_edge(D, E)
        g.add_edge(E, F)
        g.add_edge(G, G)

        self.assertListEqual(D.get_neighbours(), [E])
        self.assertListEqual(E.get_neighbours(), [D, F])
        self.assertListEqual(F.get_neighbours(), [E])
        self.assertListEqual(
            G.get_neighbours(), [G]
        )  # A self-loop contains itself only once as neighbour.

    def test_has_edge(self):
        """Tests whether a Node has an Edge to another Node or itself."""
        g_uu = create_graph()

        A, B, C = g_uu.add_nodes(["A", "B", "C"])
        D = Node("D")
        g_uu.add_edge(A, B)
        g_uu.add_edge(C, C)

        # A
        self.assertFalse(A.has_edge(A))
        self.assertTrue(A.has_edge(B))
        self.assertFalse(A.has_edge(C))

        # B
        self.assertTrue(B.has_edge(A))
        self.assertFalse(B.has_edge(B))
        self.assertFalse(B.has_edge(C))

        # C
        self.assertFalse(C.has_edge(A))
        self.assertFalse(C.has_edge(B))
        self.assertTrue(C.has_edge(C))

        # D
        self.assertFalse(D.has_edge(A))
        self.assertFalse(D.has_edge(B))
        self.assertFalse(D.has_edge(C))
        self.assertFalse(D.has_edge(D))


if __name__ == "__main__":
    unittest.main(exit=False)
