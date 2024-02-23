from src.game import Game
from src.ui import Ui

if __name__ == "__main__":
    game = Game()
    ui = Ui(game)
    ui.run_ui()
