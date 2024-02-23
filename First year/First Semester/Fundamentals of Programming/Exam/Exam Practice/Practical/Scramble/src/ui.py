from src.game import Game


class Ui:

    def __init__(self, game: Game):
        self.game = game

    def run_ui(self):
        self.print_title()

        commands = {
            "exit": Ui.exit,
            "swap": self.swap,
            "undo": self.undo
        }

        while True:
            self.print_scrambled_word()

            command, args = Ui.get_command()

            try:
                outcome = commands[command](*args)

                if outcome == "GAME OVER":
                    self.game_over()

            except Exception as error:
                print("\nInvalid input:", error)

    @staticmethod
    def exit():
        print("\nGoodbye!")
        exit(1)

    def swap(self, word_1: str, letter_1: str, word_2: str, letter_2: str) -> str:
        word_1, letter_1 = int(word_1), int(letter_1)
        word_2, letter_2 = int(word_2), int(letter_2)

        outcome = self.game.swap(word_1, letter_1, word_2, letter_2)
        return outcome

    def undo(self) -> str:
        self.game.undo()

        return "CONTINUE"

    @staticmethod
    def get_command():
        command = input(">: ")

        command = [argument.strip() for argument in command.split(" ")]
        try:
            command.remove("-")
        except ValueError:
            pass

        return command[0], command[1:]

    @staticmethod
    def print_title():
        print()
        print("# ---------------------------- #")
        print("# --------- Scramble --------- #")
        print("# ---------------------------- #")

    def print_scrambled_word(self):
        print(f"\n{self.game.scrambled_word} [score is: {self.game.score}]")

    def game_over(self):
        self.print_scrambled_word()

        if self.game.scrambled_word == self.game.solved_word:
            print(f"\nYou won! Your score is {self.game.score}.")

        else:
            print("\nDefeat!")

        exit(1)
