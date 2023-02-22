"""
Created Date : 23-Jun-22
"""

# Common Constants
COMMON_EMPTY_GRAPH_ERROR = "Graph is empty.\n Nothing to do here."
NEG_CYCLE_ERROR = 'Graph contains an negative cycle.'
NOT_CONNECTED_ERROR = 'Graph is not connected.'
NO_EDGE_WEIGHT = 'All Edges need edge-weights'
SHORTEST_COST_LOG = "Displaying Shortest Cost to each Node"

# A-STAR Algorithm Constants
ASTAR_EXCEPTION_ERROR = 'Only "WeightedGraph" can be used for A-Star Algorithm'
ASTAR_RUNNING_INFO = "Running A Star Algorithm"
ASTAR_RUNNING_INFO = (
    "Running A* Algorithm \n LEGENDS : \n Red Node : Current Node \n Green Node : In Queue Node \n Orange Node : Final Path Node \n "
    " Orange Edge : Final Path"
)


# Dijkstra Algorithm Constants
DA_EXCEPTION_ERROR = 'Only "WeightedGraph" can be used for Dijkstra Algorithm'
DA_RUNNING_INFO = (
    "Running Dijkstra Algorithm \n LEGENDS : \n Red Node : Current Node \n Green Node : In Queue Node \n Orange Node : Final Path Node \n "
    " Orange Edge : Final Path"
)
# BellFord Algorithm Constants
BELLFORD_EXCEPTION_ERROR = 'Only "WeightedDirectedGraph" can be used for Bellman-Ford-Algorithm'
BELLFORD_RUNNING_INFO = "Running Bellman Ford Algorithm"
# Floyd Warshall Constants
FW_DIRECTED_ERROR = 'Only "DirectedGraph" can be used for Floyd-Warshall-Algorithm'
