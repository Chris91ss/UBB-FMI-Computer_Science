from texttable import Texttable


class Board:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def __str__(self):
        table = Texttable()
        for row in self.board:
            table.add_row(row)
        return table.draw()

    def move(self, row, col, symbol):
        if self.board[row][col] == " ":
            self.board[row][col] = symbol
        else:
            raise ValueError("Invalid move")

    def movement_phase(self, row, col, symbol):
        if self.board[row][col] == symbol:
            self.board[row][col] = " "
            return True
        else:
            raise ValueError("Invalid move")

    def check_for_win(self, symbol):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == symbol and self.board[i][0] != " ":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == symbol and self.board[0][i] != " ":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol and self.board[0][0] != " ":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol and self.board[0][2] != " ":
            return True
        return False



