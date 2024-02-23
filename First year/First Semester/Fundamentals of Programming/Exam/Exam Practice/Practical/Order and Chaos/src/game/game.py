from src.board.board import Board
from src.players.computer import Computer
from src.players.player import Player
from src.validators.move_validator import MoveValidator


class Game:

    def __init__(self, board: Board, player_1: Player, player_2: Player):
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2

        self.next_move_owner = player_1
        self.last_move = None

        self.order_win = False
        self.chaos_win = False

    def next_move(self, move: tuple[int, int, str]) -> str:
        if type(self.next_move_owner) == Computer:
            move = self.next_move_owner.move(self.board)

        MoveValidator.validate_move(self.board, move)
        self.make_move(move)

        if self.next_move_owner == self.player_1:
            self.next_move_owner = self.player_2
        elif self.next_move_owner == self.player_2:
            self.next_move_owner = self.player_1

        outcome = self.verify_game_state()
        return outcome

    def make_move(self, move: tuple[int, int, str]):
        row, column, symbol = move

        cell = self.board.get_cell((row, column))
        cell.symbol = symbol
        self.last_move = move

    def verify_game_state(self) -> str:
        # CHECK FOR ORDER WIN
        row, column, symbol = self.last_move

        # check row
        symbols_one_after_another = 0
        for column_of_row in range(self.board.size):
            cell = self.board.get_cell((row, column_of_row))

            if cell.symbol == symbol:
                symbols_one_after_another += 1
                if symbols_one_after_another == self.board.win_size:
                    self.order_win = True
                    return "GAME OVER"

            else:
                symbols_one_after_another = 0

        # check column
        symbols_one_after_another = 0
        for row_of_column in range(self.board.size):
            cell = self.board.get_cell((row_of_column, column))

            if cell.symbol == symbol:
                symbols_one_after_another += 1
                if symbols_one_after_another == self.board.win_size:
                    self.order_win = True
                    return "GAME OVER"

            else:
                symbols_one_after_another = 0

        # check main diagonal
        symbols_one_after_another = 0

        main_diagonal_row, main_diagonal_column = row, column
        while main_diagonal_row > 0 and main_diagonal_column:
            main_diagonal_row -= 1
            main_diagonal_column -= 1

        while main_diagonal_row in range(self.board.size) and \
                main_diagonal_column in range(self.board.size):

            cell = self.board.get_cell((main_diagonal_row, main_diagonal_column))

            if cell.symbol == symbol:
                symbols_one_after_another += 1
                if symbols_one_after_another == self.board.win_size:
                    self.order_win = True
                    return "GAME OVER"

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

        while secondary_diagonal_row in range(self.board.size) and secondary_diagonal_column in range(self.board.size):

            cell = self.board.get_cell((secondary_diagonal_row, secondary_diagonal_column))

            if cell.symbol == symbol:
                symbols_one_after_another += 1
                if symbols_one_after_another == self.board.win_size:
                    self.order_win = True
                    return "GAME OVER"

            else:
                symbols_one_after_another = 0

            secondary_diagonal_row += 1
            secondary_diagonal_column -= 1

        # CHECK FOR CHAOS WIN
        if self.verify_chaos_win():
            self.chaos_win = True
            return "GAME OVER"

        return "CONTINUE"

    def verify_chaos_win(self) -> bool:
        """
        This function checks if the board is full.
        If so, chaos won and returns True
        :return: bool, True if the board is full
                       False if the board is not full
        """

        all_cells = self.board.get_all_cells()

        for cell in all_cells:
            if not cell.occupied:
                break
        else:
            return True

        return False

    def get_board_str(self) -> str:
        return self.board.get_str()
