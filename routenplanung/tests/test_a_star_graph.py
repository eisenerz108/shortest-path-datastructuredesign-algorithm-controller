"""
Create Date : 28-Jul-22

"""
import unittest
from unittest import TestCase

import pytest
from datenstruktur.graph import Graph, create_graph

from routenplanung.a_star import AStar
from routenplanung.utils import constants


class TestAstar(unittest.TestCase):
    def test_source_target_nodes(self):
        weighted_graph, S, T, heuristics = create_weighted_graph()
        astar = AStar()
        astar.run_test(
            graph=weighted_graph, start_node=S, end_node=T, heuristics=heuristics
        )
        assert astar.start_node.label == "S"
        assert astar.end_node.label == "T"

    def test_default_edge_weights(self):
        weighted_graph, S, T, heuristics = create_weighted_graph()
        for edge in weighted_graph.edges:
            assert edge.weight is not None

    def test_length_distance_matrix_nodes(self):
        weighted_graph, S, T, heuristics = create_weighted_graph()
        astar = AStar()
        astar.run_test(
            graph=weighted_graph, start_node=S, end_node=T, heuristics=heuristics
        )
        assert len(astar.distance.items()) == len(weighted_graph.nodes)

    def test_distance_source_zero(self):
        weighted_graph, S, T, heuristics = create_weighted_graph()
        astar = AStar()
        astar.run_test(
            graph=weighted_graph, start_node=S, end_node=T, heuristics=heuristics
        )
        assert astar.distance.get("S") == 0

    def test_non_weighted_graph(self):
        directed_graph = create_graph(directed=True)
        S, A, B, C, T = directed_graph.add_nodes(["S", "A", "B", "C", "T"])
        heuristics = {S: 6, A: 2, B: 1, C: 0, T: 0}
        SB = directed_graph.add_edge(S, B)
        SA = directed_graph.add_edge(S, A)
        AC = directed_graph.add_edge(A, C)
        CT = directed_graph.add_edge(C, T)
        astar = AStar()
        with pytest.raises(Exception) as exinfo:
            astar.run_test(
                graph=directed_graph, start_node=S, end_node=T, heuristics=heuristics
            )
        assert str(exinfo.value) == constants.ASTAR_EXCEPTION_ERROR

    def test_previous_nodes(self):
        weighted_graph, S, T, heuristics = create_weighted_graph()
        astar = AStar()
        astar.run_test(
            graph=weighted_graph, start_node=S, end_node=T, heuristics=heuristics
        )
        assert len(astar.previous_nodes) == len(weighted_graph.nodes) - 1

    def test_target_node_cost(self):
        weighted_graph, S, T, heuristics = create_weighted_graph()
        astar = AStar()
        astar.run_test(
            graph=weighted_graph, start_node=S, end_node=T, heuristics=heuristics
        )
        assert astar.distance.get("T") == 8


def create_weighted_graph():
    weighted_graph = create_graph(weighted=True)
    S, A, B, C, T = weighted_graph.add_nodes(["S", "A", "B", "C", "T"])
    heuristics = {S: 8, A: 4, B: 3, C: 2, T: 1}
    SB = weighted_graph.add_edge(S, B, 1)
    SA = weighted_graph.add_edge(S, A, 3)
    AC = weighted_graph.add_edge(A, C, 4)
    CT = weighted_graph.add_edge(C, T)
    return weighted_graph, S, T, heuristics
