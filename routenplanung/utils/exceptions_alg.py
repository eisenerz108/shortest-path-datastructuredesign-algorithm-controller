class WeightNotFoundError(Exception):
    """
    Exception raised in the input graph

    Args:
        Graph: Graph wich caused the error
        Message: Explenation of the error
    """

    def __init__(
        self, graph, message="Edge in the graph does not have an weight assigned to it"
    ):
        self.graph = graph
        self.message = message
        super().__init__(self.message)


class GraphNotDirected(Exception):
    """
    Exception to raised in the input graph

    Args:
        Graph:  Graph wich caused the error
        Message: Explenation of the error
    """

    def __init__(self, graph, message="Graph is not directed"):
        self.graph = graph
        self.message = message
        super().__init__(self.message)


class NegativeCycle(Exception):
    """
    Exception to raised in the input graph

    Args:
        Graph:  Graph wich caused the error
        Message: Explenation of the error
    """

    def __init__(self, graph, message="Graph contains a negative cycle"):
        self.graph = graph
        self.message = message
        super().__init__(self.message)


class GraphNotConnected(Exception):
    """
    Exception to raised in the input graph

    Args:
        Graph:  Graph wich caused the error
        Message: Explenation of the error
    """

    def __init__(self, graph, message="Graph is not connected"):
        self.graph = graph
        self.message = message
        super().__init__(self.message)
