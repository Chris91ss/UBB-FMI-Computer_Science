from colorama import Fore
from graph_exceptions import GraphException
from undirectedGraph.undirected_graph import UndirectedGraph


class UndirectedGraphUI:
    def __init__(self):
        self.__graph = UndirectedGraph()
        self.__original_graph = None

    def run_app(self):
        print(Fore.MAGENTA + "~~~ 🌟🐍 Graph Algorithms in Python! 🐍🌟 ~~~\n")

        input_options = {
            "1": self.__get_number_of_vertices,
            "2": self.__print_the_graph,
            "3": self.__print_the_vertices_of_the_graph,
            "4": self.__check_if_edge_exists_between_two_vertices,
            "5": self.__get_cost_of_an_edge,
            "6": self.__modify_cost_of_an_edge,
            "7": self.__add_vertex,
            "8": self.__remove_vertex,
            "9": self.__add_edge,
            "10": self.__remove_edge,
            "copy": self.__create_a_copy_of_the_current_graph,
            "restore": self.__restore_the_graph_to_the_copy,
            "create": self.__create_a_random_graph,
            "read": self.__read_from_file,
            "write": self.__write_to_file,
            "bfs": self.__find_connected_components_using_bfs,
            "2-2B": self.__find_biconnected_components_using_tarjans_algorithm,
            "pw-5": self.__find_a_clique_of_maximum_size
        }

        while True:
            UndirectedGraphUI.print_menu()
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
        print(Fore.LIGHTYELLOW_EX + "4.", Fore.BLUE + "Given two vertices, "
                                                      "find out whether there is an edge from the first one to the second one")
        print(Fore.LIGHTYELLOW_EX + "5.", Fore.BLUE + "Get the cost of an edge")
        print(Fore.LIGHTYELLOW_EX + "6.", Fore.BLUE + "Modify the cost of an edge")
        print(Fore.LIGHTYELLOW_EX + "7.", Fore.BLUE + "Add a vertex")
        print(Fore.LIGHTYELLOW_EX + "8.", Fore.BLUE + "Remove a vertex")
        print(Fore.LIGHTYELLOW_EX + "9.", Fore.BLUE + "Add an edge")
        print(Fore.LIGHTYELLOW_EX + "10.", Fore.BLUE + "Remove an edge")
        print(Fore.LIGHTYELLOW_EX + "copy.", Fore.BLUE + "Create a copy of the current graph")
        print(Fore.LIGHTYELLOW_EX + "restore.", Fore.BLUE + "Restore the graph to the copy")
        print(Fore.LIGHTYELLOW_EX + "create.", Fore.BLUE + "Create a random graph")
        print(Fore.LIGHTYELLOW_EX + "read.", Fore.BLUE + "Read a graph from a file")
        print(Fore.LIGHTYELLOW_EX + "write.", Fore.BLUE + "Write the graph to a file")
        print(Fore.LIGHTYELLOW_EX + "bfs.", Fore.BLUE + "Find the connected components using a breadth-first traversal of the graph")
        print(Fore.LIGHTYELLOW_EX + "2-2B.", Fore.BLUE + "Find the biconnected components of an undirected graph in O(n+m)"
                                                       " (using Tarjan's algorithm)")
        print(Fore.LIGHTYELLOW_EX + "pw-5.", Fore.BLUE + "Find a clique of maximum size")
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

    def __find_connected_components_using_bfs(self):
        print("The connected components are: ")
        components = self.__graph.connected_components()
        for component in components:
            print(component)

    def __find_biconnected_components_using_tarjans_algorithm(self):
        self.__graph.BCC()
        print("Above are % d biconnected components in graph" % self.__graph.count)

    def __find_a_clique_of_maximum_size(self):
        max_clique = self.__graph.find_max_clique()
        print("The maximum clique is: ", max_clique)
