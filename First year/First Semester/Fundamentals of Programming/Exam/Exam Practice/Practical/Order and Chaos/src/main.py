from src.board.board import Board
from src.game.game import Game
from src.players.computer import Computer
from src.players.human import Human
from src.strategy.order_strategy import OrderStrategy
from src.ui.ui import Ui

if __name__ == "__main__":
    board = Board()

    strategy = OrderStrategy()
    player_1 = Computer(strategy)
    # player_1 = Human()
    player_2 = Human()

    game = Game(board, player_1, player_2)
    ui = Ui(game)

    ui.run_ui()
