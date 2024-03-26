from colorama import Fore


class GraphException(Exception):
    """
    Custom class for exceptions in this project.
    """
    def __init__(self, message, color=Fore.RED):
        """
        Constructor for the class.
        :param message: Exception message.
        :param color:  Color of the message.
        """
        self.__message = color + message

    def __str__(self):
        """
        Function to return the message.
        :return: Message.
        """
        return self.__message
