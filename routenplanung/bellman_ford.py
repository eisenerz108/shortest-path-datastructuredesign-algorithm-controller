"""
Created Date : 27-May-22
"""
from algorithmus.options import Color
from datenstruktur.node import Node
from datenstruktur.graph import Graph, WeightedDirectedGraph
"""
Only selected WeightedDirectedGraph, due to the limitation regarding 
the detection of a negative cycle set by undirected Graphs,
which would be the only real addon of the algorithm if compared to Dijkstra
"""
from routenplanung.RoutenPlanungAlgorithm import RoutenPlanungAlgorithm 
from routenplanung.utils import constants
from algorithmus.algorithm import Algorithm

from tabulate import tabulate
import pandas as pd

class BellmanFord(RoutenPlanungAlgorithm):
    """
    Creates an instance of the Bellman-Ford Algorithm
            
    Args:
        graph: Graph structure with all the nodes, edges
        source: Source Vertex; i.e. starting node from which all corresponding shortest paths will be calculated
    """

    need_graph = WeightedDirectedGraph
    need_start = True
    need_end = True
    """
    need_end = True, in order to prevent programm from crashing, details down below; the algorithm itself does not need an end-/dest-node, 
    albeit if none is provided the programm crashes 
    """
     
    def get_info(self) -> str:
        return constants.BELLFORD_RUNNING_INFO

    def run(self, graph: Graph, start_node: Node, end_node: Node ) -> bool:
        """
        Runs the whole Bellman-Ford Algorithm

        Args:
            graph: Graph structure with all the nodes, edges
            start_node: Source Node
            end_node: needed due to otherwise RoutenPlanungAlgorithm conflict 

        Returns :
            bool : True for successful run, False for unsuccessful run. 
        """
        self.initialize(graph, start_node, end_node )
        
        if len(self.graph.nodes) == 0:
            self.show_error(constants.COMMON_EMPTY_GRAPH_ERROR)
            return False
        """
        checks whether or not nodes are existing
        """       

        if isinstance(self.graph, WeightedDirectedGraph):
            all_nodes = self.graph.nodes
            all_edges = self.graph.edges
            infinity = float("inf")
        
            for each_node in all_nodes:
                self.distance[each_node.label] = infinity
            self.distance[self.start_node.label] = 0
            """
            1. step (initialization): 
                - every node except start_node initialized to inf 
                - start_node = 0 
            """
            
            for i in range((len(all_nodes)) -1):       
                """
                2. step (general BellmanFord Algorithm):
                - most important part => relaxation
                """
                self.color_node(start_node, Color.marked)
                self.display()
                for edge in all_edges:
                    (u,v) = edge.get_endpoints()
                    if (self.distance[u.label] == infinity):
                        self.color_edge(self.graph.get_edge(u,v), Color.current)
                        self.display()
                        self.color_edge(self.graph.get_edge(u,v), Color.deactivated )
                        self.display()
                    else:
                        self.color_edge(self.graph.get_edge(u,v), Color.current)
                        self.display()
                        self.color_edge(self.graph.get_edge(u,v), Color.marked)
                        self.display()
                        tempDist = self.distance[u.label] + self.graph.get_edge(u,v).weight
                        if (tempDist < self.distance[v.label]):
                            self.distance[v.label] = tempDist 
                            self.color_edge(self.graph.get_edge(u,v), Color.selected)
                            """
                            selected for update
                            """
                            self.display()
                            self.add_log("A change of distances")
            for edge in all_edges: 
                """
                3. step (negativ cycle detection, if existing)
                """
                (u,v) = edge.get_endpoints()
                if self.distance[u.label] + self.graph.get_edge(u,v).weight < self.distance [v.label]:
                    self.show_error(constants.NEG_CYCLE_ERROR)
                    return False
                            

            self.print_final_log(self.distance)     
          
            return True
        else:
            self.show_error(constants.BELLFORD_EXCEPTION_ERROR)
            raise Exception(constants.BELLFORD_EXCEPTION_ERROR) 


 

    def print_final_log(self, distance):
        self.add_log("Displaying SP from Source to every other Node")
        for key, value in distance.items():
            distance[key] = [value]
        distance_df = pd.DataFrame(distance)
        self.add_log(tabulate(distance_df, headers="keys", tablefmt="github"))
 
      
      
"""
error if no end node is specified:
- algorithm won't run 
- any changes within the same instance of gave is impossible;
- need to restart 
- all due to self.end_node_label = end_node.label within the initialization step in RoutenPlanungAlgorithm
Workaround:
- specify an end_node, won't affect the algorihm's performance nor its correctness 
"""
