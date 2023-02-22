from datenstruktur.edge import Edge
from datenstruktur.graph import BipartiteGraph, Graph, WeightedGraph
from datenstruktur.node import Node

from algorithmus.options import Color, Pattern


class Algorithm:

    # define conditions for user input by changing these values
    need_start = False  # default: no start node is needed
    need_end = False  # default: no end node is needed
    need_graph = Graph  # default: every type of graph can be used

    # other conditions, which are not met, can be handled by using show_error() and returning False

    def __init__(self, controller=None, drawboard=None) -> None:
        """Initializes new algorithm object."""
        self.ds_graph = None
        self.controller = controller
        self.drawboard = drawboard

        if controller is None or drawboard is None:
            self.is_test = True
        else:
            self.is_test = False

    # only overwrite run() and get_info()
    def run(self, graph: Graph, start_node: Node, end_node: Node) -> bool:
        """Run your algorithm in here.

        Make sure to call self.init_graph(graph) at the beginning of run.

        Return True at the end of your algorithm.
        Return False, if something went wrong and
        consider using show_error() to give feedback to the user.

        Args:
            graph (Graph): datastructure graph to run the algorithm on
            start_node (Node): start node; can be None if not selected by user
            end_node (Node): end node; can be None if not selected by user

        Returns:
            bool: The return value. True for success, False otherwise.

        """

    def get_info(self) -> str:
        """Returned String will be shown on the details panel in the GUI.
        Maybe describe briefly what the algorithm is doing and/or what each color means in your case.
        """
        return ""

    def init_graph(self, graph: Graph):
        """Defines the graph on which will be worked on.

        Args:
            graph (Graph): datastructure graph to run the algorithm on
        """

        self.ds_graph = graph

    def display(self):
        """Creates a breakpoint for visible changes to the graph.
        Example:
        color_node(1)
        color_node(2)
        display()
        color_node(3)
        display()
        will color the nodes 1 and 2 in a single step, while node 3's color will be changed in the next step.

        """
        if not self.is_test:
            self.controller.display()

    def color_node(self, node: Node, color: Color):
        """Colors a given node.

        Args:
            node (Node): specifies the node to color
            color (Color): the new color of the node (choose from options.Color)
        """
        if not self.is_test:
            self.controller.change_node(node, "fill", color)

    def color_edge(self, edge: Edge, color: Color):
        """Colors a given edge.

        Args:
            edge (Edge): specifies the edge to color
            color (Color): the new color of the edge (choose from options.Color)

        """
        if not self.is_test:
            self.controller.change_edge(edge, "fill", color)

    def change_node_pattern(self, node: Node, pattern_type: Pattern):
        """Makes the outline of a given node appear in the pattern stated by pattern_type.

        Args:
            node (Node): specifies the node to change the pattern of
            pattern_type (Pattern): pattern type from options.Pattern (solid, dashed, dotted)

        """
        if not self.is_test:
            self.controller.change_node(node, "dash", pattern_type)

    def change_edge_pattern(self, edge: Edge, pattern_type: Pattern):
        """Makes the outline of a given edge appear in the pattern stated by pattern_type.

        Args:
            edge (Edge): specifies the edge to change the pattern of
            pattern_type (Pattern): pattern type from options.Pattern (solid, dashed, dotted)

        """
        if not self.is_test:
            self.controller.change_edge(edge, "dash", pattern_type)

    def change_node_size(self, node: Node, size: int):
        """Changes the outline width of a given node.

        Args:
            node (Node): specifies the node to change the size of
            size (int): new width in pixel; default is 3

        """
        if not self.is_test:
            self.controller.change_node(node, "width", size)

    def change_edge_size(self, edge: Edge, size: int):
        """Changes the width of a given edge.

        Args:
            edge (Edge): specifies the edge to change the size of
            size (int): new width in pixel; default is 3

        """
        if not self.is_test:
            self.controller.change_edge(edge, "width", size)

    def change_edge_weight(self, edge: Edge, weight: float, repre: str):
        """Changes the weight of a given edge on the canvas.
        Repr is independent of the data structure which allows for a different representation of the weight.
        This way capacities can be visualized differently (e.g. "1/3").

        Args:
            edge (Edge): specifies the edge to change the weight of
            weight (float): new weight for datastructure
            repr: (str): str shown on the canvas

        """
        edge.weight = weight
        if not self.is_test:
            self.controller.change_weight_value(edge, repre)

    def color_edge_weight(self, edge: Edge, color: Color):
        """Changes the weight color of a given edge on the canvas.

        Args:
            edge (Edge): specifies the edge to change the weight color of
            color (Color): the new color of the weight (choose from options.Color)

        """
        if not self.is_test:
            self.controller.change_weight(edge, "fill", color)

    def dist_to_weight(self):
        """Sets the weight of each edge to its length. This function
        updates the weights both in the datastructure and on the canvas."""

        if not self.is_test:
            if isinstance(self.ds_graph, WeightedGraph):
                for edge in self.ds_graph.edges:
                    edge.weight = self.drawboard.get_edge_length(
                        self.drawboard.get_g_edge_from_ds(edge)
                    )
                self.controller.dist_to_weight()

    def update_label(self, node: Node, new_label: str, overwrite: bool = False):
        """Updates the label of a given node with new_label for both the node on the canvas and in the datastructure.

        Args:
            node (Node): specifies the node to update the label of
            new_label (str): new label
            overwrite (bool): when set to True label and possibly "Start" or "End" will be discarded and only new_label will be shown

        """

        node.label = new_label
        if not self.is_test:
            self.controller.change_label(node, "text", new_label, overwrite)

    def get_node_coords(self, node: Node):
        """Retrieves the center coordinates of a node given by node.

        Returns:
            (int,int):first x and then y coordinate in the canvas
        """
        if not self.is_test:
            g_node = self.drawboard.get_g_node_from_ds(node)
            return self.drawboard.get_center(g_node)

    def create_node(self, label: str, coords=None, is_L=True) -> Node:
        """Creates a new node on the canvas.

        This function will try to put the new node at the given coordinates or
        or near them if obstructed. When coords is None the new node will be placed
        near a random existing node on the canvas or at the top left for an empty canvas.

        This function creates the datastructure node and should replace the standard add_node
        function of the Graph datastructure.
        By default nodes will be placed in set L for bipartite graphs.

        Args:
            label (Node): label for the new node
            coords (int,int): position to place the node at
            is_L (bool): set this to False, if the node should be in set R

        """
        if isinstance(self.ds_graph, BipartiteGraph):
            if is_L:
                new_node = self.ds_graph.add_l_node(label)
            else:
                new_node = self.ds_graph.add_r_node(label)
        else:
            new_node = self.ds_graph.add_node(label)
        if not self.is_test and new_node is not None:
            self.controller.create_node(new_node, coords, is_L)

        return new_node

    def delete_node(self, node: Node):
        """Deletes the specified node on the canvas and removes it from the datastructure.

        This function should replace the standard remove_node functions of the Graph datastructure.

        Args:
            node (Node): specifies the node to delete
        """
        if not self.is_test:
            self.controller.hide_node(node)
        self.ds_graph.remove_node(node)

    def create_edge(self, start_node: Node, end_node: Node, weight=1) -> Edge:
        """Creates a new edge on the canvas and for the datastructure.

        This function should replace the standard add_edge functions of the Graph datastructure.

        """
        if isinstance(self.ds_graph, WeightedGraph):
            new_edge = self.ds_graph.add_edge(start_node, end_node, weight)
        else:
            new_edge = self.ds_graph.add_edge(start_node, end_node)
        if not self.is_test and new_edge is not None:
            self.controller.create_edge(new_edge)
        return new_edge

    def delete_edge(self, edge: Edge):
        """Deletes the specified edge on the canvas and removes it from the datastructure.

        This function should replace the standard remove_edge functions of the Graph datastructure.

        Args:
            edge (Edge): specifies the edge to delete
        """
        if not self.is_test:
            self.controller.hide_edge(edge)
        self.ds_graph.remove_edge(edge)

    def show_info(self, info_message: str):
        """Creates an information pop up window for the user with the given text.
        The intended usage is to call it possibly at the end of the algorithm to
        notify the user and give some feedback.

        Args:
            info_message (str): message shown in the pop up fenster
        """
        if not self.is_test:
            self.controller.show_info(info_message)

    def show_error(self, error_message: str):
        """Immediately creates an error pop up window for the user with the given text.
        Could be used after failed check for compability of the graph.
        Notify the user about what went wrong and maybe why before returning False.

        Args:
            error_message (str): message shown in the pop up fenster
        """
        if not self.is_test:
            self.controller.show_error(error_message)

    def add_log(self, text: str):
        """Adds a new entry to the log panel.
        The final log entry has the form:
        log count: text \n

        Args:
            text (str): log message which will be shown in the text panel
        """
        if not self.is_test:
            self.controller.add_log(text)
