from src.controller.controller import Controller


class Ui:

    def __init__(self, controller: Controller):
        self.controller = controller

    def run_ui(self):
        options = {
            "1": self.add_sentence,
            "2": self.start_game
        }

        while True:
            Ui.print_options()

            option = Ui.get_option()

            try:
                options[option]()

            except Exception as error:
                print(error)

    def start_game(self):
        while True:
            self.print_shown_line()
            self.print_hangman()
            letter = Ui.get_letter()

            try:
                self.controller.add_letter(letter)

            except Exception as error:
                print(error)

            if self.controller.game_over:
                self.game_over()

    def game_over(self):
        if self.controller.lost:
            self.print_hangman()
            print("\nYOU LOSE")
            self.print_true_line()

        else:
            print("\nYOU WIN")

        exit(1)

    def add_sentence(self):
        new_sentence = input("\nNew sentence: ").strip()
        self.controller.add_sentence(new_sentence)

    @staticmethod
    def get_letter():
        return input("\nLetter: ").strip()

    @staticmethod
    def get_option() -> str:
        return input("\n>: ").strip()

    @staticmethod
    def print_options():
        print("\n1: Add sentence")
        print("2: Start")

    def print_shown_line(self):
        print(f"\n{self.controller.get_shown_line()}")

    def print_true_line(self):
        print(f"\n{self.controller.get_true_line()}")

    def print_hangman(self):
        print(f"{self.controller.get_hangman()}")
