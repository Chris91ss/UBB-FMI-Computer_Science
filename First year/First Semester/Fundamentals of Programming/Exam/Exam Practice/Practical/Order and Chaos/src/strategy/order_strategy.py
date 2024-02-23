import copy

from src.board.board import Board
from src.strategy.strategy import Strategy


class OrderStrategy(Strategy):

    def get_next_move(self, board: Board) -> tuple[int, int, str]:
        # try to find a winning move
        for row in range(board.size):
            for column in range(board.size):
                for symbol in ["X", "O"]:
                    board_copy = copy.deepcopy(board)
                    cell = board_copy.get_cell((row, column))
                    cell.symbol = symbol

                    if OrderStrategy.is_wining_move(board_copy, row, column, symbol):
                        return row, column, symbol

        # determine most common symbol
        number_of_x = 0
        number_of_o = 0

        all_cells = board.get_all_cells()
        for cell in all_cells:
            if cell.symbol == "X":
                number_of_x += 1
            if cell.symbol == "O":
                number_of_o += 1

        # first move of the game
        if number_of_x == number_of_o == 0:
            return 0, 0, "X"

        chosen_symbol = "X"
        if number_of_o > number_of_x:
            chosen_symbol = "O"

        chosen_row_column = None
        max_number_of_neighbors = 0
        for row in range(board.size):
            for column in range(board.size):
                current_cell = board.get_cell((row, column))
                if not current_cell.occupied:
                    current_number_of_neighbors = OrderStrategy.get_number_of_neighbors(board, row, column,
                                                                                        chosen_symbol)

                    if current_number_of_neighbors > max_number_of_neighbors:
                        chosen_row_column = row, column
                        max_number_of_neighbors = current_number_of_neighbors

        row, column = chosen_row_column
        return row, column, chosen_symbol

    @staticmethod
    def get_number_of_neighbors(board: Board, row: int, column: int, symbol: str) -> int:
        number_of_neighbors = 0

        try:
            cell = board.get_cell((row - 1, column - 1))
            if cell.symbol == symbol:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = board.get_cell((row - 1, column))
            if cell.symbol == symbol:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = board.get_cell((row - 1, column + 1))
            if cell.symbol == symbol:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = board.get_cell((row, column + 1))
            if cell.symbol == symbol:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = board.get_cell((row + 1, column + 1))
            if cell.symbol == symbol:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = board.get_cell((row + 1, column))
            if cell.symbol == symbol:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = board.get_cell((row + 1, column - 1))
            if cell.symbol == symbol:
                number_of_neighbors += 1
        except KeyError:
            pass

        try:
            cell = board.get_cell((row, column - 1))
            if cell.symbol == symbol:
                number_of_neighbors += 1
        except KeyError:
            pass

        return number_of_neighbors

    @staticmethod
    def is_wining_move(board: Board, row: int, column: int, symbol: str) -> bool:
        # check row
        symbols_one_after_another = 0
        for column_of_row in range(board.size):
            cell = board.get_cell((row, column_of_row))

            if cell.symbol == symbol:
                symbols_one_after_another += 1
                if symbols_one_after_another == board.win_size:
                    return True

            else:
                symbols_one_after_another = 0

        # check column
        symbols_one_after_another = 0
        for row_of_column in range(board.size):
            cell = board.get_cell((row_of_column, column))

            if cell.symbol == symbol:
                symbols_one_after_another += 1
                if symbols_one_after_another == board.win_size:
                    return True

            else:
                symbols_one_after_another = 0

        # check main diagonal
        symbols_one_after_another = 0

        main_diagonal_row, main_diagonal_column = row, column
        while main_diagonal_row > 0 and main_diagonal_column:
            main_diagonal_row -= 1
            main_diagonal_column -= 1

        while main_diagonal_row in range(board.size) and \
                main_diagonal_column in range(board.size):

            cell = board.get_cell((main_diagonal_row, main_diagonal_column))

            if cell.symbol == symbol:
                symbols_one_after_another += 1
                if symbols_one_after_another == board.win_size:
                    return True

            else:
                symbols_one_after_another = 0

            main_diagonal_row += 1
            main_diagonal_column += 1

        # check secondary diagonal
        symbols_one_after_another = 0

        secondary_diagonal_row, secondary_diagonal_column = row, column
        while secondary_diagonal_row > 0 and main_diagonal_column:
            secondary_diagonal_row -= 1
            secondary_diagonal_column += 1

        while secondary_diagonal_row in range(board.size) and secondary_diagonal_column in range(board.size):

            cell = board.get_cell((secondary_diagonal_row, secondary_diagonal_column))

            if cell.symbol == symbol:
                symbols_one_after_another += 1
                if symbols_one_after_another == board.win_size:
                    return True

            else:
                symbols_one_after_another = 0

            secondary_diagonal_row += 1
            secondary_diagonal_column -= 1

        return False
