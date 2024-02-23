from texttable import Texttable


class Board:

    def __init__(self):
        self.board = [[" " for _ in range(8)] for _ in range(8)]

    def set_alive(self, x: int, y: int):
        """
        This revives the cell on the coordinates x and y
        :param x: int, x coordinate / row
        :param y: int, y coordinate / column
        """

        self.board[x][y] = "X"

    def set_dead(self, x: int, y: int):
        """
        This kills the cell on the coordinates x and y
        :param x: int, x coordinate / row
        :param y: int, y coordinate / column
        """
        self.board[x][y] = " "

    def get_number_of_neighbors(self, x: int, y: int) -> int:
        """
        This function returns the number of neighbors a cell has
        Uses try excepts to stop it from searching for neighbors outside the grid
        :param x: int, x coordinate / row of the cell
        :param y: int, y coordinate / column of the cell
        :return: int, the number of neighbors
        """

        number_of_neighbors = 0

        try:
            if x == 0 or y == 0:
                raise IndexError

            if self.board[x - 1][y - 1] == "X":
                number_of_neighbors += 1
        except IndexError:
            pass

        try:
            if x == 0:
                raise IndexError

            if self.board[x - 1][y] == "X":
                number_of_neighbors += 1
        except IndexError:
            pass

        try:
            if x == 0 or y == 7:
                raise IndexError

            if self.board[x - 1][y + 1] == "X":
                number_of_neighbors += 1
        except IndexError:
            pass

        try:
            if y == 7:
                raise IndexError

            if self.board[x][y + 1] == "X":
                number_of_neighbors += 1
        except IndexError:
            pass

        try:
            if x == 7 or y == 7:
                raise IndexError

            if self.board[x + 1][y + 1] == "X":
                number_of_neighbors += 1
        except IndexError:
            pass

        try:
            if x == 7:
                raise IndexError

            if self.board[x + 1][y] == "X":
                number_of_neighbors += 1
        except IndexError:
            pass

        try:
            if x == 7 or y == 0:
                raise IndexError

            if self.board[x + 1][y - 1] == "X":
                number_of_neighbors += 1
        except IndexError:
            pass

        try:
            if y == 0:
                raise IndexError

            if self.board[x][y - 1] == "X":
                number_of_neighbors += 1
        except IndexError:
            pass

        return number_of_neighbors

    def __str__(self) -> str:
        table = Texttable()
        for row in self.board:
            table.add_row(row)

        return table.draw()
