import unittest

from src.board import Board


class TestBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board()

    def test_get_number_of_neighbors(self):
        self.board.board[0][1] = "X"
        self.assertEqual(self.board.get_number_of_neighbors(0, 0), 1)
