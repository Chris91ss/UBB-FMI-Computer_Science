import random

from src.board.board import Board
from src.coordinates_converter import CoordinatesConverter
from src.exceptions import CoordinatesError


class Game:

    def __init__(self, board: Board, coordinate_converter: CoordinatesConverter):
        self.board = board
        self.converter = coordinate_converter
        self.endeavour_location = 0, 0

        self.number_of_blingons = 3
        self.number_of_stars = 10

        self.place_starts_randomly()
        self.place_endeavour_randomly()
        self.place_blingons_randomly()

    def get_board_str(self, cheat: bool) -> str:
        return self.board.get_str(cheat)

    def place_starts_randomly(self):
        """
        This function places the stars randomly
        """

        number_of_starts = self.number_of_stars

        while number_of_starts > 0:
            row = random.randint(1, 8)
            column = random.randint(1, 8)

            cell = self.board.get_cell(row, column)
            if cell.occupied or self.board.get_number_of_neighbors(row, column) > 0:
                continue

            cell.occupy("star")
            number_of_starts -= 1

    def place_blingons_randomly(self):
        # deoccupy all cells with blingons
        for i in range(1, 9):
            for j in range(1, 9):
                cell = self.board.get_cell(i, j)
                if cell.resident == "blingon":
                    cell.deoccupy()

        number_of_blingons = self.number_of_blingons

        while number_of_blingons > 0:
            row = random.randint(1, 8)
            column = random.randint(1, 8)

            cell = self.board.get_cell(row, column)
            if cell.occupied:
                continue

            cell.occupy("blingon")
            number_of_blingons -= 1

    def place_endeavour_randomly(self):
        while True:
            row = random.randint(1, 8)
            column = random.randint(1, 8)

            cell = self.board.get_cell(row, column)
            if cell.occupied:
                continue

            self.place_endeavour(row, column)
            break

    def place_endeavour(self, row: int, column: int):
        old_row, old_column = self.endeavour_location
        if (old_row, old_column) != (0, 0):  # initial value
            old_cell = self.board.get_cell(old_row, old_column)
            old_cell.deoccupy()

        # notify the neighbors that they are no longer near Endeavour
        try:
            cell = self.board.get_cell(old_row - 1, old_column - 1)
            cell.near_endeavour = False
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(old_row - 1, old_column)
            cell.near_endeavour = False
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(old_row - 1, old_column + 1)
            cell.near_endeavour = False
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(old_row, old_column + 1)
            cell.near_endeavour = False
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(old_row + 1, old_column + 1)
            cell.near_endeavour = False
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(old_row + 1, old_column)
            cell.near_endeavour = False
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(old_row + 1, old_column - 1)
            cell.near_endeavour = False
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(old_row, old_column - 1)
            cell.near_endeavour = False
        except KeyError:
            pass

        new_cell = self.board.get_cell(row, column)
        new_cell.occupy("endeavour")
        self.endeavour_location = row, column

        # notify the neighbors that they are near Endeavour
        try:
            cell = self.board.get_cell(row - 1, column - 1)
            cell.near_endeavour = True
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(row - 1, column)
            cell.near_endeavour = True
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(row - 1, column + 1)
            cell.near_endeavour = True
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(row, column + 1)
            cell.near_endeavour = True
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(row + 1, column + 1)
            cell.near_endeavour = True
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(row + 1, column)
            cell.near_endeavour = True
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(row + 1, column - 1)
            cell.near_endeavour = True
        except KeyError:
            pass

        try:
            cell = self.board.get_cell(row, column - 1)
            cell.near_endeavour = True
        except KeyError:
            pass

    def warp(self, coordinates: str) -> str:
        row, column = self.converter.str_to_tuple(coordinates)

        if row != self.endeavour_location[0] and column != self.endeavour_location[1]:
            diagonal_coordinates = []

            row_copy, column_copy = self.endeavour_location
            for i in range(min(row_copy - 1, column_copy - 1)):
                row_copy, column_copy = row_copy - 1, column_copy - 1
                diagonal_coordinates.append((row_copy, column_copy))

            row_copy, column_copy = self.endeavour_location
            for i in range(min(row_copy - 1, 8 - column_copy)):
                row_copy, column_copy = row_copy - 1, column_copy + 1
                diagonal_coordinates.append((row_copy, column_copy))

            row_copy, column_copy = self.endeavour_location
            for i in range(min(8 - row_copy, 8 - column_copy)):
                row_copy, column_copy = row_copy + 1, column_copy + 1
                diagonal_coordinates.append((row_copy, column_copy))

            row_copy, column_copy = self.endeavour_location
            for i in range(min(8 - row_copy, column_copy - 1)):
                row_copy, column_copy = row_copy + 1, column_copy - 1
                diagonal_coordinates.append((row_copy, column_copy))

            if (row, column) not in diagonal_coordinates:
                raise CoordinatesError("must warp on the same row, column or diagonal")

        row_step = 0
        if row < self.endeavour_location[0]:
            row_step = -1
        elif row > self.endeavour_location[0]:
            row_step = +1

        column_step = 0
        if column < self.endeavour_location[1]:
            column_step = -1
        elif column > self.endeavour_location[1]:
            column_step = +1

        endeavour_row, endeavour_column = self.endeavour_location
        while endeavour_row != row or endeavour_column != column:
            endeavour_row += row_step
            endeavour_column += column_step

            cell = self.board.get_cell(endeavour_row, endeavour_column)
            if cell.resident == "star":
                raise CoordinatesError("star is in the way")

        cell = self.board.get_cell(row, column)
        if cell.resident == "blingon":
            return "GAME OVER"

        self.place_endeavour(row, column)
        return "CONTINUE"

    def fire(self, coordinates: str) -> str:
        row, column = self.converter.str_to_tuple(coordinates)

        endeavour_neighbors = []
        row_endeavour, column_endeavour = self.endeavour_location
        endeavour_neighbors.append((row_endeavour - 1, column_endeavour - 1))
        endeavour_neighbors.append((row_endeavour - 1, column_endeavour))
        endeavour_neighbors.append((row_endeavour - 1, column_endeavour + 1))
        endeavour_neighbors.append((row_endeavour, column_endeavour + 1))
        endeavour_neighbors.append((row_endeavour + 1, column_endeavour + 1))
        endeavour_neighbors.append((row_endeavour + 1, column_endeavour))
        endeavour_neighbors.append((row_endeavour + 1, column_endeavour - 1))
        endeavour_neighbors.append((row_endeavour, column_endeavour - 1))

        if (row, column) not in endeavour_neighbors:
            raise CoordinatesError("shot is not near endeavour")

        cell = self.board.get_cell(row, column)
        if cell.resident == "blingon":
            self.number_of_blingons -= 1
            if self.number_of_blingons == 0:
                return "GAME OVER"

            self.place_blingons_randomly()
        return "CONTINUE"
