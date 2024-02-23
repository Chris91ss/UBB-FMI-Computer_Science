from src.board import Board
from src.game import Game
from src.command_ui import CommandUi

if __name__ == "__main__":
    patterns_path = "data/patterns.txt"

    board = Board()
    game = Game(board, patterns_path)
    ui = CommandUi(game)

    ui.run_ui()
