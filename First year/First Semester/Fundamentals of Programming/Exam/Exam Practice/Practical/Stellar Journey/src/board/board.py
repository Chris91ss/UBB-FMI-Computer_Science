from texttable import Texttable

from src.board.cell import Cell
from src.coordinates_converter import CoordinatesConverter


class Board:

    STAR = "*"
    ENDEAVOUR = "E"
    BLINGON = "B"
    EMPTY = " "

    def __init__(self, coordinates_converter: CoordinatesConverter):
        self.cells = {}
        self.__create_cells()

        self.converter = coordinates_converter

    def __create_cells(self):
        for row in range(1, 9):
            for column in range(1, 9):
                cell = Cell(row, column)
                self.cells[(row, column)] = cell

    def get_cell(self, row: int, column: int) -> Cell:
        return self.cells[(row, column)]

    def get_number_of_neighbors(self, row: int, column: int) -> int:
        number_of_neighbors = 0

        try:
            cell = self.cells[row - 1, column - 1]
            if cell.occupied:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = self.cells[row - 1, column]
            if cell.occupied:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = self.cells[row - 1, column + 1]
            if cell.occupied:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = self.cells[row, column + 1]
            if cell.occupied:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = self.cells[row + 1, column + 1]
            if cell.occupied:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = self.cells[row + 1, column]
            if cell.occupied:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = self.cells[row + 1, column - 1]
            if cell.occupied:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = self.cells[row, column - 1]
            if cell.occupied:
                number_of_neighbors += 1
        except KeyError:
            pass

        return number_of_neighbors

    def get_str(self, cheat: bool) -> str:
        table = Texttable()
        table.header([" "] + [str(i) for i in range(1, 9)])

        for row in range(1, 9):
            str_row = []
            for column in range(1, 9):
                cell = self.cells[(row, column)]

                if cell.occupied:
                    if cell.resident == "blingon":
                        if cheat or cell.near_endeavour:
                            str_row += [Board.BLINGON]
                        else:
                            str_row += [Board.EMPTY]

                    elif cell.resident == "endeavour":
                        str_row += [Board.ENDEAVOUR]

                    elif cell.resident == "star":
                        str_row += [Board.STAR]

                else:
                    str_row += [Board.EMPTY]

            table.add_row([self.converter.int_to_str(row)] + str_row)

        return table.draw()
