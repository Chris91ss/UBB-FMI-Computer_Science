import copy
import heapq
from random import randint

from graph_exceptions import GraphException


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

    def get_inbound_edges_degree(self, vertex):
        len(self.inbound_edges[vertex])

    def get_outbound_edges_degree(self, vertex):
        len(self.outbound_edges[vertex])

    def check_if_edge_exists(self, source, destination) -> bool:
        """
        Checks if an edge exists between two vertices
        :param source: the source vertex
        :param destination: the destination vertex
        :return: True if the edge exists, False otherwise
        """
        if source in self.inbound_edges and destination in self.outbound_edges[source]:
            return True
        return False

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

    def _dfs_forward(self, vertex, visited, stack):
        """
        Depth-first search for the strongly connected components algorithm
        :param vertex: vertex to start the search from
        :param visited: dictionary of visited vertices
        :param stack: stack to store the vertices
        :return: None
        """
        visited[vertex] = True
        for neighbor in self.outbound_edges[vertex]:
            if not visited[neighbor]:
                self._dfs_forward(neighbor, visited, stack)
        stack.append(vertex)

    def _dfs_reverse(self, vertex, visited, component):
        """
        Depth-first search in the reverse graph for the strongly connected components algorithm
        :param vertex: vertex to start the search from
        :param visited: dictionary of visited vertices
        :param component: list to store the vertices
        :return: None
        """
        visited[vertex] = True
        component.append(vertex)
        for neighbor in self.inbound_edges[vertex]:
            if not visited[neighbor]:
                self._dfs_reverse(neighbor, visited, component)

    def _transpose(self):
        """
        Creates the transpose of the graph
        :return: the transpose of the graph
        """
        transposed_graph = DirectedGraph(self.number_of_vertices)
        for source, destinations in self.inbound_edges.items():
            for destination in destinations:
                transposed_graph.add_edge(destination, source, self.costs.get((source, destination), 0))
        return transposed_graph

    def strongly_connected_components(self):
        """
        Finds the strongly connected components of the graph
        :return: a list of strongly connected components
        """
        stack = []
        visited = {vertex: False for vertex in self.outbound_edges}

        for vertex in self.outbound_edges:
            if not visited[vertex]:
                self._dfs_forward(vertex, visited, stack)

        transposed_graph = self._transpose()
        visited = {vertex: False for vertex in self.inbound_edges}

        components = []
        while stack:
            vertex = stack.pop()
            if not visited[vertex]:
                component = []
                transposed_graph._dfs_reverse(vertex, visited, component)
                components.append(component)

        return components

    def dijkstra(self, start, end):
        """
        Dijkstra algorithm for finding the shortest path between two vertices
        :param start: start vertex to find the path from
        :param end: end vertex to find the path to
        :return: a tuple containing the path and the cost of the path
        """
        distances = {vertex: float('inf') for vertex in self.outbound_edges}
        distances[start] = 0
        previous = {vertex: None for vertex in self.outbound_edges}
        visited = {vertex: False for vertex in self.outbound_edges}
        heap = [(0, start)]

        while heap:
            current_distance, current_vertex = heapq.heappop(heap)
            if current_distance > distances[current_vertex]:
                continue
            visited[current_vertex] = True

            for neighbor in self.outbound_edges[current_vertex]:
                if visited[neighbor]:
                    continue
                new_distance = current_distance + self.costs.get((current_vertex, neighbor), 0)
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(heap, (new_distance, neighbor))

        path = []
        current_vertex = end
        while previous[current_vertex] is not None:
            path.append(current_vertex)
            current_vertex = previous[current_vertex]
        path.append(start)
        path.reverse()
        return path, distances[end]

    def number_of_distinct_walks_of_minimum_cost_dijkstra(self, start, end):
        """
        Finds the number of distinct walks of minimum cost between two vertices
        :param start: start vertex to find the walks from
        :param end: end vertex to find the walks to
        :return: the number of distinct walks of minimum cost
        """
        distances = {vertex: float('inf') for vertex in self.outbound_edges}
        distances[start] = 0
        previous = {vertex: [] for vertex in self.outbound_edges}
        visited = {vertex: False for vertex in self.outbound_edges}
        heap = [(0, start)]

        while heap:
            current_distance, current_vertex = heapq.heappop(heap)
            if current_distance > distances[current_vertex]:
                continue
            visited[current_vertex] = True

            for neighbor in self.outbound_edges[current_vertex]:
                if visited[neighbor]:
                    continue
                new_distance = current_distance + self.costs.get((current_vertex, neighbor), 0)
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = [current_vertex]
                    heapq.heappush(heap, (new_distance, neighbor))
                elif new_distance == distances[neighbor]:
                    previous[neighbor].append(current_vertex)

        def dfs(vertex):
            if vertex == start:
                return 1
            count = 0
            for _neighbor in previous[vertex]:
                count += dfs(_neighbor)
            return count

        return dfs(end)

    def number_of_distinct_walks_between_two_vertices(self, start, end):
        """
        Finds the number of distinct walks between two vertices
        :param start: start vertex to find the walks from
        :param end: end vertex to find the walks to
        :return: the number of distinct walks
        """
        if start == end:
            return 1
        visited = {vertex: False for vertex in self.outbound_edges}
        count = 0

        def dfs(vertex):
            nonlocal count
            visited[vertex] = True
            if vertex == end:
                count += 1
            else:
                for neighbor in self.outbound_edges[vertex]:
                    if not visited[neighbor]:
                        dfs(neighbor)
            visited[vertex] = False

        dfs(start)
        return count

    @staticmethod
    def solve_bridge_and_torch(times):
        """
        Solves the bridge and torch problem using a priority queue.
        :param times: a list of times needed for each person to cross the bridge
        :return: the minimum total time needed for all people to cross the bridge
        """
        if not times:
            return 0

        times.sort()
        queue = []
        total_time = 0

        while len(times) > 3:
            # Two fastest on the right side go to the left
            first, second = times[:2]
            total_time += second
            queue.append(first)
            queue.append(second)
            times = times[2:]
            # The fastest on the left goes back to the right
            fastest = heapq.heappop(queue)
            times.append(fastest)
            total_time += fastest
            times.sort()

        if len(times) == 3:
            total_time += times[0] + times[1] + times[2]
        elif len(times) == 2:
            total_time += times[1]
        else:  # len(times) == 1
            total_time += times[0]

        return total_time

    def create_times_list(self):
        """
        Creates a list of times from the costs dictionary.
        :return: a list of times
        """
        times = []
        for edge, cost in self.costs.items():
            times.append(cost)
        return times
