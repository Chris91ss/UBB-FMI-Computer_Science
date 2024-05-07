from collections import deque, defaultdict
from random import randint
from graph_exceptions import GraphException


class UndirectedGraph:
    def __init__(self, number_of_vertices=0):
        """
        Constructor for the UndirectedGraph class
        :param number_of_vertices: the number of vertices in the graph
        """
        self.number_of_vertices = number_of_vertices
        self.number_of_edges = 0
        self.edges = defaultdict(set)
        self.costs = {}
        # time is used to find discovery times
        self.Time = 0
        # Count is number of biconnected components
        self.count = 0

    def __str__(self):
        """
        Returns a string representation of the graph
        """
        string = f"UndirectedGraph: {self.number_of_vertices} vertices, {self.number_of_edges} edges"
        for vertex, connected_vertices in self.edges.items():
            for connected_vertex in connected_vertices:
                try:
                    if vertex < connected_vertex:  # To avoid duplicate edges
                        cost = 0
                        if (vertex, connected_vertex) in self.costs:
                            cost = self.costs[(vertex, connected_vertex)]
                        string += f"\n {vertex} <-> {connected_vertex}: {cost}"
                except GraphException:
                    pass

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
        return list(self.edges.keys())

    def get_neighbors(self, vertex):
        return self.edges[vertex]

    def check_if_edge_exists(self, vertex1, vertex2) -> bool:
        """
        Checks if an edge exists between two vertices
        :param vertex1: one of the vertices
        :param vertex2: the other vertex
        :return: True if the edge exists, False otherwise
        """
        if vertex1 in self.edges and vertex2 in self.edges[vertex1]:
            return True
        return False

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph
        :param vertex: the vertex to be added
        :return: None
        """
        if vertex in self.edges:
            raise GraphException("The vertex already exists")

        if vertex not in self.edges:
            self.edges[vertex] = set()
            self.number_of_vertices += 1

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph
        :param vertex: the vertex to be removed
        :return: None
        """
        if vertex not in self.edges:
            raise GraphException("The vertex does not exist")

        if vertex in self.edges:
            for connected_vertex in self.edges[vertex]:
                self.edges[connected_vertex].remove(vertex)
                self.number_of_edges -= 1
            del self.edges[vertex]
            self.number_of_vertices -= 1

    def add_edge(self, vertex1, vertex2, cost):
        """
        Adds an edge to the graph
        :param vertex1: one of the vertices
        :param vertex2: the other vertex
        :param cost: the cost of the edge
        :return: None
        """
        if self.check_if_edge_exists(vertex1, vertex2):
            raise GraphException("The edge already exists")

        if not self.check_if_edge_exists(vertex1, vertex2):
            try:
                self.add_vertex(vertex1)
            except GraphException:
                pass
            try:
                self.add_vertex(vertex2)
            except GraphException:
                pass
            self.edges[vertex1].add(vertex2)
            self.edges[vertex2].add(vertex1)
            self.costs[(vertex1, vertex2)] = cost
            self.number_of_edges += 1

    def remove_edge(self, vertex1, vertex2):
        """
        Removes an edge from the graph
        :param vertex1: one of the vertices
        :param vertex2: the other vertex
        :return: None
        """
        if self.check_if_edge_exists(vertex1, vertex2):
            self.edges[vertex1].remove(vertex2)
            self.edges[vertex2].remove(vertex1)
            del self.costs[(vertex1, vertex2)]
            self.number_of_edges -= 1
            return
        raise GraphException("The edge does not exist")

    def get_copy_of_graph(self):
        """
        Creates a copy of the graph
        :return: a copy of the graph
        """
        graph_copy = UndirectedGraph(self.number_of_vertices)
        graph_copy.edges = {vertex: set(neighbors) for vertex, neighbors in self.edges.items()}
        graph_copy.costs = self.costs.copy()
        return graph_copy

    def create_random_graph(self, number_of_vertices, number_of_edges):
        """
        Creates a random graph with a given number of vertices and edges
        :param number_of_vertices: the number of vertices
        :param number_of_edges: the number of edges
        :return: None
        """
        if number_of_edges > number_of_vertices * (number_of_vertices - 1) / 2:
            raise GraphException("Invalid input! The number of edges must be less than"
                                 " or equal to (number of vertices * (number of vertices - 1)) / 2")
        if self.number_of_vertices != 0:
            raise GraphException("The graph already exists.")

        for i in range(number_of_vertices):
            self.add_vertex(i)

        num_edges = number_of_edges
        while num_edges > 0:
            source = randint(0, number_of_vertices - 1)
            destination = randint(0, number_of_vertices - 1)
            if source != destination and not self.check_if_edge_exists(source, destination):
                cost = randint(1, 100)
                self.add_edge(source, destination, cost)
                num_edges -= 1

    def read_graph_from_file(self, file_name):
        """
        Reads a graph from a file
        :param file_name: the name of the file to read from
        :return: None
        """
        with open(file_name, 'r') as file:
            self.number_of_edges = 0
            self.number_of_vertices = 0
            self.costs = {}

            number_of_vertices, number_of_edges = file.readline().split()
            number_of_edges = int(number_of_edges)
            number_of_vertices = int(number_of_vertices)

            for vertex in range(number_of_vertices):
                self.add_vertex(vertex)

            while number_of_edges:
                line = file.readline().split()
                source, destination, cost = line[0], line[1], line[2]
                try:
                    self.add_edge(int(source), int(destination), int(cost))
                except GraphException:
                    pass
                number_of_edges -= 1

    def write_graph_to_file(self, file_name):
        """
        Writes the graph to a file
        :param file_name: the name of the file to write to
        :return: None
        """
        with open(file_name, 'w') as file:
            file.write(f"{self.number_of_vertices} {self.number_of_edges}\n")
            for vertex, connected_vertices in self.edges.items():
                for connected_vertex in connected_vertices:
                    if vertex < connected_vertex:  # To avoid duplicate edges
                        file.write(f"{vertex} {connected_vertex} {self.costs[(vertex, connected_vertex)]}\n")

    def breadth_first_search(self, start_vertex, visited):
        """
        Perform breadth-first search starting from a given vertex.
        :param start_vertex: the starting vertex
        :param visited: the visited vertices
        :return: a list of vertices in the connected component
        """
        component = []
        queue = deque([start_vertex])
        visited[start_vertex] = True

        while queue:
            vertex = queue.popleft()
            component.append(vertex)

            for neighbor in self.edges[vertex]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)

        return component

    def connected_components(self):
        """
        Find connected components of an undirected graph.
        :return: a list of connected components
        """
        visited = {vertex: False for vertex in self.get_vertices()}
        components = []

        for vertex in self.get_vertices():
            if not visited[vertex]:
                component = self.breadth_first_search(vertex, visited)
                components.append(component)

        return components

    def BCCUtil(self, u, parent, low, disc, st, visited):
        """
        Utility function to find biconnected components in an undirected graph.
        :param u: the vertex
        :param parent: the parent of the vertices
        :param low: the lowest discovery time of the vertices
        :param disc: the discovery times of the vertices
        :param st: the stack
        :param visited: the visited vertices
        """
        children = 0
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1

        for v in self.edges[u]:
            if disc[v] == -1:
                parent[v] = u
                children += 1
                st.append((u, v))
                self.BCCUtil(v, parent, low, disc, st, visited)

                low[u] = min(low[u], low[v])

                if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                    self.count += 1
                    w = (-1, -1)
                    while w != (u, v):
                        w = st.pop()
                        print(w, end=" ")
                    print()
            elif v != parent[u] and low[u] > disc[v]:
                low[u] = min(low[u], disc[v])
                st.append((u, v))

    def BCC(self):
        """
        Find biconnected components in an undirected graph.
        """
        disc = [-1] * self.number_of_vertices
        low = [-1] * self.number_of_vertices
        parent = [-1] * self.number_of_vertices
        st = []
        visited = {vertex: False for vertex in range(self.number_of_vertices)}

        for i in range(self.number_of_vertices):
            if disc[i] == -1:
                self.BCCUtil(i, parent, low, disc, st, visited)
            if st:
                self.count += 1

                while st:
                    w = st.pop()
                    print(w, end=" ")
                print()

    def bron_kerbosch(self, clique=None, candidates=None, excluded=None):
        if clique is None:
            clique = set()
        if candidates is None:
            candidates = set(self.get_vertices())
        if excluded is None:
            excluded = set()
        if not candidates and not excluded:
            yield clique
        else:
            for vertex in list(candidates):
                new_candidates = candidates.intersection(self.get_neighbors(vertex))
                new_excluded = excluded.intersection(self.get_neighbors(vertex))
                for result in self.bron_kerbosch(clique | {vertex}, new_candidates, new_excluded):
                    yield result
                candidates.remove(vertex)
                excluded.add(vertex)

    def find_max_clique(self):
        cliques = list(self.bron_kerbosch())
        max_clique = max(cliques, key=len)
        return max_clique
