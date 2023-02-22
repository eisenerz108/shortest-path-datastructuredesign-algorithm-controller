import datenstruktur.interfaces as interfaces


class Edge(interfaces.Edge):
    """See interfaces.Edge class."""

    def __init__(self, src_node, dest_node) -> None:
        self.dest_node = dest_node
        self.src_node = src_node
        self._info = None

    def __hash__(self) -> int:
        return hash((self.src_node, self.dest_node))

    def __eq__(self, other_edge) -> bool:
        return (
            self.__class__ == other_edge.__class__
            and self.get_endpoints() == other_edge.get_endpoints()
        )

    def __str__(self) -> str:
        return ""  # Returns empty placeholder string.

    def __repr__(self) -> str:
        return "Edge({}, {})".format(self.dest_node, self.src_node)

    @property
    def info(self):
        """See interfaces.Edge class."""
        return self._info

    @info.setter
    def info(self, val):
        """See interfaces.Edge class."""
        self._info = val

    def get_endpoints(self):
        """See interfaces.Edge class."""
        return frozenset([self.src_node, self.dest_node])

    @property
    def visited(self):
        """See interfaces.Node class."""
        return self._visited

    @visited.setter
    def visited(self, val):
        """See interfaces.Node class."""
        self._visited = val


class DirectedEdge(Edge, interfaces.DirectedEdge):
    """See interfaces.DirectedEdge class."""

    def __hash__(self) -> int:
        return hash((self.src_node, self.dest_node))

    def __eq__(self, other_edge) -> bool:
        return super().__eq__(other_edge)

    def get_head_node(self):
        """See interfaces.Edge class."""
        return self.dest_node

    def get_tail_node(self):
        """See interfaces.Edge class."""
        return self.src_node

    def get_endpoints(self):
        return (self.src_node, self.dest_node)


class WeightedEdge(Edge, interfaces.WeightedEdge):
    """See interfaces.WeightedEdge class."""

    def __init__(self, src_node, dest_node, weight=1) -> None:
        """See interfaces.WeightedEdge class."""
        self.dest_node = dest_node
        self.src_node = src_node
        self._weight = weight
        self._info = None

    def __hash__(self) -> int:
        return hash((self.src_node, self.dest_node))

    def __str__(self) -> str:
        return ""  # Returns empty placeholder string.

    @property
    def weight(self):
        """See interfaces.WeightedEdge class."""
        return self._weight

    @weight.setter
    def weight(self, val: float):
        """See interfaces.WeightedEdge class."""
        self._weight = val


class DirectedWeightedEdge(DirectedEdge, WeightedEdge):
    """See interfaces.DirectedWeightedEdge class."""

    def __init__(self, src_node, dest_node, weight=1) -> None:
        """See interfaces.WeightedEdge class."""
        self.dest_node = dest_node
        self.src_node = src_node
        self._weight = weight
        self._info = None
