from directedGraph.directed_graph import DirectedGraph
from graph_exceptions import GraphException
from colorama import Fore


class DirectedGraphUI:
    def __init__(self):
        self.__graph = DirectedGraph()
        self.__original_graph = None

    def run_app(self):
        print(Fore.MAGENTA + "~~~ 🌟🐍 Graph Algorithms in Python! 🐍🌟 ~~~\n")

        input_options = {
            "1": self.__get_number_of_vertices,
            "2": self.__print_the_graph,
            "3": self.__print_the_vertices_of_the_graph,
            "4": self.__check_if_edge_exists_between_two_vertices,
            "5": self.__get_in_degree_and_out_degree_of_a_vertex,
            "6": self.__print_the_inbound_edges_of_a_vertex,
            "7": self.__print_the_outbound_edges_of_a_vertex,
            "8": self.__get_cost_of_an_edge,
            "9": self.__modify_cost_of_an_edge,
            "10": self.__add_vertex,
            "11": self.__remove_vertex,
            "12": self.__add_edge,
            "13": self.__remove_edge,
            "copy": self.__create_a_copy_of_the_current_graph,
            "restore": self.__restore_the_graph_to_the_copy,
            "create": self.__create_a_random_graph,
            "read": self.__read_from_file,
            "write": self.__write_to_file,
            "2-1B": self.__find_strongly_connected_components_using_kosarajus_algorithm,
            "3-1": self.__find_lowest_cost_walk_dijkstra,
            "3-1B": self.__find_number_of_distinct_walks_of_minimum_cost,
            "3-2B": self.__find_number_of_distinct_walks_between_two_vertices,
            "3-3B": self.__solve_bridge_and_torch_problem,
            "4-1": self.__practical_work_no4_1,
            "4-2B": self.__practical_work_no4_2b,
            "4-3B": self.__practical_work_no4_3b
        }

        while True:
            DirectedGraphUI.print_menu()
            command = input(Fore.GREEN + "Enter a command: ")
            try:
                if command == "exit":
                    print(Fore.MAGENTA + "Goodbye! 🌟🐍")
                    break
                input_options[command]()
            except KeyError:
                print("Invalid command")

    @staticmethod
    def print_menu():
        print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Get the number of vertices")
        print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Print the graph")
        print(Fore.LIGHTYELLOW_EX + "3.", Fore.BLUE + "Print the vertices of the graph")
        print(Fore.LIGHTYELLOW_EX + "4.",
              Fore.BLUE + "Given two vertices, find out whether there is an edge from the first one to the second one")
        print(Fore.LIGHTYELLOW_EX + "5.", Fore.BLUE + "Get the in degree and out degree of a vertex")
        print(Fore.LIGHTYELLOW_EX + "6.", Fore.BLUE + "Print the inbound edges of a vertex")
        print(Fore.LIGHTYELLOW_EX + "7.", Fore.BLUE + "Print the outbound edges of a vertex")
        print(Fore.LIGHTYELLOW_EX + "8.", Fore.BLUE + "Get the cost of an edge")
        print(Fore.LIGHTYELLOW_EX + "9.", Fore.BLUE + "Modify the cost of an edge")
        print(Fore.LIGHTYELLOW_EX + "10.", Fore.BLUE + "Add a vertex")
        print(Fore.LIGHTYELLOW_EX + "11.", Fore.BLUE + "Remove a vertex")
        print(Fore.LIGHTYELLOW_EX + "12.", Fore.BLUE + "Add an edge")
        print(Fore.LIGHTYELLOW_EX + "13.", Fore.BLUE + "Remove an edge")
        print(Fore.LIGHTYELLOW_EX + "copy.", Fore.BLUE + "Create a copy of the current graph")
        print(Fore.LIGHTYELLOW_EX + "restore.", Fore.BLUE + "Restore the graph to the copy")
        print(Fore.LIGHTYELLOW_EX + "create.", Fore.BLUE + "Create a random graph")
        print(Fore.LIGHTYELLOW_EX + "read.", Fore.BLUE + "Read a graph from a file")
        print(Fore.LIGHTYELLOW_EX + "write.", Fore.BLUE + "Write the graph to a file")
        print(Fore.LIGHTYELLOW_EX + "2-1B.", Fore.BLUE + "Find the strongly connected components using Kosaraju's algorithm")
        print(Fore.LIGHTYELLOW_EX + "3-1.", Fore.BLUE + "Find the lowest cost walk between the given vertices, using Dijkstra's algorithm")
        print(Fore.LIGHTYELLOW_EX + "3-1B.", Fore.BLUE + "Given a graph with costs, having no negative cost cycles, and a pair of vertices,"
                                                         " finds the number of distinct walks of minimum cost between the given vertices.")
        print(Fore.LIGHTYELLOW_EX + "3-2B.", Fore.BLUE + "Given a graph that has no cycles (a directed acyclic graph, DAG) "
                                                         "and a pair of vertices, finds the number of distinct walks between the given vertices")
        print(Fore.LIGHTYELLOW_EX + "3-3B.", Fore.BLUE + "Solve the bridge and torch problem")
        print(Fore.LIGHTYELLOW_EX + "4-1.", Fore.BLUE + "Practical work no. 4.1 - given a list of activities with duration and list of "
                                                        "prerequisites for each activity")
        print(Fore.BLUE + "           -verify if the corresponding graph is a DAG and performs a topological sorting of the activities using"
                          " the algorithm based on depth-first traversal (Tarjan's algorithm).")
        print(Fore.BLUE + "           -prints the earliest and the latest starting time for each activity and the total time of the project.")
        print(Fore.BLUE + "           -prints the critical activities.")
        print(Fore.LIGHTYELLOW_EX + "4-2B.", Fore.BLUE + "Practical work no. 4.2B- given a graph, do the following: ")
        print(Fore.BLUE + "           -verify if the corresponding graph is a DAG and performs a topological sorting of the activities.")
        print(Fore.BLUE + "           -if it is a DAG, finds the number of distinct paths between two given vertices, in O(m+n).")
        print(Fore.LIGHTYELLOW_EX + "4-3B.", Fore.BLUE + "Practical work no. 4.3B- given a graph with costs, do the following: ")
        print(Fore.BLUE + "           -verify if the corresponding graph is a DAG and performs a topological sorting of the activities;")
        print(Fore.BLUE + "           -if it is a DAG, finds the number of distinct lowest cost paths between two given vertices, in O(m+n).")
        print(Fore.LIGHTYELLOW_EX + "exit.", Fore.BLUE + "Exit the application")

    def __get_number_of_vertices(self):
        print(f" The number of vertices is: {self.__graph.get_number_of_vertices()}")

    def __print_the_graph(self):
        print("The graph is: ")
        print(self.__graph)

    def __print_the_vertices_of_the_graph(self):
        print(f"The vertices of the graph are: {self.__graph.get_vertices()}")

    def __check_if_edge_exists_between_two_vertices(self):
        source = int(input("Enter the source vertex: "))
        destination = int(input("Enter the destination vertex: "))
        try:
            if self.__graph.check_if_edge_exists(source, destination):
                print(f"There is an edge from {source} to {destination}")
            else:
                print(f"There is no edge from {source} to {destination}")
        except GraphException:
            print(f"There is no edge from {source} to {destination}")

    def __get_in_degree_and_out_degree_of_a_vertex(self):
        vertex = int(input("Enter the vertex: "))
        try:
            in_degree = self.__graph.get_inbound_edges_degree(vertex)
            out_degree = self.__graph.get_outbound_edges_degree(vertex)
            print(f"The in degree of {vertex} is {in_degree} and the out degree of {vertex} is {out_degree}")
        except KeyError:
            print(f"The vertex {vertex} is not in the current graph.")

    def __print_the_inbound_edges_of_a_vertex(self):
        vertex = int(input("Enter the vertex: "))
        try:
            print(f"The inbound edges of {vertex} are: {self.__graph.inbound_edges[vertex]}")
        except KeyError:
            print(f"The vertex {vertex} is not in the current graph.")

    def __print_the_outbound_edges_of_a_vertex(self):
        vertex = int(input("Enter the vertex: "))
        try:
            print(f"The outbound edges of {vertex} are: {self.__graph.outbound_edges[vertex]}")
        except KeyError:
            print(f"The vertex {vertex} is not in the current graph.")

    def __get_cost_of_an_edge(self):
        source = int(input("Enter the source vertex: "))
        destination = int(input("Enter the destination vertex: "))
        try:
            print(f"The cost of the edge from {source} to {destination} is {self.__graph.get_cost_of_an_edge(source, destination)}")
        except GraphException:
            print(f"There is no edge from {source} to {destination}")

    def __modify_cost_of_an_edge(self):
        source = int(input("Enter the source vertex: "))
        destination = int(input("Enter the destination vertex: "))
        cost = int(input("Enter the new cost: "))
        try:
            self.__graph.set_cost_of_an_edge(source, destination, cost)
            print(f"The cost of the edge from {source} to {destination} has been modified to {cost}")
        except GraphException:
            print(f"There is no edge from {source} to {destination}")

    def __add_vertex(self):
        vertex = int(input("Enter the vertex: "))
        try:
            self.__graph.add_vertex(vertex)
            print(f"The vertex {vertex} has been added to the graph")
        except GraphException:
            print(f"The vertex {vertex} is already in the graph")

    def __remove_vertex(self):
        vertex = int(input("Enter the vertex: "))
        try:
            self.__graph.remove_vertex(vertex)
            print(f"The vertex {vertex} has been removed from the graph")
        except GraphException:
            print(f"The vertex {vertex} is not in the graph")

    def __add_edge(self):
        source = int(input("Enter the source vertex: "))
        destination = int(input("Enter the destination vertex: "))
        cost = int(input("Enter the cost of the edge: "))
        try:
            self.__graph.add_edge(source, destination, cost)
            print(f"The edge from {source} to {destination} with cost {cost} has been added to the graph")
        except GraphException:
            print(f"The edge from {source} to {destination} with cost {cost} is already in the graph")

    def __remove_edge(self):
        source = int(input("Enter the source vertex: "))
        destination = int(input("Enter the destination vertex: "))
        try:
            self.__graph.remove_edge(source, destination)
            print(f"The edge from {source} to {destination} has been removed from the graph")
        except GraphException:
            print(f"The edge from {source} to {destination} is not in the graph")

    def __create_a_copy_of_the_current_graph(self):
        if self.__original_graph is not None:
            print("There is already a copy of the graph")
            return

        self.__original_graph = self.__graph
        self.__graph = self.__graph.get_copy_of_graph()
        print("The current graph has been copied")

    def __restore_the_graph_to_the_copy(self):
        if self.__original_graph is None:
            print("There is no copy of the graph")
            return

        self.__graph = self.__original_graph
        self.__original_graph = None
        print("The graph has been restored to the copy")

    def __create_a_random_graph(self):
        number_of_vertices = int(input("Enter the number of vertices: "))
        number_of_edges = int(input("Enter the number of edges: "))
        try:
            self.__graph.create_random_graph(number_of_vertices, number_of_edges)
        except GraphException as ge:
            print(ge)
            return
        print(f"A random graph with {number_of_vertices} vertices and {number_of_edges} edges has been created")

    def __read_from_file(self):
        file_name = input("Enter the file name: ")
        try:
            self.__graph.read_graph_from_file(file_name)
        except GraphException as ge:
            print(ge)
            return
        print(f"The graph has been read from the file {file_name}")

    def __write_to_file(self):
        file_name = input("Enter the file name: ")
        self.__graph.write_graph_to_file(file_name)
        print(f"The graph has been written to the file {file_name}")

    def __find_strongly_connected_components_using_kosarajus_algorithm(self):
        components = self.__graph.strongly_connected_components()
        print("The strongly connected components are:\n")
        for idx, component in enumerate(components):
            print(f"Component {idx}: {component}")

    def __find_lowest_cost_walk_dijkstra(self):
        source = int(input("Enter the source vertex: "))
        destination = int(input("Enter the destination vertex: "))
        try:
            path, cost = self.__graph.dijkstra(source, destination)
            print(f"The lowest cost walk from {source} to {destination} is {path} with cost {cost}")
        except GraphException as ge:
            print(ge)

    def __find_number_of_distinct_walks_of_minimum_cost(self):
        source = int(input("Enter the source vertex: "))
        destination = int(input("Enter the destination vertex: "))
        try:
            number_of_walks = self.__graph.number_of_distinct_walks_of_minimum_cost_dijkstra(source, destination)
            print(f"The number of distinct walks of minimum cost from {source} to {destination} is {number_of_walks}")
        except GraphException as ge:
            print(ge)

    def __find_number_of_distinct_walks_between_two_vertices(self):
        source = int(input("Enter the source vertex: "))
        destination = int(input("Enter the destination vertex: "))
        try:
            number_of_walks = self.__graph.number_of_distinct_walks_between_two_vertices(source, destination)
            print(f"The number of distinct walks from {source} to {destination} is {number_of_walks}")
        except GraphException as ge:
            print(ge)

    def __solve_bridge_and_torch_problem(self):
        try:
            times = self.__graph.create_times_list()
            print("The total time for solving the bridge and torch problem is: ", self.__graph.solve_bridge_and_torch(times))
        except GraphException as ge:
            print(ge)

    @staticmethod
    def display_graph_info(graph, durations):
        # Perform topological sort
        sorted_vertices = graph.topological_sort()
        print("Topological sort of activities: ", sorted_vertices)

        # Calculate earliest and latest start times
        earliest_times, latest_times = graph.calculate_earliest_latest_times(durations)
        print("Earliest start times for each activity: ", earliest_times)
        print("Latest start times for each activity: ", latest_times)

        # Calculate total time of the project
        total_time = max([start + duration for start, duration in zip(earliest_times, durations)])
        print("Total time of the project: ", total_time)

        # Find critical activities
        critical_activities = graph.find_critical_activities(durations)
        print("Critical activities: ", critical_activities)

    def __practical_work_no4_1(self):
        graph = DirectedGraph()
        for i in range(5):
            graph.add_vertex(i)
        durations = [2, 3, 1, 4, 2]
        graph.add_edge(0, 1, durations[0])  # Activity 0 must be completed before activity 1 can start
        graph.add_edge(0, 2, durations[0])  # Activity 0 must be completed before activity 2 can start
        graph.add_edge(1, 3, durations[1])  # Activity 1 must be completed before activity 3 can start
        graph.add_edge(2, 4, durations[2])  # Activity 2 must be completed before activity 4 can start
        graph.add_edge(3, 4, durations[3])  # Activity 3 must be completed before activity 4 can start
        self.display_graph_info(graph, durations)

    def __practical_work_no4_2b(self):
        is_DAG, sorted_vertices = self.__graph.is_DAG()
        if is_DAG:
            print("The graph is a DAG. The topological sort of the vertices is:")
            print(sorted_vertices)
            print("Input source vertex:")
            source_vertex = int(input())
            print("Input destination vertex:")
            destination_vertex = int(input())
            num_paths = self.__graph.count_paths(source_vertex, destination_vertex)
            print(f"The number of distinct paths from vertex {source_vertex} to vertex {destination_vertex} is {num_paths}.")
        else:
            print("The graph is not a DAG.")

    def __practical_work_no4_3b(self):
        is_DAG, sorted_vertices = self.__graph.is_DAG()
        if is_DAG:
            print("The graph is a DAG. The topological sort of the vertices is:")
            print(sorted_vertices)
            print("Input source vertex:")
            source_vertex = int(input())
            print("Input destination vertex:")
            destination_vertex = int(input())
            distance, count = self.__graph.shortest_paths(source_vertex, destination_vertex)
            print(f"The shortest distance from {source_vertex} to {destination_vertex} is {distance}")
            print(f"The number of distinct shortest paths is {count}")

        else:
            print("The graph is not a DAG.")
