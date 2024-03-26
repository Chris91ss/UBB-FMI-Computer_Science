from graph_exceptions import GraphException
import copy
from random import randint


class DirectedGraph:

    def __init__(self, number_of_vertices=0):
        """
        Constructor for the DirectedGraph class
        :param number_of_vertices: the number of vertices in the graph
        """
        self.number_of_vertices = number_of_vertices
        self.number_of_edges = 0
        self.inbound_edges = {}
        self.outbound_edges = {}
        self.costs = {}

    def __str__(self):
        """
        Returns a string representation of the graph
        """
        string = f"DirectedGraph: {self.number_of_vertices} vertices, {self.number_of_edges} edges"
        for vertex, inbound_edges in self.inbound_edges.items():
            for inbound_edge in inbound_edges:
                if not inbound_edges and not self.outbound_edges[vertex]:
                    string += f"\n {vertex} -> isolated vertex"
                    continue

                string += f"\n {inbound_edge} -> {vertex} ->: {self.costs[(inbound_edge, vertex)]}"

        return string

    def get_number_of_vertices(self):
        """
        Getter for the number of vertices
        :return: the number of vertices
        """
        return self.number_of_vertices

    def set_number_of_vertices(self, number_of_vertices):
        """
        Setter for the number of vertices
        :param number_of_vertices: the new number of vertices
        :return: None
        """
        self.number_of_vertices = number_of_vertices

    def get_cost_of_an_edge(self, source, destination):
        """
        Getter for the cost of an edge
        :param source: the source vertex
        :param destination: the destination vertex
        :return: the cost of the edge
        """
        if self.check_if_edge_exists(source, destination):
            return self.costs[(source, destination)]
        else:
            raise GraphException("There is no edge from {source} to {destination}")

    def set_cost_of_an_edge(self, source, destination, cost):
        """
        Setter for the cost of an edge
        :param source: the source vertex
        :param destination: the destination vertex
        :param cost: the new cost of the edge
        :return: None
        """
        if self.check_if_edge_exists(source, destination):
            self.costs[(source, destination)] = cost
        else:
            self.add_edge(source, destination, cost)

    def get_vertices(self):
        """
        Getter for all the vertices in the graph
        :return: a list of vertices
        """
        return list(self.inbound_edges.keys())

    def check_if_edge_exists(self, source, destination) -> bool:
        """
        Checks if an edge exists between two vertices
        :param source: the source vertex
        :param destination: the destination vertex
        :return: True if the edge exists, False otherwise
        """
        return (source, destination) in self.costs

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph
        :param vertex: the vertex to be added
        :return: None
        """
        if vertex in self.inbound_edges:
            raise GraphException("The vertex already exists")

        self.inbound_edges[vertex] = []
        self.outbound_edges[vertex] = []
        self.number_of_vertices += 1

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph
        :param vertex: the vertex to be removed
        :return: None
        """
        if vertex not in self.inbound_edges:
            raise GraphException("The vertex does not exist")

        if vertex in self.inbound_edges:
            self.number_of_vertices -= 1
            self.number_of_edges -= len(self.inbound_edges[vertex]) + len(self.outbound_edges[vertex])
            for inbound_vertex in self.inbound_edges[vertex]:
                del self.costs[(vertex, inbound_vertex)]
                del self.outbound_edges[inbound_vertex][vertex]
            for outbound_vertex in self.outbound_edges[vertex]:
                del self.costs[(vertex, outbound_vertex)]
                del self.inbound_edges[outbound_vertex][vertex]
            del self.inbound_edges[vertex]
            del self.outbound_edges[vertex]

    def add_edge(self, source, destination, cost):
        """
        Adds an edge to the graph
        :param source: the source vertex
        :param destination: the destination vertex
        :param cost: the cost of the edge
        :return: None
        """
        if self.check_if_edge_exists(source, destination):
            raise GraphException("The edge already exists")
        try:
            self.add_vertex(source)
        except GraphException:
            pass
        try:
            self.add_vertex(destination)
        except GraphException:
            pass

        if source not in self.outbound_edges:
            self.outbound_edges[source] = []
        if destination not in self.inbound_edges:
            self.inbound_edges[destination] = []

        self.outbound_edges[source].append(destination)
        self.inbound_edges[destination].append(source)
        self.costs[(source, destination)] = cost
        self.number_of_edges += 1

    def remove_edge(self, source, destination):
        """
        Removes an edge from the graph
        :param source: the source vertex
        :param destination: the destination vertex
        :return: None
        """
        if self.check_if_edge_exists(source, destination):
            del self.costs[(source, destination)]
            self.outbound_edges[source].remove(destination)
            self.inbound_edges[destination].remove(source)
            self.number_of_edges -= 1
            return
        raise GraphException("The edge does not exist")

    def get_copy_of_graph(self):
        """
        Creates a copy of the graph
        :return: a copy of the graph
        """
        graph_copy = DirectedGraph(self.number_of_vertices)
        graph_copy.inbound_edges = copy.deepcopy(self.inbound_edges)
        graph_copy.outbound_edges = copy.deepcopy(self.outbound_edges)
        graph_copy.costs = copy.deepcopy(self.costs)
        return graph_copy

    def create_random_graph(self, number_of_vertices, number_of_edges):
        """
        Creates a random graph with a given number of vertices and edges
        :param number_of_vertices: the number of vertices
        :param number_of_edges: the number of edges
        :return: None
        """
        if number_of_edges > number_of_vertices * (number_of_vertices - 1):
            raise GraphException("Invalid input! The number of edges must be less than the number of vertices * (number of vertices - 1)")
        if self.number_of_vertices != 0:
            raise GraphException("The graph already exists.")

        for i in range(number_of_vertices):
            self.add_vertex(i)

        possible_edges = [(i, j) for i in range(number_of_vertices) for j in range(number_of_vertices) if i != j]
        num_edges = number_of_edges
        for source, destination in possible_edges:
            cost = randint(1, 100)
            self.add_edge(source, destination, cost)
            num_edges -= 1
            if num_edges == 0:
                break

    def read_graph_from_file(self, file_name):
        """
        Reads a graph from a file
        :param file_name: the name of the file to read from
        :return: None
        """
        with open(file_name, 'r') as file:
            self.number_of_edges = 0
            self.number_of_vertices = 0
            self.inbound_edges = {}
            self.outbound_edges = {}
            self.costs = {}

            number_of_vertices, number_of_edges = file.readline().split()
            number_of_edges = int(number_of_edges)
            number_of_vertices = int(number_of_vertices)

            for vertex in range(number_of_vertices):
                self.add_vertex(vertex)

            while number_of_edges:
                line = file.readline().split()
                source, destination, cost = line[0], line[1], line[2]
                self.add_edge(int(source), int(destination), int(cost))
                number_of_edges -= 1

    def write_graph_to_file(self, file_name):
        """
        Writes the graph to a file
        :param file_name: the name of the file to write to
        :return: None
        """
        with open(file_name, 'w') as file:
            file.write(f"{self.number_of_vertices} {self.number_of_edges}\n")
            for vertex, outbound_edges in self.outbound_edges.items():
                for outbound_edge in outbound_edges:
                    file.write(f"{vertex} {outbound_edge} {self.costs[(vertex, outbound_edge)]}\n")
