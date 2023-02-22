"""
Created Date : 23-Jun-22
@author : Oskar Besler
"""

from lib2to3.pytree import Node
import unittest

from datenstruktur.graph import create_graph
from routenplanung.floyd_warshall import FloydWarshall
import routenplanung.utils.exceptions_alg as ex
from routenplanung.floyd_warshall import FloydWarshall


class TestFloydWGraph(unittest.TestCase):
    def test_graph(self):
        # TODO Check if graph is directed edge cases etc.
        graph = create_graph(weighted=True, directed=True, bipartite=False)
        A, B, C = graph.add_nodes(["A", "B", "C"])
        AB = graph.add_edge(A, B, 1)
        AC = graph.add_edge(A, C, 5)
        BA = graph.add_edge(B, A, 2)
        BC = graph.add_edge(B, C, 1)
        CB = graph.add_edge(C, B, 8)
        FW_distances = FloydWarshall(graph, None, is_test=True).run(graph, None, None)
        self.assertEqual(FW_distances, True)

    def test_gnd_exception(self):
        graph = create_graph(weighted=True, directed=False, bipartite=False)
        FW_distances = FloydWarshall(graph, None, is_test=True).run(graph, None, None)
        self.assertEqual(FW_distances, False)

    def test_no_weight_exception(self):
        graph = create_graph(directed=True, bipartite=False)
        A, B, C = graph.add_nodes(["A", "B", "C"])
        AB = graph.add_edge(A, B)
        AC = graph.add_edge(A, C)
        BA = graph.add_edge(B, A)
        BC = graph.add_edge(B, C)
        CB = graph.add_edge(C, B)
        FW_distances = FloydWarshall(graph, None, is_test=True).run(graph, None, None)
        self.assertEqual(FW_distances, False)

    def test_negc_exception(self):
        graph = create_graph(weighted=True, directed=True, bipartite=False)
        A, B, C = graph.add_nodes(["A", "B", "C"])
        AB = graph.add_edge(A, B, 1)
        AC = graph.add_edge(A, C, 5)
        BA = graph.add_edge(B, A, -2)
        BC = graph.add_edge(B, C, 1)
        CB = graph.add_edge(C, B, 8)
        FW_distances = FloydWarshall(graph, None, is_test=True).run(graph, None, None)
        self.assertEqual(FW_distances, False)

    def test_gnc_exception(self):
        graph = create_graph(weighted=True, directed=True, bipartite=False)
        A, B, C = graph.add_nodes(["A", "B", "C"])
        AB = graph.add_edge(A, B, 1)
        AC = graph.add_edge(A, C, 5)
        BC = graph.add_edge(B, C, 1)
        CB = graph.add_edge(C, B, 8)
        FW_distances = FloydWarshall(graph, None, is_test=True).run(graph, None, None)
        self.assertEqual(FW_distances, False)

    def test_no_node_exception(self):
        graph = create_graph(weighted=True, directed=True, bipartite=False)
        FW_distances = FloydWarshall(graph, None, is_test=True).run(graph, None, None)
        self.assertEqual(FW_distances, False)

    def test_one_node_exception(self):
        graph = create_graph(weighted=True, directed=True, bipartite=False)
        A = graph.add_nodes(["A"])
        FW_distances = FloydWarshall(graph, None, is_test=True).run(graph, None, None)
        self.assertEqual(FW_distances, True)

    def test_two_node_exception(self):
        graph = create_graph(weighted=True, directed=True, bipartite=False)
        A, B = graph.add_nodes(["A", "B"])
        AB = graph.add_edge(A, B, 1)
        BA = graph.add_edge(B, A, 2)
        FW_distances = FloydWarshall(graph, None, is_test=True).run(graph, None, None)
        self.assertEqual(FW_distances, True)


if __name__ == "__main__":
    unittest.main()
