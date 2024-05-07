from WolfGoatCabbage.graphs.wgc_vertex import WolfGoatCabbageVertex


class WolfGoatCabbageGraph:

    """
    A class representing a Wolf, Goat, Cabbage graph from the famous puzzle.
    Used to solve the puzzle using a graph.
    """

    @staticmethod
    def get_neighbors(vertex: WolfGoatCabbageVertex):
        """
        Returns the neighboring vertices of vertex.

        :param vertex: WolfGoatCabbageVertex, the vertex to get the neighbors of

        :return: a generator of WolfGoatCabbageVertex, the neighbors of vertex
        """

        return vertex.get_neighbors()

    @staticmethod
    def is_edge(vertex1: WolfGoatCabbageVertex, vertex2: WolfGoatCabbageVertex):
        """
        Returns True if vertex1 is a neighbor of vertex2, False otherwise.

        :param vertex1: WolfGoatCabbageVertex, the first vertex
        :param vertex2: WolfGoatCabbageVertex, the second vertex

        :return: True if vertex1 is a neighbor of vertex2, False otherwise
        """

        return vertex1 in vertex2.get_neighbors()

    @staticmethod
    def get_start():
        """
        Returns the start vertex of the graph.
        Which is the vertex that represents the start state of the puzzle.
        Position of the wolf, goat, cabbage and boat on the left side of the river (0000).

        :return: WolfGoatCabbageVertex, the start vertex of the graph
        """

        return WolfGoatCabbageVertex(0b0000)

    @staticmethod
    def get_end():
        """
        Returns the end vertex of the graph.
        Which is the vertex that represents the end state of the puzzle.
        Position of the wolf, goat, cabbage and boat on the right side of the river (1111).

        :return: WolfGoatCabbageVertex, the end vertex of the graph
        """

        return WolfGoatCabbageVertex(0b1111)
