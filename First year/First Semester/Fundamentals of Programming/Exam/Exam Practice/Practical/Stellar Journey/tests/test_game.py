import unittest

from src.board.board import Board
from src.coordinates_converter import CoordinatesConverter
from src.game import Game


class TestGame(unittest.TestCase):

    def test_place_stars_randomly(self):
        coordinates_converter = CoordinatesConverter()
        board = Board(coordinates_converter)

        new_board = Board(coordinates_converter)
        game = Game(new_board, coordinates_converter)

        number_of_board_stars = 0
        for cell in board.cells.values():
            if cell.resident == "star":
                number_of_board_stars += 1

        number_of_new_board_stars = 0
        for cell in new_board.cells.values():
            if cell.resident == "star":
                number_of_new_board_stars += 1

        self.assertEqual(number_of_board_stars, 0)
        self.assertEqual(number_of_new_board_stars, 10)
