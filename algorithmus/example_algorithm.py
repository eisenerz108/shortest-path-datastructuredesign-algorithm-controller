import random

from datenstruktur.graph import (
    BipartiteGraph,
    DirectedGraph,
    Graph,
    WeightedBipartiteGraph,
    WeightedGraph,
)
from datenstruktur.node import Node

from algorithmus.algorithm import Algorithm
from algorithmus.options import Color, Pattern


class Example_Algorithm(Algorithm):

    need_start = True
    need_end = False
    need_graph = Graph

    def get_info(self) -> str:
        return "Example:\n The algorithm does something.\nThe capacities have no meaning.\nd: recursion depth\n\ngreen: start node\nred: current path\nblue: visited paths"

    def run(self, graph: Graph, start_node: Node, end_node: Node):
        self.init_graph(graph)
        self.graph = graph
        new_nodes = list()
        # handeling and setting up given graph:
        if len(self.graph.nodes) == 0:
            self.show_error("Graph is empty.\n Nothing to do here.")
            return False

        if start_node is not None:
            self.start_node = start_node
        else:
            self.start_node = random.choice(list(self.graph.nodes))
            label = "Start\n" + self.start_node.label
            self.update_label(self.start_node, label, overwrite=True)

        # random example algorithm
        self.marked = set()
        self.marked.add(self.start_node)
        self.color_node(self.start_node, Color.marked)
        coords = self.get_node_coords(self.start_node)
        self.display()
        if isinstance(self.graph, BipartiteGraph):
            if self.start_node in self.graph.l_nodes:
                new_node = self.create_node(
                    str(len(graph.nodes) + 1), coords=coords, is_L=False
                )
            else:
                new_node = self.create_node(
                    str(len(graph.nodes) + 1), coords=coords, is_L=True
                )
        else:
            new_node = self.create_node(str(len(graph.nodes) + 1), coords=coords)

        self.update_label(new_node, "new")
        e = self.create_edge(self.start_node, new_node)
        self.display()
        self.change_edge_weight(e, 1 / 3, str(1 / 3))
        self.color_edge(e, Color.color2)
        self.display()
        self.delete_edge(e)
        self.display()
        self.create_edge(self.start_node, new_node)
        self.display()
        self.add_log("Calculating weights from distances")
        self.dist_to_weight()
        self.display()
        for i in range(5):
            new_node = self.create_node(str(len(graph.nodes) + 1), coords=coords)
            new_nodes.append(new_node)
        self.add_log("3")
        self.display()
        for i in new_nodes:
            new_node = self.delete_node(i)
        self.add_log("2")
        self.display()
        for i in range(5):
            new_node = self.create_node(str(len(graph.nodes) + 1), coords=coords)
        self.add_log("1")
        self.display()
        self.add_log("Weee!")
        self.rec_color(self.start_node, 1)

        self.display()

        self.delete_node(self.start_node)

        self.show_info("Finished!")
        return True

    def rec_color(self, node: Node, depth):
        """Recursive helper method going through all neighbours."""

        if isinstance(self.graph, DirectedGraph):
            neighbours = self.graph.get_node_neighbours(node, "out")
        else:
            neighbours = self.graph.get_node_neighbours(node)
        self.change_node_size(node, 4)
        self.add_log("Depth: " + str(depth))
        self.display()
        for n in neighbours:
            if n not in self.marked:
                self.marked.add(n)
                e = self.graph.get_edge(node, n)
                self.color_edge(e, Color.visited)
                self.color_edge_weight(e, Color.visited)
                self.change_edge_pattern(e, Pattern.dotted)
                self.change_node_pattern(n, Pattern.dashed)
                self.color_node(n, Color.current)
                if isinstance(self.graph, WeightedGraph):
                    self.change_edge_weight(e, e.weight, "1/" + str(e.weight))
                self.rec_color(n, depth + 1)
        self.change_node_size(node, 3)
        self.change_node_pattern(node, Pattern.solid)
        self.color_node(node, Color.visited)
        self.display()
