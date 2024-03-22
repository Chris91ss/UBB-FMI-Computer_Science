from colorama import Fore


class GraphException(Exception):
    def __init__(self, message, color=Fore.RED):
        self.__message = color + message

    def __str__(self):
        return self.__message
