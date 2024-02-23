from abc import abstractmethod

from src.board.board import Board


class Player:

    @abstractmethod
    def move(self, board: Board) -> tuple[int, int, str]:
        pass
