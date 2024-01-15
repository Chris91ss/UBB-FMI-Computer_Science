from src.services.game_service import GameService


class UI:
    def __init__(self, size):
        self.game_service = GameService(size)

    def run(self):
        self.game_service.start_game()

        while not self.is_game_over():
            self.display_board()
            while not self.get_and_make_move(): continue
            self.game_service.make_computer_move()

        self.display_board()
        self.display_game_result()

    def display_board(self):
        self.game_service.board.display()

    def get_and_make_move(self):
        try:
            row = int(input("Enter row (0-indexed): "))
            col = int(input("Enter column (0-indexed): "))
        except Exception as exception:
            print(exception)
            print("Invalid input. Try again.")
            return False

        try:
            while not self.game_service.make_move(row, col):
                try:
                    row = int(input("Enter row (0-indexed): "))
                    col = int(input("Enter column (0-indexed): "))
                except Exception as exception:
                    print(exception)
                    print("Invalid input. Try again.")
                    return False
        except Exception as exception:
            print(exception)
            print("Invalid input. Try again.")
            return False

        return True

    def is_game_over(self):
        return self.game_service.is_game_over()

    def display_game_result(self):
        if self.game_service.check_winner():
            if self.game_service.last_move_performed_by == "Player":
                print(f"{self.game_service.player.name} wins!")
            elif self.game_service.last_move_performed_by == "Computer":
                print(f"{self.game_service.computer_player.name} wins!")
        elif self.game_service.check_tie():
            print("It's a tie!")
