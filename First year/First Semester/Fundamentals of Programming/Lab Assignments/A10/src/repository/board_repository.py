class BoardRepository:
    def __init__(self):
        self.board = None

    def save_board(self, board):
        self.board = board
