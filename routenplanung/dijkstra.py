"""
Created Date : 05-May-22
"""

from algorithmus.options import Color
from datenstruktur.graph import Graph, WeightedGraph
from datenstruktur.node import Node

from routenplanung.RoutenPlanungAlgorithm import RoutenPlanungAlgorithm
from routenplanung.utils import constants
from routenplanung.utils.priority_queue import PriorityQueue


class Dijkstra(RoutenPlanungAlgorithm):

    need_start = True
    need_end = True
    need_graph = Graph

    def get_info(self) -> str:
        return constants.DA_RUNNING_INFO

    def run(self, graph: Graph, start_node: Node, end_node: Node) -> bool:

        """
        Runs the whole Dijkstra Algorithm

        Args:
            graph: Graph structure with all the nodes, edges
            start_node: Source Node
            end_node: Target (Destination) Node

        Returns :
            bool : True for successful run, False for Unsuccessful run.
        """
        self.initialize(graph, start_node, end_node)

        # Show error if there are no Nodes
        if len(self.graph.nodes) == 0:
            self.show_error(constants.COMMON_EMPTY_GRAPH_ERROR)
            return False

        # Check if the Instance of the Graph is Weighted, else throw an error.
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

            while len(unseen_nodes) > 0:
                current_node = pq.pop()
                self.marked.add(current_node)
                self.color_node(current_node, Color.current)
                self.add_log(f"Exploring the Node {current_node.label}")
                self.display()
                unseen_nodes.remove(current_node)

                # Exploring the Neighbor of the Current Nodes
                self.explore_neighbors(current_node, unseen_nodes, pq, True)

            self.cost_to_each_node_log(self.distance)
            self.shortest_path_log(
                self.previous_nodes, start_node, end_node, self.distance
            )
            self.add_log("Number of iterations = " + str(self.number_of_iterations))

            return True
        else:
            self.show_error(constants.DA_EXCEPTION_ERROR)
            raise Exception(constants.DA_EXCEPTION_ERROR)
