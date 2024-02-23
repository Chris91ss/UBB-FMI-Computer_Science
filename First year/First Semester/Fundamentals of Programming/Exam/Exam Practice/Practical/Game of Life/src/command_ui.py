from time import sleep

from src.game import Game


class CommandUi:

    def __init__(self, game: Game):
        self.game = game

    def run_ui(self):
        CommandUi.print_title()

        commands = {
            "exit": CommandUi.exit,
            "place": self.place,
            "tick": self.tick,
            "save": self.save,
            "load": self.load,
        }

        while True:
            self.print_board()
            command, args = CommandUi.get_command()

            try:
                commands[command](args)

            except Exception as error:
                print("Invalid command:", error)

    @staticmethod
    def exit(args):
        print("Goodbye!")
        exit(0)

    def place(self, args):
        pattern_name = args[0]
        x, y = args[1].split(",")
        coordinates = int(x), int(y)

        self.game.place(pattern_name, coordinates)

    def tick(self, args):
        """
        This function advances the board one stage.
        Kills or revives a cells based on the predetermined conditions.
        Also prints the board after each stage
        :param args: list[int], a list that contains only one integer, the number of times the function will run
        """

        if args:
            number_of_times = int(args[0])
        else:
            number_of_times = 1

        for i in range(number_of_times):
            self.game.tick()
            if i != number_of_times - 1:
                self.print_board()
                sleep(1)

    def save(self, args):
        file_name = args[0]
        file_path = f"data/{file_name}.txt"

        self.game.save(file_path)

    def load(self, args):
        file_name = args[0]
        file_path = f"data/{file_name}.txt"

        self.game.load(file_path)

    @staticmethod
    def get_command() -> tuple[str, list[str]]:
        command = input(">: ")

        command = command.split(" ")
        for arg in command:
            arg.strip()

        return command[0], command[1:]

    @staticmethod
    def print_title():
        print()
        print("# ------------------------------ #")
        print("# -------- Game of Life -------- #")
        print("# ------------------------------ #")

    def print_board(self):
        print(f"\n{self.game.print_board()}\n")
