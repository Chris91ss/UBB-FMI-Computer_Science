from src.game import Game
from src.ui import Ui

if __name__ == "__main__":
    input_path = "data/input.txt"

    game = Game(input_path)
    ui = Ui(game)

    ui.run_ui()
