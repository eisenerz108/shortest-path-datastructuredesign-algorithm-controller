import datenstruktur.edge as edge
import datenstruktur.graphEX as gX
import datenstruktur.interfaces as interfaces
import datenstruktur.node as node


class Graph(interfaces.Graph):
    """See interfaces.Graph class."""

    def __init__(self, nodes=None, edges=None):
        self.nodes = set()
        if nodes is None:
            nodes = set()
        for node in nodes:
            self.add_node(node)

        self.edges = set()
        if edges is None:
            edges = set()
        for edge in edges:
            self.add_edge(*edge)

    def __len__(self):
        return len(self.nodes)

    def __str__(self) -> str:
        res = "Nodes: "
        for node in self.nodes:
            res += str(node) + " "

        res += "\nEdges: "

        for edge in self.edges:
            res += str(edge) + " "

        res += "\n"

        return res

    @property
    def info(self):
        """See interfaces.Graph class."""
        return self._info

    @info.setter
    def info(self, val):
        """See interfaces.Graph class."""
        self._info = val

    def add_node(self, label):
        if isinstance(label, node.Node):
            if label in self.nodes:
                print("Node already in Graph.")
                return label
            if label.degree:
                print("Node cannot be added as it has incident Edges not in Graph.")
            self.nodes.add(label)
            return label
        new_node = node.Node(label)
        self.nodes.add(new_node)

        return new_node

    def add_nodes(self, labels):
        """See interfaces.Graph class."""
        return [self.add_node(label) for label in labels]

    def remove_node(self, node):
        """See interfaces.Graph class."""
        self.nodes.remove(node)

        for to_remove in node._edges.copy():
            self.remove_edge(to_remove.src_node, to_remove.dest_node)

        del node

    def get_node_by_label(self, label):
        """See interfaces.Graph class."""
        for node in self.nodes:
            if node.label == label:
                return node

        return None

    def get_nodes_by_label(self, label):
        """See interfaces.Graph class."""
        return [node for node in self.nodes if node.label == label]

    def get_node_neighbours(self, node):
        """See interfaces.Graph class."""
        return node.neighbours

    def add_edge(self, src, dest=None):
        """See interfaces.Graph class."""

        if not dest:
            assert isinstance(src, edge.Edge), "Argument is not an Edge object!"
            a, b = src.get_endpoints()

            if a not in self.nodes or b not in self.nodes:
                raise gX.AddEdgeException(
                    "One of the nodes not in Graph, the edge cannot be added."
                )
            result_edge = self.add_edge(a, b)

            if src.info:
                result_edge.info = src.info

            return result_edge

        if src not in self.nodes:
            print("Node {} does not exist in Graph.".format(src.label))
            return None

        elif dest not in self.nodes:
            print("Node {} does not exist in Graph.".format(dest.label))
            return None

        if src.has_edge(dest):
            print("Edge already exists.")
            return None

        to_add = edge.Edge(src, dest)

        src._edges.add(to_add)
        dest._edges.add(to_add)

        src.neighbours.append(dest)
        if src is not dest:  # not self-loop
            dest.neighbours.append(src)

        # change node degrees
        src._degree += 1
        src._in_degree += 1
        src._out_degree += 1
        dest._degree += 1
        dest._in_degree += 1
        dest._out_degree += 1

        self.edges.add(to_add)

        return to_add

    def add_edges(self, edges):
        """See interfaces.Graph class."""
        res = []
        for edg in edges:
            if isinstance(edg, edge.Edge):
                res.append(self.add_edge(edg))
            else:
                res.append(self.add_edge(*edg))
        return res

    def get_edge(self, src, dest):
        """See interfaces.Graph class."""
        assert isinstance(src, node.Node) and isinstance(
            dest, node.Node
        ), "get_edge(): Arguments must be of type Node."

        for edge in src._edges:
            if (dest == edge.dest_node and src == edge.src_node) or (
                dest == edge.src_node and src == edge.dest_node
            ):
                return edge

        return None

    def remove_edge(self, src, dest=None):
        """See interfaces.Graph class."""
        if not dest:
            assert isinstance(src, edge.Edge), "Argument is not an Edge object!"
            self.remove_edge(src.src_node, src.dest_node)
            return

        assert isinstance(
            dest, node.Node
        ), "Two Arguments, but {} is not a Node Object".format(dest)
        for edg in src._edges:
            if (dest == edg.dest_node and src == edg.src_node) or (
                dest == edg.src_node and src == edg.dest_node
            ):
                src._edges.remove(edg)
                dest._edges.remove(edg)

                src.neighbours.remove(dest)
                dest.neighbours.remove(src)

                src._degree -= 1
                src._in_degree -= 1
                src._out_degree -= 1

                dest._degree -= 1
                dest._in_degree -= 1
                dest._out_degree -= 1

                self.edges.remove(edg)
                del edg

                break

    def detect_cycle(self):
        """See interfaces.Graph class."""
        for node in self.nodes:
            node.visited = False
        for edge in self.edges:
            edge.visited = False

        for node in self.nodes:
            if node.visited == False:
                print("Starting with " + node.label)
                if self._detect_cycle_helper(node) == True:
                    return True
        return False

    def _detect_cycle_helper(self, node):
        if node.visited == True:
            return True

        node.visited = True
        # if a node has no circle every Node will only be visited once

        for edge in node._edges:
            if edge.visited == False:
                edge.visited = True
                if edge.src_node == node:
                    if self._detect_cycle_helper(edge.dest_node) == True:
                        return True
                else:
                    if self._detect_cycle_helper(edge.src_node) == True:
                        return True
        return False

    def breadth_first_search(self, start):
        """See interfaces.Graph class."""

        queue = []
        for node in self.nodes:
            node.visited = False

        queue.append(start)
        start.visited = True

        while queue:
            curr = queue.pop(0)
            yield curr

            for neighbour in curr.neighbours:
                if neighbour.visited == False:
                    queue.append(neighbour)
                    neighbour.visited = True

    bfs = breadth_first_search

    def depth_first_search(self, start):
        """See interfaces.Graph class."""

        queue = []
        for node in self.nodes:
            node.visited = False

        queue.append(start)

        while queue:
            curr = queue.pop()

            if not curr.visited:
                yield curr
                curr.visited = True

                for neighbour in curr.neighbours:
                    if not neighbour.visited:
                        queue.append(neighbour)

    dfs = depth_first_search

    def get_connected_components(self):
        res = []
        remaining_nodes = self.nodes.copy()

        while len(remaining_nodes):
            current = remaining_nodes.pop()
            component = set(self.bfs(current))
            remaining_nodes -= component
            res.append(component)

        return res

    gcc = get_connected_components


class WeightedGraph(Graph, interfaces.WeightedGraph):
    """See interfaces.WeightedGraph class."""

    def add_edge(self, src, dest=None, weight=1):
        """See interfaces.WeightedGraph class."""

        if not dest:
            assert isinstance(src, edge.Edge), "Argument is not an Edge object!"
            a, b = src.get_endpoints()
            w = src.weight
            if a not in self.nodes or b not in self.nodes:
                raise gX.AddEdgeException(
                    "One of the nodes not in Graph, the edge cannot be added."
                )
            res = self.add_edge(a, b, w)
            if src.info:
                res.info = src.info
            return res

        if src not in self.nodes:
            print("Node {} does not exist in Graph.".format(src.label))
            return None

        elif dest not in self.nodes:
            print("Node {} does not exist in Graph.".format(dest.label))
            return None

        if src.has_edge(dest):
            print("Edge already exists.")
            return None

        to_add = edge.WeightedEdge(src, dest, weight)

        src._edges.add(to_add)
        src.neighbours.append(dest)
        dest._edges.add(to_add)
        dest.neighbours.append(src)

        # change node degrees
        src._degree += 1
        src._in_degree += 1
        src._out_degree += 1
        dest._degree += 1
        dest._in_degree += 1
        dest._out_degree += 1

        self.edges.add(to_add)

        return to_add
    
    def minimum_spanning_tree(self):
        def edge_weight(ex):
            return ex.weight

        edge_list = list(self.edges)
        edge_list.sort(key=edge_weight)
        res = set()
        g = WeightedGraph()
        for to_add in self.nodes:
            g.add_node(to_add.label)
        while edge_list:
            to_check = edge_list.pop()
            a, b = to_check.get_endpoints()
            a = g.get_node_by_label(a.label)
            b = g.get_node_by_label(b.label)
            g.add_edge(a,b)
            if g.detect_cycle():
                print(to_check)
                g.remove_edge(a,b)
                continue
            res.add(to_check)
            if len(res) == len(g.nodes) -1:
                break
        if not len(res) == len(g.nodes) -1:
            return None
        return res

    mst = minimum_spanning_tree


class DirectedGraph(Graph, interfaces.DirectedGraph):
    """See interfaces.DirectedGraph class."""

    def remove_node(self, node):
        """See interfaces.Graph class."""
        self.nodes.remove(node)

        for to_remove in node._edges.copy():
            self.remove_edge(to_remove.src_node, to_remove.dest_node)

        for selected_edge in self.edges.copy():
            if selected_edge.dest_node == node:
                self.remove_edge(selected_edge.src_node, selected_edge.dest_node)

        del node

    def get_node_neighbours(self, node, which="all"):
        """See interfaces.DirectedGraph class."""

        if which == "in":
            neighbours = set()

            for current_node in self.nodes:
                for edge in current_node._edges:
                    if edge.dest_node == node:
                        neighbours.add(current_node)

            return neighbours

        if which == "out":
            return set([edge.dest_node for edge in node._edges])

        if which == "all":
            neighbours = set()

            for edge in node._edges:
                neighbours.add(edge.dest_node)

            for current_node in self.nodes:
                for edge in current_node._edges:
                    if edge.dest_node == node:
                        neighbours.add(current_node)

            return neighbours

    def add_edge(self, src, dest=None):
        """See interfaces.DirectedGraph class."""

        if not dest:
            assert isinstance(src, edge.Edge), "Argument is not an Edge object!"
            a, b = src.get_endpoints()
            if a not in self.nodes or b not in self.nodes:
                raise gX.AddEdgeException(
                    "One of the nodes not in Graph, the edge cannot be added."
                )
            res = self.add_edge(a, b)
            if src.info:
                res.info = src.info
            return res

        if src not in self.nodes:
            print("Node {} does not exist in Graph.".format(src.label))
            return None

        elif dest not in self.nodes:
            print("Node {} does not exist in Graph.".format(dest.label))
            return None

        if src.has_edge(dest):
            print("Edge already exists.")
            return None

        to_add = edge.DirectedEdge(src, dest)
        src._edges.add(to_add)
        src.neighbours.append(dest)

        # change node degrees
        src._out_degree += 1
        src._degree += 1
        dest._in_degree += 1
        dest._degree += 1

        self.edges.add(to_add)

        return to_add

    def get_edge(self, src, dest):
        """See interfaces.Graph class."""
        assert isinstance(src, node.Node) and isinstance(
            dest, node.Node
        ), "get_edge(): Arguments must be of type Node."

        for edge in src._edges:
            if dest == edge.dest_node:
                return edge

        return None

    def remove_edge(self, src, dest=None):
        """See interfaces.DirectedGraph class."""
        if not dest:
            assert isinstance(
                src, edge.Edge
            ), "One Argument, but it is not an Edge object!"
            self.remove_edge(src.src_node, src.dest_node)
            return

        assert isinstance(
            dest, node.Node
        ), "Two Arguments, but {} is not a Node Object".format(dest)
        for edg in src._edges:
            if dest == edg.dest_node:
                src._edges.remove(edg)
                src.neighbours.remove(dest)

                # change node degrees
                src._out_degree -= 1
                src._degree -= 1
                dest._in_degree -= 1
                dest._degree -= 1

                self.edges.remove(edg)
                del edg

                break

    def detect_cycle(self):
        """See interfaces.DirectedGraph class."""
        pass

    def topological_sort(self):
        """See interfaces.DirectedGraph class."""
        free_nodes = []
        remaining = []
        res = []
        incoming = dict()

        for node in self.nodes:
            if node.in_degree == 0:
                free_nodes.append(node)
                incoming[node] = 0
            else:
                remaining.append(node)
                incoming[node] = node.in_degree

        while free_nodes:
            to_remove = free_nodes.pop()
            res.append(to_remove)

            for nb in to_remove.neighbours:
                incoming[nb] -= 1

                if nb in remaining and incoming[nb] == 0:
                    remaining.remove(nb)
                    free_nodes.append(nb)
        if remaining:
            print("There is a cycle in the graph, no topological ordering possible")
            return None
        return res

    toposort = topological_sort


class WeightedDirectedGraph(
    DirectedGraph, WeightedGraph, interfaces.WeightedDirectedGraph,
):
    """See interfaces.WeightedDirectedGraph class."""

    def add_edge(self, src, dest=None, weight=1):

        if not dest:
            assert isinstance(src, edge.Edge), "Argument is not an Edge object!"
            a, b = src.get_endpoints()
            w = src.weight
            if a not in self.nodes or b not in self.nodes:
                raise gX.AddEdgeException(
                    "One of the nodes not in Graph, the edge cannot be added."
                )
            res = self.add_edge(a, b, w)
            if src.info:
                res.info = src.info
            return res

        if src not in self.nodes:
            print("Node {} does not exist in Graph.".format(src.label))
            return None

        elif dest not in self.nodes:
            print("Node {} does not exist in Graph.".format(dest.label))
            return None

        if src.has_edge(dest):
            print("Edge already exists.")
            return None

        to_add = edge.DirectedWeightedEdge(src, dest, weight)
        src._edges.add(to_add)
        src.neighbours.append(dest)

        # change node degrees
        src._out_degree += 1
        src._degree += 1
        dest._in_degree += 1
        dest._degree += 1

        self.edges.add(to_add)

        return to_add


class BipartiteGraph(Graph, interfaces.BipartiteGraph):
    """See interfaces.BipartiteGraph class."""

    def __init__(self, r_nodes=None, l_nodes=None, edges=None):
        self.r_nodes = set()
        self.l_nodes = set()
        self.nodes = set()
        self.edges = set()

        if r_nodes is None:
            r_nodes = set()
        if l_nodes is None:
            l_nodes = set()
        if edges is None:
            edges = set()

        for node in r_nodes:
            self.add_r_node(node)

        for node in l_nodes:
            self.add_l_node(node)

        self.add_edges(edges)

    def add_r_node(self, label):
        tmp = Graph.add_node(self, label)
        self.r_nodes.add(tmp)
        return tmp

    def add_l_node(self, label):
        tmp = Graph.add_node(self, label)
        self.l_nodes.add(tmp)
        return tmp

    def add_l_nodes(self, labels):
        return [self.add_l_node(label) for label in labels]

    def add_r_nodes(self, labels):
        return [self.add_r_node(label) for label in labels]

    def add_node(self, label):
        """See interfaces.BipartiteGraph class."""
        raise gX.AddNodeException(
            "Cannot add a node to Bipartite Graph without specifying side"
        )

    def add_nodes(self, labels):
        """See interfaces.BipartiteGraph class."""
        raise gX.AddNodeException(
            "Cannot add a node to Bipartite Graph without specifying side"
        )

    def add_edge(self, src, dest=None):
        """See interfaces.BipartiteGraph class."""
        if not dest:
            if (src.src_node in self.r_nodes and src.dest_node in self.r_nodes) or (
                src.src_node in self.l_nodes and dest.dest_node in self.l_nodes
            ):
                raise gX.AddEdgeException(
                    "Edge does not preserve the bipartite property of the Bipartite Graph"
                )
            return Graph.add_edge(self, src)

        if (src in self.r_nodes and dest in self.r_nodes) or (
            src in self.l_nodes and dest in self.l_nodes
        ):
            raise gX.AddEdgeException(
                "Edge does not preserve the bipartite property of the Bipartite Graph"
            )
        return Graph.add_edge(self, src, dest)

    def is_bipartite(self):
        """See interfaces.BipartiteGraph class."""
        return True


class WeightedBipartiteGraph(
    WeightedGraph, BipartiteGraph, interfaces.WeightedBipartiteGraph
):
    """See interfaces.WeightedBipartiteGraph class."""

    def __init__(self, r_nodes=None, l_nodes=None, edges=None):
        BipartiteGraph.__init__(self, r_nodes, l_nodes, edges)

    def add_node(self, label):
        """See interfaces.DirectedBipartiteGraph class."""
        return BipartiteGraph.add_node(label)

    def add_nodes(self, labels):
        """See interfaces.DirectedBipartiteGraph class."""
        return BipartiteGraph.add_nodes(labels)

    def add_r_node(self, label):
        tmp = WeightedGraph.add_node(self, label)
        self.r_nodes.add(tmp)
        return tmp

    def add_l_node(self, label):
        tmp = WeightedGraph.add_node(self, label)
        self.l_nodes.add(tmp)
        return tmp

    def add_edge(self, src, dest=None, weight=1):
        """See interfaces.BipartiteGraph class."""

        if not dest:
            if (src.src_node in self.r_nodes and src.dest_node in self.r_nodes) or (
                src.src_node in self.l_nodes and dest.dest_node in self.l_nodes
            ):
                raise gX.AddEdgeException(
                    "Edge does not preserve the bipartite property of the Bipartite Graph"
                )
            return WeightedGraph.add_edge(self, src)

        if (src in self.r_nodes and dest in self.r_nodes) or (
            src in self.l_nodes and dest in self.l_nodes
        ):
            raise gX.AddEdgeException(
                "Edge does not preserve the bipartite property of the Bipartite Graph"
            )
        return WeightedGraph.add_edge(self, src, dest, weight)


class DirectedBipartiteGraph(
    DirectedGraph, BipartiteGraph, interfaces.DirectedBipartiteGraph
):
    """See interfaces.DirectedBipartiteGraph class."""

    def __init__(self, r_nodes=None, l_nodes=None, edges=None):
        BipartiteGraph.__init__(self, r_nodes, l_nodes, edges)

    def add_node(self, label):
        """See interfaces.DirectedBipartiteGraph class."""
        return BipartiteGraph.add_node(label)

    def add_nodes(self, labels):
        """See interfaces.DirectedBipartiteGraph class."""
        return BipartiteGraph.add_nodes(labels)

    def add_r_node(self, label):
        tmp = DirectedGraph.add_node(self, label)
        self.r_nodes.add(tmp)
        return tmp

    def add_l_node(self, label):
        tmp = DirectedGraph.add_node(self, label)
        self.l_nodes.add(tmp)
        return tmp

    def add_edge(self, src, dest=None):
        """See interfaces.BipartiteGraph class."""

        if not dest:
            if (src.src_node in self.r_nodes and src.dest_node in self.r_nodes) or (
                src.src_node in self.l_nodes and dest.dest_node in self.l_nodes
            ):
                raise gX.AddEdgeException(
                    "Edge does not preserve the bipartite property of the Bipartite Graph"
                )
            return DirectedGraph.add_edge(self, src)

        if (src in self.r_nodes and dest in self.r_nodes) or (
            src in self.l_nodes and dest in self.l_nodes
        ):
            raise gX.AddEdgeException(
                "Edge does not preserve the bipartite property of the Bipartite Graph"
            )
        return DirectedGraph.add_edge(self, src, dest)


class WeightedDirectedBipartiteGraph(
    WeightedDirectedGraph, BipartiteGraph, interfaces.WeightedDirectedBipartiteGraph,
):
    """See interfaces.WeightedDirectedBipartiteGraph class."""

    def __init__(self, r_nodes=None, l_nodes=None, edges=None):
        BipartiteGraph.__init__(self, r_nodes, l_nodes, edges)

    def add_node(self, label):
        """See interfaces.DirectedBipartiteGraph class."""
        return BipartiteGraph.add_node(label)

    def add_nodes(self, labels):
        """See interfaces.DirectedBipartiteGraph class."""
        return BipartiteGraph.add_nodes(labels)

    def add_r_node(self, label):
        tmp = WeightedDirectedGraph.add_node(self, label)
        self.r_nodes.add(tmp)
        return tmp

    def add_l_node(self, label):
        tmp = WeightedDirectedGraph.add_node(self, label)
        self.l_nodes.add(tmp)
        return tmp

    def add_edge(self, src, dest=None, weight=1):
        """See interfaces.BipartiteGraph class."""

        if not dest:
            if (src.src_node in self.r_nodes and src.dest_node in self.r_nodes) or (
                src.src_node in self.l_nodes and dest.dest_node in self.l_nodes
            ):
                raise gX.AddEdgeException(
                    "Edge does not preserve the bipartite property of the Bipartite Graph"
                )
            return WeightedDirectedGraph.add_edge(self, src)

        if (src in self.r_nodes and dest in self.r_nodes) or (
            src in self.l_nodes and dest in self.l_nodes
        ):
            raise gX.AddEdgeException(
                "Edge does not preserve the bipartite property of the Bipartite Graph"
            )
        return WeightedDirectedGraph.add_edge(self, src, dest, weight)


def create_graph(weighted=False, directed=False, bipartite=False) -> Graph:
    """See interfaces.create_graph function."""

    assert (
        isinstance(weighted, bool)
        and isinstance(directed, bool)
        and isinstance(bipartite, bool)
    ), f"Please make sure to use booleans as arguments. Used: {weighted, directed, bipartite}"

    graphs = [
        Graph,  # 0 unweighted, undirected, non-bipartite
        WeightedGraph,  # 1 weighted, undirected, non-bipart.
        DirectedGraph,  # 2 unweighted, directed, non-bipart.
        WeightedDirectedGraph,  # 3 weighted, directed, non-bipart.
        BipartiteGraph,  # 4 unweighted, undirected, bipart.
        WeightedBipartiteGraph,  # 5 weighted, undirected, bipart.
        DirectedBipartiteGraph,  # 6 unweighted, directed, bipart.
        WeightedDirectedBipartiteGraph,  # 7 weighted, directed, bipart.
    ]

    selected = 1 * weighted + 2 * directed + 4 * bipartite

    return graphs[selected]()
