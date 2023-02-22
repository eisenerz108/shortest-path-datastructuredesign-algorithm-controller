import os
import sys
import unittest

from sqlalchemy import true

sys.path.append(os.path.dirname(__file__) + "/../../")  # Go to parent directory.

from datenstruktur.edge import DirectedEdge, Edge, WeightedEdge
from datenstruktur.graph import (
    BipartiteGraph,
    DirectedBipartiteGraph,
    DirectedGraph,
    Graph,
    WeightedBipartiteGraph,
    WeightedDirectedBipartiteGraph,
    WeightedDirectedGraph,
    WeightedGraph,
    create_graph,
)
from datenstruktur.node import Node

from datenstruktur.graphEX import AddEdgeException


class TestGraph(unittest.TestCase):
    """Tests Graph related functionality."""

    def test_info(self):
        """The info attribute stores information in the Graph."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        a = g.add_node("A")
        a.info = 5
        self.assertEqual(a.info, 5)

    def test_add_node_with_label(self):
        """Adds a Node to the Graph with provided 'label'."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        a = g.add_node("A")
        b = g.add_node("B")
        c = g.add_node("C")
        self.assertEqual(len(g.nodes), 3)

    def test_add_node_with_node(self):
        """Adds a Node to the Graph with provided node"""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        node_a = Node("A")
        node_b = Node("B")
        node_c = Node("C")
        a = g.add_node(node_a)
        b = g.add_node(node_b)
        c = g.add_node(node_c)
        self.assertEqual(len(g.nodes), 3)

    def test_add_nodes(self):
        """Adds multiple Node's to the Graph with 'labels'."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        g.add_nodes(["A", "B", "C", "D"])
        self.assertEqual(len(g.nodes), 4)

    def test_remove_node(self):
        """Removes 'node' (Node)."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        nodes = dict()
        to_add = ["A", "B", "C", "D"]
        vals = g.add_nodes(to_add)
        nodes.update(zip(to_add, vals))
        g.add_edges(
            [
                (nodes["A"], nodes["B"]),
                (nodes["A"], nodes["C"]),
                (nodes["A"], nodes["D"]),
            ]
        )
        self.assertEqual(nodes["A"].degree, 3)
        self.assertEqual(nodes["B"].degree, nodes["C"].degree)
        g.remove_node(nodes["A"])
        self.assertEqual(len(g.nodes), 3)
        self.assertEqual(nodes["B"].degree, 0)
        self.assertEqual(nodes["C"].degree, 0)
        self.assertEqual(nodes["D"].degree, 0)

    def test_get_node_neighbours(self):
        """Returns a list of Node neighbours for 'node' (Node)."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        nodes = dict()
        to_add = ["A", "B", "C", "D"]
        vals = g.add_nodes(to_add)
        nodes.update(zip(to_add, vals))
        g.add_edges(
            [
                (nodes["A"], nodes["B"]),
                (nodes["A"], nodes["C"]),
                (nodes["A"], nodes["D"]),
            ]
        )
        self.assertEqual(len(g.get_node_neighbours(nodes["A"])), 3)
        self.assertTrue(nodes["C"] in g.get_node_neighbours(nodes["A"]))
        g.remove_edge(nodes["A"], nodes["C"])
        self.assertEqual(len(g.get_node_neighbours(nodes["A"])), 2)
        g.remove_node(nodes["D"])
        self.assertEqual(len(g.get_node_neighbours(nodes["A"])), 1)

    def test_add_edge(self):
        """Adds an Edge between the Node 'src' and the Node 'dest'."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        nodes = dict()
        to_add = ["A", "B", "C", "D", "E"]
        vals = g.add_nodes(to_add)
        nodes.update(zip(to_add, vals))
        g.add_edge(nodes["A"], nodes["B"])
        e = Edge(nodes["D"], nodes["E"])
        g.add_edge(e)
        self.assertIsInstance(g.add_edge(nodes["A"], nodes["B"]), type(None))
        self.assertIsInstance(g.add_edge(e), type(None))
        self.assertEqual(nodes["A"].degree, nodes["B"].degree)
        self.assertIsInstance(g.add_edge(Node("F"), nodes["B"]), type(None))

    def test_add_edges(self):
        """Adds multiple Edge's to the Graph with 'labels'."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        nodes = dict()
        to_add = ["A", "B", "C", "D", "E"]
        vals = g.add_nodes(to_add)
        nodes.update(zip(to_add, vals))
        g.add_edges(
            [
                (nodes["A"], nodes["B"]),
                (nodes["A"], nodes["C"]),
                (nodes["B"], nodes["D"]),
                (nodes["C"], nodes["E"]),
            ]
        )
        self.assertEqual(nodes["A"].degree, 2)

    def test_get_edge(self):
        """Gets an undirected edge given source and destination Node."""
        g = create_graph()
        A, B, C = g.add_nodes(["A", "B", "C"])

        edge1, edge2 = g.add_edges([Edge(A, B), Edge(B, C)])

        AB = g.get_edge(A, B)
        BA = g.get_edge(B, A)
        AC = g.get_edge(A, C)

        self.assertEqual(edge1, AB)
        self.assertEqual(edge1, BA)
        self.assertFalse(AC in g.edges)

    def test_remove_edge(self):
        """Removes the Edge between Node 'src' and Node 'dest'."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        nodes = dict()
        to_add = ["A", "B", "C", "D", "E"]
        vals = g.add_nodes(to_add)
        nodes.update(zip(to_add, vals))
        g.add_edges(
            [
                (nodes["A"], nodes["B"]),
                (nodes["A"], nodes["C"]),
                (nodes["B"], nodes["D"]),
                (nodes["C"], nodes["E"]),
            ]
        )
        g.remove_edge(nodes["B"], nodes["A"])
        g.add_edge(nodes["B"], nodes["A"])
        g.remove_edge(nodes["A"], nodes["B"])
        self.assertEqual(nodes["A"].degree, 1)
        self.assertEqual(nodes["B"].degree, 1)

    def test_breadth_first_search(self):
        """Tests the BFS traversal given a start Node."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        nodes = dict()
        to_add = ["A", "B", "C", "D", "E"]
        vals = g.add_nodes(to_add)
        nodes.update(zip(to_add, vals))
        g.add_edges(
            [
                (nodes["A"], nodes["C"]),
                (nodes["A"], nodes["B"]),
                (nodes["B"], nodes["D"]),
                (nodes["C"], nodes["E"]),
            ]
        )

        type_gen = type(
            (lambda: (yield))()
        )  # Credits to https://forum.micropython.org/viewtopic.php?t=5538#p31934
        self.assertEqual(type(g.bfs(nodes["A"])), type_gen)

        bfs_traversal_list = [node for node in g.bfs(nodes["A"])]
        self.assertEqual(
            [nodes["A"], nodes["C"], nodes["B"], nodes["E"], nodes["D"]],
            bfs_traversal_list,
        )

    def test_depth_first_search(self):
        """Tests the DFS traversal given a start Node."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        nodes = dict()
        to_add = ["A", "B", "C", "D", "E"]
        vals = g.add_nodes(to_add)
        nodes.update(zip(to_add, vals))
        g.add_edges(
            [
                (nodes["A"], nodes["B"]),
                (nodes["A"], nodes["C"]),
                (nodes["B"], nodes["D"]),
                (nodes["C"], nodes["E"]),
            ]
        )

        type_gen = type(
            (lambda: (yield))()
        )  # Credits to https://forum.micropython.org/viewtopic.php?t=5538#p31934
        self.assertEqual(type(g.dfs(nodes["A"])), type_gen)

        dfs_traversal_list = [node for node in g.dfs(nodes["A"])]
        self.assertEqual(
            [nodes["A"], nodes["C"], nodes["E"], nodes["B"], nodes["D"]],
            dfs_traversal_list,
        )

    def test_detect_cycle(self):
        """Detects if the Graph contains a cycle and returns True or False."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        a = g.add_node("A")
        b = g.add_node("B")
        c = g.add_node("C")
        g.add_edges([(a, b), (b, c), (c, a)])

        self.assertEqual(g.detect_cycle(), True)

    def test_detect_cycle_negative(self):
        """Detects if the Graph contains a cycle and returns True or False."""
        g = create_graph(weighted=False, directed=False, bipartite=False)
        a = g.add_node("A")
        b = g.add_node("B")
        c = g.add_node("C")
        g.add_edges([(a, b), (b, c)])

        self.assertEqual(g.detect_cycle(), False)

    def test_get_connected_components(self):
        g = create_graph()
        a = g.add_node("A")
        b = g.add_node("B")
        c = g.add_node("C")
        g.add_edge(a, b)
        previous_nodes = g.nodes
        print(g.gcc())
        self.assertEqual(previous_nodes, g.nodes)
        self.assertEqual(2, len(g.gcc()))
        g.add_edge(b, c)
        self.assertEqual(1, len(g.gcc()))


class TestWeightedGraph(unittest.TestCase):
    """Tests WeightedGraph class related functionality."""

    def test_add_edge(self):
        g = create_graph(weighted=True)
        A, B, C, D = g.add_nodes(["A", "B", "C", "D"])
        AB = g.add_edge(A, B)
        CD = g.add_edge(C, D, 3)
        AC = g.add_edge(A, C, 10)

        self.assertEqual(AB.weight, 1)
        self.assertEqual(CD.weight, 3)
        AB.weight = 10
        self.assertEqual(AB.weight, AC.weight)
        self.assertEqual(AB.weight, g.get_edge(A, B).weight)
    
    def test_mst(self):
        g = create_graph(weighted=True)
        A, B, C, D = g.add_nodes(["A", "B", "C", "D"])
        AB = g.add_edge(A, B)
        BC = g.add_edge(B, C, 3)
        
        self.assertEqual(None, g.mst())
        
        CD = g.add_edge(C, D)

        AC = g.add_edge(A, C, 10)

        temp = g.mst()

        self.assertEqual(3, len(temp))

        self.assertEqual(temp, set([BC, CD, AC]))


class TestDirectedGraph(unittest.TestCase):
    """Tests DirectedGraph class related functionality."""

    def test_get_edge(self):
        """Gets a directed edge from given source to destination Node."""
        g = create_graph(directed=True)
        A, B, C = g.add_nodes(["A", "B", "C"])

        edge1 = g.add_edge(A, B)
        edge2 = g.add_edge(B, C)

        AB = g.get_edge(A, B)
        BA = g.get_edge(B, A)
        AC = g.get_edge(A, C)

        self.assertEqual(edge1, AB)
        self.assertNotEqual(edge1, BA)
        self.assertEqual(edge2, g.get_edge(B, C))
        self.assertFalse(AC in g.edges)
        self.assertTrue(isinstance(AC, type(None)))

    def test_remove_node(self):
        """See interfaces.Graph class."""
        g = create_graph(directed=True)
        A, B, C = g.add_nodes(["A", "B", "C"])

        edge1 = g.add_edge(A, B)
        edge2 = g.add_edge(B, C)
        edge3 = g.add_edge(C, A)

        self.assertTrue(isinstance(edge1, Edge))
        g.remove_node(A)
        self.assertTrue(isinstance(g.get_node_by_label("A"), type(None)))
        self.assertFalse(A in g.nodes)
        self.assertFalse(edge1 in g.edges)
        self.assertTrue(edge2 in g.edges)
        self.assertFalse(edge3 in g.edges)

    def test_get_node_neighbours(self):
        """See interfaces.DirectedGraph class."""
        g = create_graph(directed=True)

    def test_add_edge(self):
        """See interfaces.DirectedGraph class."""
        g = create_graph(directed=True)

        A, B, C = g.add_nodes(["A", "B", "C"])

        edge1 = g.add_edge(A, B)
        edge2 = g.add_edge(B, C)
        edge3 = g.add_edge(C, A)

        self.assertEqual(len(g.get_node_neighbours(A, "in")), 1)
        self.assertEqual(len(g.get_node_neighbours(A, "all")), 2)
        self.assertEqual(len(g.get_node_neighbours(A, "out")), 1)
        self.assertEqual(
            len(g.get_node_neighbours(A, "in")), len(g.get_node_neighbours(C, "out"))
        )

    def test_remove_edge(self):
        """See interfaces.DirectedGraph class."""
        g = create_graph(directed=True)

        A, B, C = g.add_nodes(["A", "B", "C"])

        edge1 = g.add_edge(A, B)
        edge2 = g.add_edge(B, C)

        g.remove_edge(A, B)
        self.assertTrue(isinstance(g.get_edge(A, B), type(None)))
        self.assertTrue(isinstance(edge2, DirectedEdge))
        self.assertTrue(edge2 in g.edges)
        g.remove_edge(edge2)
        self.assertFalse(edge2 in g.edges)
        self.assertTrue(isinstance(g.get_edge(B, C), type(None)))

    def test_detect_cycle(self):
        """See interfaces.DirectedGraph class."""
        # g = create_graph(directed=True)
        # g = create_graph(directed=True)

        # A, B, C = g.add_nodes(["A", "B", "C"])

        # edge1 = g.add_edge(A, B)
        # edge2 = g.add_edge(B, C)
        # edge3 = g.add_edge(A, C)

        # self.assertFalse(g.detect_cycle())

        # g.add_edge(C, A)

        # self.assertTrue(g.detect_cycle())

    def test_topological_sort(self):
        """See interfaces.DirectedGraph class."""
        g = create_graph(directed=True)
        g = create_graph(directed=True)

        A, B, C = g.add_nodes(["A", "B", "C"])

        edge1 = g.add_edge(A, B)
        edge2 = g.add_edge(B, C)

        self.assertEqual(g.toposort(), [A, B, C])


class TestWeightedDirectedGraph(unittest.TestCase):
    """Tests WeightedDirectedGraph class related functionality."""

    pass


class TestBipartiteGraph(unittest.TestCase):
    """Tests BipartiteGraph class related functionality."""
    def test_add_edge(self):
        g = create_graph(bipartite=True)
        r = g.add_r_nodes(['A','B','C'])
        l = g.add_l_nodes(['D','E','F'])
        g.add_edge(r[0],l[0])
        self.assertRaises(AddEdgeException, g.add_edge, r[1], r[2])

    def test_init(self):
        g = BipartiteGraph(['A', 'B', 'C'], ['D', 'E', 'F'])
        x = Node('x')
        y = Node('y')
        z = Node('z')
        xz = Edge(x, z)
        yz = Edge(y, z)
        g2 = BipartiteGraph([x, y], [z], [xz, yz])

class TestWeightedBipartiteGraph(unittest.TestCase):
    """Tests WeightedBipartiteGraph class related functionality."""

    pass


class TestDirectedBipartiteGraph(unittest.TestCase):
    """Tests DirectedBipartiteGraph class related functionality."""

    pass


class TestWeightedDirectedBipartiteGraph(unittest.TestCase):
    """Tests WeightedDirectedBipartiteGraph class related functionality."""

    pass


class TestFunctions(unittest.TestCase):
    """Functions that do not belong to the Graph class are tested here."""

    def test_create_graph(self):
        """Tests creating a Graph from a given setting."""
        g_uu = create_graph(weighted=False, directed=False, bipartite=False)
        g_wu = create_graph(weighted=True, directed=False, bipartite=False)
        g_ud = create_graph(weighted=False, directed=True, bipartite=False)
        g_wd = create_graph(weighted=True, directed=True, bipartite=False)
        g_buu = create_graph(weighted=False, directed=False, bipartite=True)
        g_bwu = create_graph(weighted=True, directed=False, bipartite=True)
        g_bud = create_graph(weighted=False, directed=True, bipartite=True)
        g_bwd = create_graph(weighted=True, directed=True, bipartite=True)

        self.assertIsInstance(g_uu, Graph)
        self.assertIsInstance(g_wu, WeightedGraph)
        self.assertIsInstance(g_ud, DirectedGraph)
        self.assertIsInstance(g_wd, WeightedDirectedGraph)
        self.assertIsInstance(g_buu, BipartiteGraph)
        self.assertIsInstance(g_bwu, WeightedBipartiteGraph)
        self.assertIsInstance(g_bud, DirectedBipartiteGraph)
        self.assertIsInstance(g_bwd, WeightedDirectedBipartiteGraph)

        # Check if non-boolean arguments passed to function.
        self.assertRaises(AssertionError, create_graph, 0, True, True)
        self.assertRaises(AssertionError, create_graph, True, 1, True)
        self.assertRaises(AssertionError, create_graph, True, True, 2)


if __name__ == "__main__":
    unittest.main(exit=False)
