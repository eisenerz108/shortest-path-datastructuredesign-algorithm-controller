"""
Created Date : 16-Jun-22
@author : Oskar Besler
"""

from algorithmus.algorithm import Algorithm
from algorithmus.options import Color, Pattern
from datenstruktur.graph import DirectedGraph

from routenplanung.utils import constants as c


class FloydWarshall(Algorithm):

    need_start = False
    need_end = False
    need_graph = DirectedGraph

    def get_info(self):
        return "All Pairs Shortest Paths"

    def run(self, graph: DirectedGraph, start_node, end_node):

        """
        Function to fetch all shortest paths from every node to every node

        Args:
            The Graph to perform the algorithm on

        Returns:
            Boolean: Returns True, if the algorithm was succesfull and False otherwise.
        """
        self.graph = graph

        if isinstance(self.graph, DirectedGraph):

            if len(self.graph.nodes) == 0:
                self.show_error(c.COMMON_EMPTY_GRAPH_ERROR)
                return False

            distance = dict()
            edges_label = dict()
            path = dict()
            all_edges = self.graph.edges
            all_nodes = self.graph.nodes
            visited = []
            all_labels = []
            infinity = float("inf")

            for node in all_nodes:
                all_labels.append(node.label)
            if not (len(self.graph.get_strongly_connected_components()) < 2):
                self.show_error(c.NOT_CONNECTED_ERROR)
                return False

            for i in all_labels:
                for j in all_labels:
                    if i == j:
                        distance[(i, j)] = 0
                    elif (i, j) not in distance:
                        distance[(i, j)] = infinity
                    path[(i, j)] = [(i, j)]

            for edge in all_edges:
                endpoints = edge.get_endpoints()
                try:
                    edges_label[(endpoints[0].label, endpoints[1].label)] = endpoints
                    distance[(endpoints[0].label, endpoints[1].label)] = edge.weight
                except:
                    self.show_error(c.NO_EDGE_WEIGHT)
                    return False

            for k in all_labels:
                visited.append(k)
                for i in all_labels:

                    for j in all_labels:
                        if distance[(i, j)] <= (distance[(i, k)] + distance[(k, j)]):
                            distance[(i, j)] = distance[(i, j)]
                        else:
                            distance[(i, j)] = distance[(i, k)] + distance[(k, j)]
                            path[(i, j)].clear()
                            path[(i, j)].extend(path[(i, k)])
                            path[(i, j)].extend(path[(k, j)])
                # Start visualisation for current set k
                for v in visited:
                    self.color_node(self.graph.get_node_by_label(v), Color.color2)
                    self.display()
                for v in visited:
                    self.color_node(self.graph.get_node_by_label(v), Color.default)
                self.display()
                for key in path:
                    if key[0] != key[1]:
                        self.color_node(
                            self.graph.get_node_by_label(key[0]), Color.current
                        )
                        self.color_node(
                            self.graph.get_node_by_label(key[1]), Color.visited
                        )
                    else:
                        self.color_node(
                            self.graph.get_node_by_label(key[0]), Color.current
                        )
                    self.display()
                    for elem in path[key]:
                        if (elem[0], elem[1]) in edges_label:
                            edge = edges_label[(elem[0], elem[1])]
                            self.change_edge_pattern(
                                self.graph.get_edge(edge[0], edge[1]), Pattern.dotted
                            )
                            self.display()
                        if elem[0] != key[0]:
                            self.color_node(
                                self.graph.get_node_by_label(elem[0]), Color.marked
                            )
                            self.display()
                    for elem in path[key]:
                        self.color_node(
                            self.graph.get_node_by_label(elem[0]), Color.default
                        )
                        self.color_node(
                            self.graph.get_node_by_label(elem[1]), Color.default
                        )
                        if (elem[0], elem[1]) in edges_label:
                            edge = edges_label[(elem[0], elem[1])]
                            self.change_edge_pattern(
                                self.graph.get_edge(edge[0], edge[1]), Pattern.solid
                            )
                    self.display()

            for i in all_labels:
                if distance[(i, i)] < 0:
                    self.show_error(c.NEG_CYCLE_ERROR)
                    return False
            return True
        else:
            self.show_error(c.FW_DIRECTED_ERROR)
            return False
