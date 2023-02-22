"""
Created Date : 24-June-22
"""

import numpy as np
import pandas as pd
from algorithmus.algorithm import Algorithm
from algorithmus.options import Color
from datenstruktur.graph import Graph, WeightedGraph
from datenstruktur.node import Node
from tabulate import tabulate

from routenplanung.RoutenPlanungAlgorithm import RoutenPlanungAlgorithm
from routenplanung.utils import constants
from routenplanung.utils.priority_queue import PriorityQueue


class AStar(RoutenPlanungAlgorithm):

    need_start = True
    need_end = True
    need_graph = Graph

    def get_info(self) -> str:
        return constants.ASTAR_RUNNING_INFO

    def calculate_heuristics(self, weighted_graph, S, T, controller, drawboard):
        algorithm = Algorithm(controller, drawboard)
        T_coords = algorithm.get_node_coords(T)
        heuristics = dict()
        for node in weighted_graph.nodes:
            t_coords_arr = np.array(T_coords)
            node_arr = np.array(algorithm.get_node_coords(node))
            heuristics[node] = np.linalg.norm(node_arr - t_coords_arr) / 100
        return heuristics

    def run_test(self, graph: Graph, start_node: Node, end_node: Node, heuristics):
        self.heuristics = heuristics
        self.is_test = True
        self.run(graph, start_node, end_node)

    def run(self, graph: Graph, start_node: Node, end_node: Node) -> bool:

        """
        Runs the whole A Star Algorithm

        Args:
            graph: Graph structure with all the nodes, edges
            start_node: Source Node
            end_node: Target (Destination) Node

        Returns :
            bool : True for successful run, False for Unsuccessful run.
        """
        self.initialize(graph, start_node, end_node)
        if not self.is_test:
            self.heuristics = self.calculate_heuristics(
                graph, start_node, end_node, self.controller, self.drawboard
            )
        self.heuristic_log(self.heuristics)
        # Show error if there are no Nodes
        if len(self.graph.nodes) == 0:
            self.show_error(constants.COMMON_EMPTY_GRAPH_ERROR)
            return False

        if isinstance(self.graph, WeightedGraph):
            all_nodes = self.graph.nodes
            unseen_nodes = list()
            infinity = float("inf")

            for each_node in all_nodes:
                self.distance[each_node.label] = infinity
                unseen_nodes.append(each_node)

            self.distance[self.start_node.label] = 0
            pq = PriorityQueue()
            pq.push(self.start_node, 0)
            current_node = pq.pop()

            while len(unseen_nodes) > 0 and current_node != end_node:
                self.marked.add(current_node)
                self.color_node(current_node, Color.current)
                self.add_log(f"Exploring the Node {current_node.label}")
                self.display()
                unseen_nodes.remove(current_node)

                self.explore_neighbors(
                    current_node, unseen_nodes, pq, False, self.heuristics
                )
                current_node = pq.pop()
            self.color_node(end_node, Color.current)
            self.shortest_path_log(
                self.previous_nodes, start_node, end_node, self.distance
            )
            self.add_log("Number of iterations = " + str(self.number_of_iterations))
            return True
        else:
            self.show_error(constants.ASTAR_EXCEPTION_ERROR)
            raise Exception(constants.ASTAR_EXCEPTION_ERROR)

    def heuristic_log(self, distance):
        hiu = dict()
        self.add_log("Displaying the value of the heuristic for each node:")
        for key, value in distance.items():
            hiu[key] = [value]
        distance_df = pd.DataFrame(hiu)
        self.add_log(tabulate(distance_df, headers="keys", tablefmt="github"))
