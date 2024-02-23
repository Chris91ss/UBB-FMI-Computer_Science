import unittest

from src.board import Board
from src.game import Game


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        patterns_path = "data/patterns.txt"

        board = Board()
        self.game = Game(board, patterns_path)
        new_board = Board()
        self.new_game = Game(new_board, patterns_path)

    def test_tick(self):
        self.new_game.place("block", (0, 0))
        self.game.place("block", (0, 0))
        self.game.tick()
        self.assertEqual(self.game.print_board(), self.new_game.print_board())
