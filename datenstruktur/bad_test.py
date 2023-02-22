import unittest

import graphEX
from edge import Edge
from graph import BipartiteGraph, DirectedGraph, Graph, WeightedGraph

# from graph import WeightedDirectedGraph
from node import Node


class TestGraph(unittest.TestCase):
    def test_directed_graph(self):
        """Tests the correctness of a directed Graph."""
        G = DirectedGraph()
        nodes = dict()
        nodes["A"] = G.add_node("A")
        nodes["B"] = G.add_node("B")
        nodes["C"] = G.add_node("C")
        nodes["D"] = G.add_node("D")
        nodes["E"] = G.add_node("E")

        self.assertEqual(len(G), 5)

        self.assertEqual(
            nodes["A"].in_degree, len(G.get_node_neighbors(nodes["A"], which="in"))
        )
        self.assertEqual(
            nodes["A"].out_degree, len(G.get_node_neighbors(nodes["A"], which="out"))
        )

        G.add_edge(nodes["A"], nodes["B"])
        edge_1 = G.add_edge(nodes["A"], nodes["C"])
        G.add_edge(nodes["A"], nodes["D"])
        G.add_edge(nodes["A"], nodes["E"])
        G.add_edge(nodes["B"], nodes["A"])
        G.add_edge(nodes["C"], nodes["D"])
        G.add_edge(nodes["E"], nodes["B"])
        G.add_edge(nodes["D"], nodes["A"])
        edge_2 = G.add_edge(nodes["B"], nodes["C"])

        self.assertEqual(
            nodes["A"].in_degree, len(G.get_node_neighbors(nodes["A"], which="in"))
        )
        self.assertEqual(
            nodes["A"].out_degree, len(G.get_node_neighbors(nodes["A"], which="out"))
        )

        self.assertEqual(edge_1.dest_node, edge_2.dest_node)

        G.breadth_first_search(nodes["A"])
        G.depth_first_search(nodes["A"])
        G.topological_sort()

        self.assertEqual(len(G.get_node_neighbors(nodes["A"], which="all")), 4)
        self.assertEqual(len(G.get_node_neighbors(nodes["A"], which="in")), 2)
        G.remove_node(nodes["B"])

        self.assertEqual(
            nodes["A"].in_degree, len(G.get_node_neighbors(nodes["A"], which="in"))
        )
        self.assertEqual(
            nodes["A"].out_degree, len(G.get_node_neighbors(nodes["A"], which="out"))
        )

        self.assertEqual(len(G.get_node_neighbors(nodes["A"], which="all")), 3)
        self.assertEqual(len(G.get_node_neighbors(nodes["A"], which="in")), 1)
        G.remove_edge(nodes["D"], nodes["A"])
        self.assertEqual(len(G.get_node_neighbors(nodes["A"], which="all")), 3)
        self.assertEqual(len(G.get_node_neighbors(nodes["A"], which="in")), 0)
        G.topological_sort()

        self.assertEqual(
            nodes["A"].in_degree, len(G.get_node_neighbors(nodes["A"], which="in"))
        )
        self.assertEqual(
            nodes["A"].out_degree, len(G.get_node_neighbors(nodes["A"], which="out"))
        )

    def test_undirected_graph(self):
        """Tests the correctness of an undirected Graph."""
        G = Graph()
        nodes = dict()
        nodes["A"] = G.add_node("A")
        nodes["B"] = G.add_node("B")
        nodes["C"] = G.add_node("C")
        nodes["D"] = G.add_node("D")
        nodes["E"] = G.add_node("E")

        self.assertEqual(len(G), 5)

        G.add_edge(nodes["A"], nodes["B"])
        G.add_edge(nodes["A"], nodes["C"])
        G.add_edge(nodes["A"], nodes["D"])
        G.add_edge(nodes["A"], nodes["E"])

        G.breadth_first_search(nodes["A"])
        G.depth_first_search(nodes["A"])

        self.assertEqual(len(G.get_node_neighbors(nodes["A"])), 4)
        print(nodes["A"]._edges)
        G.remove_node(nodes["B"])
        print(nodes["A"]._edges)
        self.assertEqual(len(G.get_node_neighbors(nodes["A"])), 3)
        self.assertEqual(len(G.get_node_neighbors(nodes["C"])), 1)
        self.assertEqual(len(G.get_node_neighbors(nodes["D"])), 1)
        self.assertEqual(len(G.get_node_neighbors(nodes["E"])), 1)
        G.remove_edge(nodes["D"], nodes["A"])
        self.assertEqual(len(G.get_node_neighbors(nodes["A"])), 2)
        self.assertEqual(len(G.get_node_neighbors(nodes["D"])), 0)

    def test_bipartite_graph(self):
        """Tests the correctness of a bipartite Graph."""
        l_nodes = ["A", "B", "C"]
        r_nodes = ["D", "E", "F"]
        edges = [("A", "F"), ("A", "D"), ("B", "E"), ("B", "F"), ("C", "D")]
        G = BipartiteGraph(l_nodes, r_nodes, edges)
        with self.assertRaises(graphEX.AddNodeException):
            G.add_node("X")


if __name__ == "__main__":
    unittest.main(exit=False)
