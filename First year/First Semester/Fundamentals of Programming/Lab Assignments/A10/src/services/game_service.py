from src.repository.board_repository import BoardRepository
from src.domain.board import Board
from src.domain.player import Player
from src.domain.computer_player import ComputerPlayer


class GameService:
    def __init__(self, size):
        self.board_repository = BoardRepository()
        self.board = Board(size)
        self.player = None
        self.computer_player = ComputerPlayer()
        self.last_move_performed_by = None

    def start_game(self):
        self.player = Player("Player", "X")
        self.board_repository.save_board(self.board)

    def make_move(self, row, col):
        self.last_move_performed_by = "Player"
        if self.board.is_empty(row, col):
            self.board.place_piece(row, col, self.player.piece)
            return True
        return False

    def make_computer_move(self):
        self.last_move_performed_by = "Computer"
        move = self.computer_player.get_move(self.board)
        if move:
            self.board.place_piece(*move, self.computer_player.piece)

    def is_game_over(self):
        if self.check_winner():
            if self.last_move_performed_by == "Player":
                print(f"{self.player.name} wins!")
            elif self.last_move_performed_by == "Computer":
                print(f"{self.computer_player.name} wins!")
            return True
        elif self.check_tie():
            print("It's a tie!")
            return True
        return False

    def check_winner(self):
        for i in range(len(self.board.grid)):
            for j in range(len(self.board.grid[i])):
                piece = self.board.grid[i][j]
                if piece != '-':
                    if (self.check_line(i, j, piece, 0, 1) or  # Horizontal
                            self.check_line(i, j, piece, 1, 0) or  # Vertical
                            self.check_line(i, j, piece, 1, 1) or  # Diagonal \
                            self.check_line(i, j, piece, 1, -1)):  # Diagonal /
                        return True
        return False

    def check_line(self, row, col, piece, row_increment, col_increment):
        count = 0
        for _ in range(5):
            if not (0 <= row < len(self.board.grid) and 0 <= col < len(self.board.grid[row])):
                break
            if self.board.grid[row][col] == piece:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0  # Reset the count if the sequence is interrupted
            row += row_increment
            col += col_increment
        return False

    def check_tie(self):
        return all(not self.board.is_empty(i, j) for i in range(len(self.board.grid)) for j in range(len(self.board.grid[i])))
