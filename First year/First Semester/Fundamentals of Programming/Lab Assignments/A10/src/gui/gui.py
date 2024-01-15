import tkinter as tk
from src.services.game_service import GameService


class GomokuGUI:
    def __init__(self, size):
        self.root = tk.Tk()
        self.root.title("Gomoku Game")

        self.game_service = GameService(size)
        self.buttons = [[0 for _ in range(size)] for _ in range(size)]
        self.game_over = False

        self.create_board_buttons()
        self.start_game()

    def create_board_buttons(self):
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                button = tk.Button(self.root, text="", width=6, height=3, font=('Helvetica', 12, 'bold'),
                                   command=lambda row=i, col=j: self.make_move(row, col), relief=tk.GROOVE)
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = button

    def start_game(self):
        self.game_service.start_game()

    def make_move(self, row, col):
        if not self.game_over:
            if not self.game_service.make_move(row, col):
                print("Invalid move. Try again.")
            else:
                self.update_board()
                if not self.is_game_over():
                    self.game_service.make_computer_move()
                    self.update_board()
                    self.is_game_over()

    def update_board(self):
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                value = self.game_service.board.grid[i][j]
                text = str(value) if value != '-' else ""

                # Set color based on move type
                if value == self.game_service.player.piece:
                    self.buttons[i][j].configure(bg='green', fg='white')
                elif value == self.game_service.computer_player.piece:
                    self.buttons[i][j].configure(bg='red', fg='white')
                else:
                    self.buttons[i][j].configure(bg='SystemButtonFace', fg='black')

                self.buttons[i][j]["text"] = text

    def is_game_over(self):
        if self.game_service.is_game_over():
            self.display_game_result()
            self.game_over = True
            return True
        return False

    def display_game_result(self):
        result = ""
        font = 0
        color = 0
        if self.game_service.check_winner():
            if self.game_service.last_move_performed_by == "Player":
                result = f"{self.game_service.player.name} wins!"
                color = 'green'
            elif self.game_service.last_move_performed_by == "Computer":
                result = f"{self.game_service.computer_player.name} wins!"
                color = 'red'
            font = ('Helvetica', 14, 'bold')
        elif self.game_service.check_tie():
            result = "It's a tie!"
            font = ('Helvetica', 14, 'bold')
            color = 'black'

        result_label = tk.Label(self.root, text=result, font=font, fg=color)
        result_label.grid(row=len(self.buttons), columnspan=len(self.buttons[0]), pady=10)

    def run(self):
        self.root.mainloop()
