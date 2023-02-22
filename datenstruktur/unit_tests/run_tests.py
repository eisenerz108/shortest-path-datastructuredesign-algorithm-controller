import os
import sys
from unittest import TestLoader as TL
from unittest import TextTestRunner as TTR

sys.path.append(os.path.dirname(__file__) + "/../")  # Go to parent directory.

import unit_tests_edge
import unit_tests_graph
import unit_tests_node

if __name__ == "__main__":
    node_suite = TL().loadTestsFromModule(unit_tests_node)
    edge_suite = TL().loadTestsFromModule(unit_tests_edge)
    graph_suite = TL().loadTestsFromModule(unit_tests_graph)

    TTR().run(node_suite)
    TTR().run(edge_suite)
    TTR().run(graph_suite)
