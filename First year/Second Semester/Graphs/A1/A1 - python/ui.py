from directed_graph import DirectedGraph
from graph_exceptions import GraphException
from colorama import Fore


class UI:
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
            "exit": UI.__exit_app
        }

        while True:
            UI.print_menu()
            command = input(Fore.GREEN + "Enter a command: ")
            try:
                input_options[command]()
            except KeyError:
                print("Invalid command")

    @staticmethod
    def print_menu():
        print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Get the number of vertices")
        print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Print the graph")
        print(Fore.LIGHTYELLOW_EX + "3.", Fore.BLUE + "Print the vertices of the graph")
        print(Fore.LIGHTYELLOW_EX + "4.", Fore.BLUE + "Given two vertices, find out whether there is an edge from the first one to the second one")
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

    @staticmethod
    def __exit_app():
        print(Fore.MAGENTA + "Goodbye! 🌟🐍")
        exit()
