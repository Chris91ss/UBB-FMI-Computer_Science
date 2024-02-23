from src.UI import UI
from src.game import Game
from src.board import Board

board = Board()
game = Game(board)
ui = UI(game)
ui.run()
