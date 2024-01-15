class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['-' for _ in range(size)] for _ in range(size)]

    def is_empty(self, row, col):
        return self.grid[row][col] == '-'

    def place_piece(self, row, col, piece):
        self.grid[row][col] = piece

    def display(self):
        # Display column indices
        col_indices = "    " + "  ".join(f"\033[34m{i: 2}\033[0m" for i in range(self.size))  # Blue text
        print(col_indices)

        # Display board rows
        for i in range(self.size):
            row_values = f"\033[34m{i: 2}\033[0m | "  # Blue text for row index
            for j in range(self.size):
                if self.grid[i][j] == 'X':
                    row_values += "\033[92mX\033[0m | "  # Green for player's move
                elif self.grid[i][j] == 'O':
                    row_values += "\033[91mO\033[0m | "  # Red for computer's move
                else:
                    row_values += "- | "
            print(row_values)

        # Display board outline
        board_outline = "    " + "\033[34m" + "-" * (4 * self.size + 1) + "\033[0m"  # Blue text
        print(board_outline)
