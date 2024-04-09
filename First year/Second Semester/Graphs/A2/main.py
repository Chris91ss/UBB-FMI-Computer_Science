from colorama import Fore

from directedGraph.directed_graph_ui import DirectedGraphUI
from undirectedGraph.undirected_graph_ui import UndirectedGraphUI
from WolfGoatCabbage import wgc
from Puzzle15 import puzzle15


def print_menu():
    print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Directed graph")
    print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Undirected graph")
    print(Fore.LIGHTYELLOW_EX + "3.", Fore.BLUE + "Wolf, Goat, Cabbage problem solution")
    print(Fore.LIGHTYELLOW_EX + "4.", Fore.BLUE + "15-puzzle problem solution")


if __name__ == '__main__':
    directed_graph_ui = DirectedGraphUI()
    undirected_graph_ui = UndirectedGraphUI()

    input_options = {
        "1": directed_graph_ui.run_app,
        "2": undirected_graph_ui.run_app,
        "3": wgc.run_app,
        "4": puzzle15.run_app
    }

    while True:
        print_menu()
        command = input(Fore.GREEN + "Enter a command: ")
        try:
            input_options[command]()
        except KeyError:
            print("Invalid command")
