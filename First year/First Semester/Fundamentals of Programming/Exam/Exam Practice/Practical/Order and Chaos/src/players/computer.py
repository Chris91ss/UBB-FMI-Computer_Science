from src.board.board import Board
from src.players.player import Player
from src.strategy.strategy import Strategy


class Computer(Player):

    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def move(self, board: Board) -> tuple[int, int, str]:
        move = self.strategy.get_next_move(board)
        return move
