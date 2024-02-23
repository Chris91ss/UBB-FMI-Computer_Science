from random import randint


class UI:
    def __init__(self, game):
        self.game = game
        self.placement_phase = True
        self.movement_phase = False
        self.player_pieces_count = 4
        self.computer_pieces_count = 4

    def run(self):
        print("Placement phase begins")
        while self.placement_phase:
            self.print_board()
            self.player_move()
            self.display_winner("X")
            self.computer_move()
            self.display_winner("O")
            if self.player_pieces_count == 0 and self.computer_pieces_count == 0:
                self.placement_phase = False
                self.movement_phase = True
                print("Placement phase over")
                print("Movement phase begins")
        while self.movement_phase:
            self.print_board()
            self.movement_phase_player()
            self.display_winner("X")
            self.print_board()
            self.movement_phase_computer()
            self.display_winner("O")

    def print_board(self):
        print(self.game.print_board())

    def movement_phase_player(self):
        was_moved = False
        while not was_moved:
            row = int(input("Enter row: "))
            col = int(input("Enter col: "))
            was_moved = self.game.movement_phase(row, col, "X")
        self.player_pieces_count += 1
        self.player_move()

    def movement_phase_computer(self):
        was_moved = False
        while not was_moved:
            row = randint(0, 2)
            col = randint(0, 2)
            was_moved = self.game.movement_phase(row, col, "O")
        self.computer_pieces_count += 1
        self.computer_move()

    def player_move(self):
        was_placed = False
        while not was_placed:
            row = int(input("Enter row: "))
            col = int(input("Enter col: "))
            was_placed = self.game.move(row, col, "X")
        self.player_pieces_count -= 1

    def computer_move(self):
        was_placed = False
        while not was_placed:
            row = randint(0, 2)
            col = randint(0, 2)
            was_placed = self.game.move(row, col, "O")
        self.computer_pieces_count -= 1

    def check_for_win(self, symbol):
        return self.game.check_for_win(symbol)

    def display_winner(self, symbol):
        if self.check_for_win(symbol):
            self.print_board()
            print("Game over")
            print("Winner is: " + symbol)
            exit(0)


