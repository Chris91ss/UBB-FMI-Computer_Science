from src.board.board import Board
from src.exceptions.exceptions import MoveError


class MoveValidator:

    @staticmethod
    def validate_move(board: Board, move: tuple[int, int, str]):
        row, column, symbol = move
        errors = []

        if symbol not in ["O", "X"]:
            errors.append("Symbol must be either X or O.")

        if row not in range(board.size) or column not in range(board.size):
            errors.append("Can not make move outside the board.")

        cell = board.get_cell((row, column))
        if cell.occupied:
            errors.append("Overlapping move.")

        if errors:
            raise MoveError(errors)
