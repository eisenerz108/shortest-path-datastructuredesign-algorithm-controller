"""
Created Date : 16-Jun-22
"""

import numpy as np
import pandas as pd
from algorithmus.algorithm import Algorithm
from algorithmus.options import Color, Pattern
from datenstruktur.graph import Graph
from datenstruktur.node import Node
from tabulate import tabulate

from routenplanung.utils import constants
from routenplanung.utils.priority_queue import PriorityQueue


class RoutenPlanungAlgorithm(Algorithm):
    def initialize(self, graph: Graph, start_node: Node, end_node: Node):
        """
        Initializes all instance attributes.

        Args:
            graph: Graph structure with all the nodes, edges
            start_node: Source Node
            end_node: Target (Destination) Node

        Returns :
            None
        """
        self.graph = graph
        self.start_node = start_node
        self.end_node = end_node
        self.distance = dict()
        self.previous_nodes = dict()
        self.marked = set()
        self.end_node_label = end_node.label
        self.number_of_iterations = 0

    def explore_neighbors(
        self,
        current_node: Node,
        unseen_nodes: list,
        pq: PriorityQueue,
        is_dijkstra: True,
        heuristics=None,
    ):
        """
        Method for the Dijkstra & A-Star Algorithm to explore the neighbors of the selected Node.
        The shortest path of the neighbor node will be added to the Priority Queue.

        Args:
            current_node: The node of which the neighbors will be explored.
            unseen_nodes: List of the unseen nodes which are yet to be explored.
            pq: Priority Queue where the new unseen nodes will be added.
            is_dijkstra : Boolean to check if the Algorthm running is Dijkstra or A-Star
            heuristics : Pass the Heuristics for the A-Star Algorithm

        Returns :
            None
        """
        for neighbor in range(len(current_node.neighbours)):
            neighbor_node = current_node.neighbours[neighbor]
            if neighbor_node not in self.marked:
                self.color_node(neighbor_node, Color.marked)
            self.display()
            dist = self.graph.get_edge(current_node, neighbor_node).weight
            if not is_dijkstra:
                node_heuristic = heuristics.get(neighbor_node)
            else:
                node_heuristic = 0

            if neighbor_node in unseen_nodes:
                self.number_of_iterations += 1
                old_cost = self.distance[neighbor_node.label]
                new_cost = self.distance[current_node.label] + dist
                new_heuristic_cost = new_cost + node_heuristic

                if new_cost < old_cost:
                    self.previous_nodes[neighbor_node] = current_node
                    if is_dijkstra:
                        # Only the Edge Cost is considered in the Priority Queue.
                        pq.update(neighbor_node, new_cost)
                    else:
                        # Heuristics along with the Edge Cost is considered in the Priority Queue
                        pq.update(neighbor_node, new_heuristic_cost)
                    self.distance[neighbor_node.label] = new_cost

    def shortest_path_log(self, previous_nodes, S, T, distance):

        """
        Gives the shortest path in the Log : From S -> T
        For Example : 1 -> 4 -> 3 -> 7 where 1 is S and 7 is T

         Args:
             previous_nodes : Previous node of the current node
             S : Source Node
             T : Target Node
             distance : Dictionary which tell the shortest cost of the respective nodes.

         Returns :
             None
        """

        shortest_path = [T]
        while S not in shortest_path:
            last_node = shortest_path[-1]
            shortest_path.append(previous_nodes[last_node])

        shortest_path = shortest_path[::-1]
        self.highlight_path_nodes_edges(shortest_path)
        target_minimum_cost = str(np.array(distance[self.end_node_label]).item())
        log1 = (
            "Shortest Path from Start Node to End Node at a cost of : "
            + target_minimum_cost
            + " would be : "
        )
        self.add_log(log1)
        self.add_log(" -> ".join(node.label for node in shortest_path))

    def cost_to_each_node_log(self, distance):

        """
        Display the shortest cost to each node :
        For Ex - 2 : 2, 4 : 2, 5 : 1 etc.

        Args:
            distance : Dictionary which tell the shortest cost of the respective nodes.

        Returns :
           None
        """

        self.add_log(constants.SHORTEST_COST_LOG)
        for key, value in distance.items():
            distance[key] = [value]
        distance_df = pd.DataFrame(distance)
        self.add_log("\n" + tabulate(distance_df, headers="keys", tablefmt="github"))

    def highlight_path_nodes_edges(self, shortest_path):

        """
        Changes the Color and the Pattern of the Nodes/Edges selected for the final Path.

        Args:
           shortest_path : List of the nodes of the Shortest Path.

        Returns :
           None
        """

        prev_node = None
        for index, node in enumerate(shortest_path):
            self.color_node(node, Color.selected)
            self.change_node_pattern(node, Pattern.dashed)
            if index > 0:
                self.change_edge_pattern(
                    self.graph.get_edge(node, prev_node), Pattern.dashed
                )
                self.color_edge(self.graph.get_edge(node, prev_node), Color.selected)
            prev_node = node
