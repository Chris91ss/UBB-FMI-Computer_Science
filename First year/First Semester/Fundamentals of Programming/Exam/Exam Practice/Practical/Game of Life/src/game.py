import copy
from math import sqrt

from src.board import Board


class Game:

    def __init__(self, board: Board, patterns_path: str):
        self.board = board
        self.patterns = self.__extract_patterns(patterns_path)

    @staticmethod
    def __extract_patterns(patterns_path: str) -> dict:
        patterns = {}
        with open(patterns_path, "r") as patterns_file:
            for line in patterns_file:
                pattern_name, positions = line.split("|")

                size, indexes = positions.split(":")
                size = int(size)
                indexes = [int(index) for index in indexes.split(",")]

                all_indexes = []
                for i in range(size ** 2):
                    if i in indexes:
                        all_indexes.append(1)
                    else:
                        all_indexes.append(0)
                patterns[pattern_name] = all_indexes

        return patterns

    def print_board(self) -> str:
        return str(self.board)

    def place(self, pattern_name: str, coordinates: tuple[int, int]):
        pattern = self.patterns[pattern_name]
        x, y = coordinates

        board_copy = copy.deepcopy(self.board)
        # copy so we don't modify the board in case of an overlap

        pattern_index = 0
        for i in range(x, x + int(sqrt(len(pattern)))):
            for j in range(y, y + int(sqrt(len(pattern)))):
                if pattern[pattern_index] == 1:
                    if board_copy.board[i][j] == "X":
                        raise IndexError("live cells can not overlap")

                    board_copy.set_alive(i, j)

                pattern_index += 1

        self.board = board_copy

    def tick(self):
        """
        This function advances the board one stage.
        Kills or revives a cells based on the predetermined conditions.
        Also prints the board after each stage
        """

        board_copy = copy.deepcopy(self.board)
        # copy so we don't modify the number of neighbors during iteration

        for i in range(8):
            for j in range(8):
                number_of_neighbors = self.board.get_number_of_neighbors(i, j)

                if number_of_neighbors not in [2, 3]:
                    board_copy.set_dead(i, j)
                if number_of_neighbors == 3:
                    board_copy.set_alive(i, j)

        self.board = board_copy

    def save(self, file_path: str):
        with open(file_path, "w") as save_file:
            for i in range(8):
                for j in range(8):
                    if self.board.board[i][j] == "X":
                        save_file.write("1 ")
                    else:
                        save_file.write("0 ")

    def load(self, file_path: str):
        with open(file_path, "r") as load_file:
            line = load_file.readlines()[0]
            cells = [cell.strip() for cell in line.split(" ")]

            cells_index = 0
            for i in range(8):
                for j in range(8):
                    if cells[cells_index] == "1":
                        self.board.set_alive(i, j)
                    else:
                        self.board.set_dead(i, j)

                    cells_index += 1
