from graph_exceptions import GraphException
import copy
from random import randint


class DirectedGraph:

    def __init__(self, number_of_vertices=0):
        self.number_of_vertices = number_of_vertices
        self.number_of_edges = 0
        self.inbound_edges = {}
        self.outbound_edges = {}
        self.costs = {}

    def __str__(self):
        string = f"DirectedGraph: {self.number_of_vertices} vertices, {self.number_of_edges} edges"
        for vertex, inbound_edges in self.inbound_edges.items():
            for inbound_edge in inbound_edges:
                if not inbound_edges and not self.outbound_edges[vertex]:
                    string += f"\n {vertex} -> isolated vertex"
                    continue

                string += f"\n {inbound_edge} -> {vertex} ->: {self.costs[(inbound_edge, vertex)]}"

        return string

    def get_number_of_vertices(self):
        return self.number_of_vertices

    def set_number_of_vertices(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices

    def get_cost_of_an_edge(self, source, destination):
        if self.check_if_edge_exists(source, destination):
            return self.costs[(source, destination)]
        else:
            raise GraphException("There is no edge from {source} to {destination}")

    def set_cost_of_an_edge(self, source, destination, cost):
        if self.check_if_edge_exists(source, destination):
            self.costs[(source, destination)] = cost
        else:
            self.add_edge(source, destination, cost)

    def get_vertices(self):
        return list(self.inbound_edges.keys())

    def check_if_edge_exists(self, source, destination) -> bool:
        return (source, destination) in self.costs

    def add_vertex(self, vertex):
        if vertex in self.inbound_edges:
            raise GraphException("The vertex already exists")

        self.inbound_edges[vertex] = []
        self.outbound_edges[vertex] = []
        self.number_of_vertices += 1

    def remove_vertex(self, vertex):
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
        if self.check_if_edge_exists(source, destination):
            del self.costs[(source, destination)]
            self.outbound_edges[source].remove(destination)
            self.inbound_edges[destination].remove(source)
            self.number_of_edges -= 1
            return
        raise GraphException("The edge does not exist")

    def get_copy_of_graph(self):
        graph_copy = DirectedGraph(self.number_of_vertices)
        graph_copy.inbound_edges = copy.deepcopy(self.inbound_edges)
        graph_copy.outbound_edges = copy.deepcopy(self.outbound_edges)
        graph_copy.costs = copy.deepcopy(self.costs)
        return graph_copy

    def create_random_graph(self, number_of_vertices, number_of_edges):
        if number_of_edges > number_of_vertices ** 2:
            raise GraphException("Invalid input! The number of edges must be less than the number of vertices squared.")
        if self.number_of_vertices != 0:
            raise GraphException("The graph already exists.")

        for i in range(number_of_vertices):
            self.add_vertex(i)
        for i in range(number_of_edges):
            source = randint(0, number_of_vertices - 1)
            destination = randint(0, number_of_vertices - 1)
            cost = randint(1, 100)
            self.add_edge(source, destination, cost)

    def read_graph_from_file(self, file_name):
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
        with open(file_name, 'w') as file:
            file.write(f"{self.number_of_vertices} {self.number_of_edges}\n")
            for vertex, outbound_edges in self.outbound_edges.items():
                for outbound_edge in outbound_edges:
                    file.write(f"{vertex} {outbound_edge} {self.costs[(vertex, outbound_edge)]}\n")
