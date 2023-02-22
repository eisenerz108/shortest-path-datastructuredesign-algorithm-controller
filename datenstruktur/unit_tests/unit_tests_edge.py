import os
import sys
import unittest

sys.path.append(os.path.dirname(__file__) + "/../../")  # Go to parent directory.

from datenstruktur.edge import DirectedEdge, Edge, WeightedEdge
from datenstruktur.node import Node


class TestEdge(unittest.TestCase):
    """Tests Edge class related functionality."""

    def test_get_endpoints(self):
        """Tests if a frozenset of source and destination Node is returned."""
        A, B, C = map(Node, ["A", "B", "C"])

        edge_endpoints = Edge(A, B).get_endpoints()
        edge_endpoints_self_loop = Edge(C, C).get_endpoints()

        self.assertTrue(isinstance(edge_endpoints, frozenset))
        self.assertEqual(edge_endpoints, frozenset([B, A]))
        self.assertEqual(len(edge_endpoints_self_loop), 1)


class TestDirectedEdge(unittest.TestCase):
    """Tests DirectedEdge class related functionality."""

    pass


class TestWeightedEdge(unittest.TestCase):
    """Tests WeightedEdge class related functionality."""

    pass


if __name__ == "__main__":
    unittest.main(exit=False)
