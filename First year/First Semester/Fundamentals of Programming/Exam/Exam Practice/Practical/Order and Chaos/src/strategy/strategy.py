from abc import abstractmethod

from src.board.board import Board


class Strategy:

    @abstractmethod
    def get_next_move(self, board: Board) -> tuple[int, int, str]:
        pass
