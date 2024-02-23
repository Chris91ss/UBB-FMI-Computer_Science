from src.board import Board


class Game:
    def __init__(self, board):
        self.board = board

    def print_board(self):
        return str(self.board)

    def move(self, row, col, symbol):
        try:
            self.board.move(row, col, symbol)
            return True
        except ValueError as ve:
            print(ve)
            return False

    def movement_phase(self, row, col, symbol):
        try:
            self.board.movement_phase(row, col, symbol)
            return True
        except ValueError as ve:
            print(ve)
            return False

    def check_for_win(self, symbol):
        return self.board.check_for_win(symbol)
