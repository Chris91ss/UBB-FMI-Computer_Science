from src.game import Game


class Ui:

    def __init__(self, game: Game):
        self.game = game

    def run_ui(self):
        Ui.print_title()

        commands = {
            "warp": self.warp,
            "fire": self.fire,
            "cheat": self.cheat,
            "exit": Ui.exit
        }

        self.print_board()
        while True:
            command, args = Ui.get_command()

            try:
                commands[command](*args)
            except Exception as error:
                print("Invalid input:", error, "\n")

    def warp(self, coordinates: str):
        outcome = self.game.warp(coordinates)

        if outcome == "GAME OVER":
            print("Game is over! You lost by warping on a blingon ship.")
            self.exit()

        self.print_board()

    def fire(self, coordinates: str):
        outcome = self.game.fire(coordinates)

        if outcome == "GAME OVER":
            print("Game is over! You won by shooting all the blingon ships.")
            self.exit()

        self.print_board()

    def cheat(self):
        self.print_board(True)

    @staticmethod
    def exit():
        print("Goodbye!")
        exit(0)

    @staticmethod
    def get_command():
        command = input(">: ")
        command = [word.strip() for word in command.split(" ")]

        return command[0], command[1:]

    @staticmethod
    def print_title():
        print()
        print("# ------------------------------------- #")
        print("# ---------- Stellar Journey ---------- #")
        print("# ------------------------------------- #")

    def print_board(self, cheat: bool = False):
        print(f"\n{self.game.get_board_str(cheat)}\n")
