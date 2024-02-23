import unittest

from src.board.board import Board
from src.game.game import Game
from src.players.human import Human


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board(1, 2)  # impossible for order to win on such conditions
        player_1 = Human()
        player_2 = Human()
        self.game = Game(self.board, player_1, player_2)

    def test_verify_chaos_win(self):
        self.game.make_move((0, 0, "X"))
        self.assertEqual(self.game.verify_chaos_win(), True)
