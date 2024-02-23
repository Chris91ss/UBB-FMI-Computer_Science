from texttable import Texttable

from src.board.cell import Cell


class Board:

    def __init__(self, size: int = 6, win_size: int = 5):
        self.size = size
        self.win_size = win_size
        self.cells = Board.create_cells(size)

    @staticmethod
    def create_cells(size: int) -> dict[(int, int), Cell]:
        all_cells = {}

        for row in range(size):
            for column in range(size):
                cell = Cell(row, column)
                all_cells[(row, column)] = cell

        return all_cells

    def get_cell(self, coordinates: tuple[int, int]) -> Cell:
        return self.cells[coordinates]

    def get_all_cells(self) -> list[Cell]:
        return list(self.cells.values())

    def get_str(self) -> str:
        table = Texttable()

        for row in range(self.size):
            table_row = []
            for column in range(self.size):
                table_row += self.cells[row, column].symbol

            table.add_row(table_row)

        return table.draw()
