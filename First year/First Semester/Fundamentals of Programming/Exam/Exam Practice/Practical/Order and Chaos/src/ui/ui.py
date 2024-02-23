from src.exceptions.exceptions import MoveError
from src.game.game import Game
from src.players.human import Human


class Ui:

    def __init__(self, game: Game):
        self.game = game

    def run_ui(self):
        while True:
            self.print_board()

            move = None
            if type(self.game.next_move_owner) == Human:
                move = Ui.get_move()

            outcome = "CONTINUE"
            try:
                outcome = self.game.next_move(move)

            except ValueError:
                print("\nInvalid input")
            except MoveError as errors:
                print(f"\n{errors}")

            if outcome == "GAME OVER":
                self.game_over()

    @staticmethod
    def get_move() -> tuple[int, int, str]:
        move = int(input("\nRow: ")) - 1, int(input("Column: ")) - 1, input("Symbol: ").upper()
        return move

    def game_over(self):
        if self.game.order_win:
            print("\nGAME OVER! ORDER WON")
        elif self.game.chaos_win:
            print("\nGAME OVER! CHAOS WIN")

        self.print_board()

        exit(1)

    def print_board(self):
        print(f"\n{self.game.get_board_str()}")
