"""
Created Date : 18-Jul-22
created by Jan-Robert Frank
"""
import unittest

import pytest
from datenstruktur.graph import Graph, create_graph

from routenplanung.bellman_ford import BellmanFord
from routenplanung.utils import constants


class TestBellmanFordGraph(unittest.TestCase):
    def test_source_target_nodes(self):
        bellford_graph, _ = create_bellford_graph()
        assert bellford_graph.source_node.label == "S"

    def test_default_edge_weights(self):
        bellford_graph, weighted_directed_graph = create_bellford_graph()
        for edge in weighted_directed_graph.edges:
            assert edge.weight is not None

    def test_length_distance_matrix_nodes(self):
        bellford_graph, weighted_directed_graph = create_bellford_graph()
        distance_matrix, _ = bellford_graph.execute_algorithm()
        assert len(distance_matrix.items()) == len(weighted_directed_graph.nodes)

    def test_distance_source_zero(self):
        bellford_graph, _ = create_bellford_graph()
        distance_matrix, _ = bellford_graph.execute_algorithm()
        assert distance_matrix.get("S") == 0

    def test_previous_nodes(self):
        bellford_graph, weighted_directed_graph = create_bellford_graph()
        _, previous_nodes = bellford_graph.execute_algorithm()
        assert len(previous_nodes) == len(weighted_directed_graph.nodes) - 1

    def test_non_weighted_graph(self):
        directed_graph = create_graph(directed=True)
        S, A, B, C, D = directed_graph.add_nodes(["S", "A", "B", "C", "D"])
        SB = directed_graph.add_edge(S, B)
        SA = directed_graph.add_edge(S, A)
        AC = directed_graph.add_edge(A, C)
        CD = directed_graph.add_edge(C, D)
        bellford_graph = BellmanFord(directed_graph, S)
        with pytest.raises(Exception) as exinfo:
            bellford_graph.execute_algorithm()
        assert str(exinfo.value) == constants.BELLFORD_EXCEPTION_ERROR


def create_bellford_graph() -> tuple[BellmanFord, Graph]:
    weighted_directed_graph = create_graph(weighted=True, directed=True)
    S, A, B, C, D, E = weighted_directed_graph.add_nodes(["S", "A", "B", "C", "D", "E"])
    SA = weighted_directed_graph.add_edge(S, A, 3)
    SB = weighted_directed_graph.add_edge(S, B, 1)
    BC = weighted_directed_graph.add_edge(B, C, 2)
    CS = weighted_directed_graph.add_edge(C, S, 3)
    CD = weighted_directed_graph.add_edge(C, D, -3)
    AE = weighted_directed_graph.add_edge(A, E, -2)
    return BellmanFord(weighted_directed_graph, S), weighted_directed_graph
