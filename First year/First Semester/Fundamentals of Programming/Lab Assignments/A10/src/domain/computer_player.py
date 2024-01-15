import random
from src.domain.player import Player


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__("Computer", "O")

    def get_move(self, board):
        # Check for winning move
        winning_move = self.find_winning_or_blocking_move(board, self.piece)
        if winning_move:
            return winning_move

        # Check for blocking opponent's winning move
        blocking_move = self.find_winning_or_blocking_move(board, 'X' if self.piece == 'O' else 'O')
        if blocking_move:
            return blocking_move

        # Try to place next to own cells for potential win
        next_to_own_cells = self.place_next_to_own_cells(board)
        if next_to_own_cells:
            return next_to_own_cells

        # If no winning, blocking, or placing next to own cells, make a strategic move
        return self.strategic_move(board)

    def place_next_to_own_cells(self, board):
        piece = self.piece

        for i in range(len(board.grid)):
            for j in range(len(board.grid[i])):
                if board.grid[i][j] == piece:
                    # Check horizontally, vertically, and diagonally for empty cells
                    for direction in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        row, col = i + direction[0], j + direction[1]
                        if 0 <= row < len(board.grid) and 0 <= col < len(board.grid[row]) and board.is_empty(row, col):
                            return row, col

        return None

    def find_winning_or_blocking_move(self, board, piece):
        for i in range(len(board.grid)):
            for j in range(len(board.grid[i])):
                if board.is_empty(i, j):
                    board.place_piece(i, j, piece)
                    if self.check_winner(board, piece):
                        board.grid[i][j] = '-'
                        return i, j
                    board.grid[i][j] = '-'

        opponent_piece = 'X' if piece == 'O' else 'O'
        for i in range(len(board.grid)):
            for j in range(len(board.grid[i])):
                if board.is_empty(i, j):
                    board.place_piece(i, j, opponent_piece)
                    if self.check_winner(board, opponent_piece):
                        board.grid[i][j] = '-'
                        return i, j
                    board.grid[i][j] = '-'

        # If no winning or blocking move found, prioritize winning moves
        for i in range(len(board.grid)):
            for j in range(len(board.grid[i])):
                if board.is_empty(i, j):
                    board.place_piece(i, j, piece)
                    if self.check_winner(board, piece):
                        board.grid[i][j] = '-'
                        return i, j
                    board.grid[i][j] = '-'

        return None

    @staticmethod
    def strategic_move(board):
        # Prioritize center move if available
        if board.is_empty(len(board.grid)//2, len(board.grid)//2):
            return len(board.grid)//2, len(board.grid)//2

        # Otherwise, choose a random available move
        empty_positions = [(i, j) for i in range(len(board.grid)) for j in range(len(board.grid[i])) if board.is_empty(i, j)]
        return random.choice(empty_positions) if empty_positions else None

    def check_winner(self, board, piece):
        # Return True if the specified piece has won, otherwise False
        return any(self.check_sequence(board, i, j, piece, 0, 1) or  # Horizontal
                   self.check_sequence(board, i, j, piece, 1, 0) or  # Vertical
                   self.check_sequence(board, i, j, piece, 1, 1) or  # Diagonal \
                   self.check_sequence(board, i, j, piece, 1, -1)    # Diagonal /
                   for i in range(len(board.grid)) for j in range(len(board.grid[i])))

    @staticmethod
    def check_sequence(board, row, col, piece, row_increment, col_increment):
        count = 0
        for _ in range(5):
            if not (0 <= row < len(board.grid) and 0 <= col < len(board.grid[row])):
                break
            if board.grid[row][col] == piece:
                count += 1
                if count == 5:
                    return True
            else:
                break
            row += row_increment
            col += col_increment
        return False
