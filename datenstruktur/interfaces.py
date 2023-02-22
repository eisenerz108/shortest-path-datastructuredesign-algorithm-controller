from abc import ABC, abstractmethod
from typing import overload


class Node(ABC):
    """Creates a Node.

    Attributes:
        info: Is of any type and can be used for storing additional information.
        neighbours: Is a list of all Neighbours a Node has.
        in_degree: Degree of Incoming Edges.
        out_degree: Degree of outgoing Edges.
        degree: Degree of all edges.
    """

    @property
    @abstractmethod
    def info(self):
        """The info attribute stores the value(s) of the Node."""

    @info.setter
    @abstractmethod
    def info(self, val):
        """Sets the info attribute of the Node to 'val'."""

    @property
    @abstractmethod
    def degree(self):
        """The degree attribute."""

    @property
    @abstractmethod
    def in_degree(self):
        """The in_degree attribute."""

    @property
    @abstractmethod
    def out_degree(self):
        """The out_degree attribute."""

    @abstractmethod
    def get_neighbours(self):
        """The Neighbours attribute safes a list of neighbours"""

    @abstractmethod
    def has_edge(self, to_node):
        """Checks whether an Edge to 'to_node' (Node) exists."""
        pass


class Edge(ABC):
    """Creates an Edge.

    Args:
        src_node: Source Node.
        dest_node: Target Node.

    Attributes:
        info: Is of any type and can be used for storing additional information.
    """

    @property
    @abstractmethod
    def info(self):
        """The info attribute stores the value(s) of the Edge."""

    @info.setter
    @abstractmethod
    def info(self, val):
        """Sets the info attribute of the Edge to 'val'."""

    @abstractmethod
    def get_endpoints(self):
        """Returns an unsorted, immutable set of source and destination Node."""
        pass


class DirectedEdge(Edge):
    """Creates a directed Edge.

    Args:
        src_node: Source Node.
        dest_node: Target Node.
    """

    @abstractmethod
    def get_head_node(self):
        """Returns the source Node of the Edge."""
        pass

    @abstractmethod
    def get_tail_node(self):
        """Returns the destination Node of the Edge."""
        pass


class WeightedEdge(Edge):
    """Creates a weighted Edge.

    Args:
        weight : Weight value defaulting to 1.
        src_node: Source Node.
        dest_node: Target Node.

    Attributes:
        weight (float): A float storing the weight of the Edge.
    """

    @property
    @abstractmethod
    def weight(self):
        """The weight attribute stores the weight of the Edge."""

    @weight.setter
    @abstractmethod
    def weight(self, val: float):
        """Sets the weight attribute of the Edge to 'val'."""


class DirectedWeightedEdge(DirectedEdge, WeightedEdge):
    """Creates a directed and weighted Edge.

    Args:
        weight : Weight value defaulting to 1.
        src_node: Source Node.
        dest_node: Target Node.

    Attributes:
        weight (float): A float storing the weight of the Edge.
    """


class Graph(ABC):
    """Creates an undirected, unweighted Graph.

    Args:
        nodes: Stores the Nodes of the Graph, defaulting to a set()
        edges: Stores the Edges of the Graph, defaulting to a set()

    Attributes:
        info: Is of any type and can be used for storing additional information.
    """

    @property
    @abstractmethod
    def info(self):
        """The info attribute stores information in the Graph."""

    @info.setter
    @abstractmethod
    def info(self, val):
        """Sets the info attribute of the Graph to 'val'."""

    @abstractmethod
    def add_node(self, label):
        """Adds a Node to the Graph with provided 'label', label can also be a node."""
        pass

    @abstractmethod
    def add_nodes(self, labels):
        """Adds multiple Node's to the Graph with 'labels'.
        TODO: Expand this docstring (Args, Returns, ...)."""
        pass

    @abstractmethod
    def remove_node(self, node):
        """Removes 'node' (Node)."""
        pass

    @abstractmethod
    def get_node_neighbours(self, node):
        """Returns a list of Node neighbours for 'node' (Node)."""
        pass

    @abstractmethod
    def add_edge(self, src, dest):
        """Adds an Edge between the Node 'src' and the Node 'dest'."""
        pass

    @overload
    @abstractmethod
    def add_edge(self, new_edge):
        """Adds an Edge 'new_edge' by creating a new edge with the same parameters and returning it."""
        pass

    def add_edges(self, edges):
        """Adds multiple Edge's to the Graph with 'labels'."""
        pass

    def get_edge(self, src, dest):
        """Returns the undirected Edge between two Nodes.

        Args:
            src: Source Node.
            dest: Target Node.

        Returns:
            Edge in the Graph between 'src' and 'dest', or None if such an Edge doesn't exist.
        """
        pass

    @abstractmethod
    def remove_edge(self, src, dest):
        """Removes the Edge between Node 'src' and Node 'dest'."""
        pass

    @abstractmethod
    def breadth_first_search(self, start):
        """Traverses the graph in BFS order given a start Node.

        Args:
            start: Start Node.

        Yields:
            Next Node in the order of BFS traversal.
        """
        pass

    @abstractmethod
    def depth_first_search(self, start):
        """Traverses the graph in DFS order given a start Node.

        Args:
            start: Start Node.

        Yields:
            Next Node in the order of DFS traversal.
        """
        pass

    @abstractmethod
    def detect_cycle(self):
        """Detects if the Graph contains a cycle and returns True or False.

        Returns:
            True or False.
        """
        pass

    @abstractmethod
    def get_connected_components(self):
        """Detects and returns connected components as seperate lists.

        Returns: List of lists of connected nodes. Each of the lists is disjoint.

        """


class WeightedGraph(Graph):
    """Turns the unweighted Graph it's derived from into a weighted Graph.

    Args:
        nodes: Stores the Nodes of the Graph, defaulting to a set()
        edges: Stores the Edges of the Graph, defaulting to a set()

    Attributes:
        info: Is of any type and can be used for storing additional information.
    """

    @abstractmethod
    @overload
    def add_edge(self, src, dest, weight):
        """Adds a weighted Edge with the Node 'src' and Node 'dest'."""
        pass
    
    def minimum_spanning_tree(self):
        """Finds set of edges representing a MST for the Graph
        Returns:
            set of Weighted Edges
        """

    mst = minimum_spanning_tree


class DirectedGraph(Graph):
    """Turns the undirected Graph it's derived from into a directed Graph.

    Args:
        nodes: Stores the Nodes of the Graph, defaulting to a set()
        edges: Stores the Edges of the Graph, defaulting to a set()

    Attributes:
        info: Is of any type and can be used for storing additional information.
    """

    @abstractmethod
    @overload
    def add_edge(self, src, dest):
        """Adds an Edge between the Node 'src' and the Node 'dest'."""
        pass

    def get_edge(self, src, dest):
        """Returns the directed Edge between two Nodes.

        Args:
            src: Source Node.
            dest: Target Node.

        Returns:
            DirectedEdge in the Graph from 'src' to 'dest', or None if such an Edge doesn't exist.
        """
        pass

    @abstractmethod
    def topological_sort(self):
        "Sorts the directed Graph in a topological order."
        pass


class WeightedDirectedGraph(DirectedGraph, WeightedGraph):
    """Combines a directed and a weighted graph into a directed, weighted Graph.

    Args:
        nodes: Stores the Nodes of the Graph, defaulting to a set()
        edges: Stores the Edges of the Graph, defaulting to a set()

    Attributes:
        info: Is of any type and can be used for storing additional information.
    """

    @abstractmethod
    @overload
    def add_edge(self, src, dest, weight):
        """Adds an Edge between the Node 'src' and the Node 'dest'."""
        pass


class BipartiteGraph(Graph):
    """Creates bipartite Graph that is unweighted and undirected."""
    def add_r_node(self, label):
        """Adds a node to the Right partition.
        Args:
            label: a label, or a node Object
        Returns:
            new node object
        """
    
    def add_l_node(self, label):
        """Adds a node to the Left partition.
        Args:
            label: a label, or a node Object
        Returns:
            new node object
        """
    
    def add_l_nodes(self, labels):
        """Adds a nodes to the Right partition.
        Args:
            labels: an iterable object of Labels or Nodes
        Returns:
            a list of Nodes
        """
    
    def add_r_nodes(self, labels):
        """Adds nodes to the Left partition.
        Args:
            labels: an iterable object of Labels or Nodes
        Returns:
            a list of Nodes
        """


class WeightedBipartiteGraph(WeightedGraph, BipartiteGraph):
    """Creates bipartite Graph that is weighted and undirected."""

    pass


class DirectedBipartiteGraph(DirectedGraph, BipartiteGraph):
    """Creates bipartite Graph that is unweighted and directed."""

    pass


class WeightedDirectedBipartiteGraph(WeightedDirectedGraph, BipartiteGraph):
    """Creates bipartite Graph that is weighted and directed."""

    pass


def create_graph(directed=False, weighted=False, bipartite=False) -> Graph:
    """Returns the right Graph from given settings.

    Args:
        directed: Boolean.
        weighted: Boolean.
        bipartite: Boolean.

    Defaults to an undirected, unweighted and non-bipartite Graph.
    """

    pass
