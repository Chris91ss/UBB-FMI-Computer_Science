from src.board.board import Board
from src.coordinates_converter import CoordinatesConverter
from src.game import Game
from src.ui import Ui

if __name__ == "__main__":
    coordinates_converter = CoordinatesConverter()
    board = Board(coordinates_converter)
    game = Game(board, coordinates_converter)
    ui = Ui(game)

    ui.run_ui()
