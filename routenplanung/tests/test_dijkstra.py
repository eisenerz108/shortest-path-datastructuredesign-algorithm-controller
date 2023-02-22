"""
Created Date : 28-Jul-22
@author : Aman Jain
"""
import unittest

import pytest
from datenstruktur.graph import create_graph

from routenplanung.dijkstra import Dijkstra
from routenplanung.utils import constants


class TestDijkstra(unittest.TestCase):
    def test_source_target_nodes(self):
        weighted_graph, S, T = create_weighted_graph()
        dijkstra = Dijkstra()
        dijkstra.run(graph=weighted_graph, start_node=S, end_node=T)
        assert dijkstra.start_node.label == "S"
        assert dijkstra.end_node.label == "T"

    def test_default_edge_weights(self):
        weighted_graph, _, _ = create_weighted_graph()
        for edge in weighted_graph.edges:
            assert edge.weight is not None

    def test_length_distance_matrix_nodes(self):
        weighted_graph, S, T = create_weighted_graph()
        dijkstra = Dijkstra()
        dijkstra.run(graph=weighted_graph, start_node=S, end_node=T)
        assert len(dijkstra.distance.items()) == len(weighted_graph.nodes)

    def test_distance_source_zero(self):
        weighted_graph, S, T = create_weighted_graph()
        dijkstra = Dijkstra()
        dijkstra.run(graph=weighted_graph, start_node=S, end_node=T)
        assert dijkstra.distance.get("S") == [0]

    def test_non_weighted_graph(self):
        directed_graph = create_graph(directed=True)
        S, A, B, C, T = directed_graph.add_nodes(["S", "A", "B", "C", "T"])
        SB = directed_graph.add_edge(S, B)
        SA = directed_graph.add_edge(S, A)
        AC = directed_graph.add_edge(A, C)
        CT = directed_graph.add_edge(C, T)
        dijkstra = Dijkstra()
        with pytest.raises(Exception) as exinfo:
            dijkstra.run(directed_graph, S, T)
        assert str(exinfo.value) == constants.DA_EXCEPTION_ERROR

    def test_previous_nodes_length(self):
        weighted_graph, S, T = create_weighted_graph()
        dijkstra = Dijkstra()
        dijkstra.run(weighted_graph, S, T)
        assert len(dijkstra.previous_nodes) == len(weighted_graph.nodes) - 1

    def test_previous_nodes_T(self):
        weighted_graph, S, T = create_weighted_graph()
        dijkstra = Dijkstra()
        dijkstra.run(weighted_graph, S, T)
        assert dijkstra.previous_nodes[T].label == "B"

    def test_target_node_cost(self):
        weighted_graph, S, T = create_weighted_graph()
        dijkstra = Dijkstra()
        dijkstra.run(weighted_graph, S, T)
        assert dijkstra.distance.get("T") == [3]


def create_weighted_graph():
    weighted_graph = create_graph(weighted=True)
    S, A, B, C, T = weighted_graph.add_nodes(["S", "A", "B", "C", "T"])
    SB = weighted_graph.add_edge(S, B, 1)
    SA = weighted_graph.add_edge(S, A, 3)
    AC = weighted_graph.add_edge(A, C, 4)
    BT = weighted_graph.add_edge(B, T, 2)
    CT = weighted_graph.add_edge(C, T)
    return weighted_graph, S, T
