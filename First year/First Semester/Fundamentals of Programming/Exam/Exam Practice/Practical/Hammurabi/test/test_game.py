import unittest

from src.game import Game


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Game()

    def test_advance_year(self):
        self.assertEqual(1, self.game.year)
        self.game.advance_year(0, 2000, 800)
        self.assertEqual(2, self.game.year)
