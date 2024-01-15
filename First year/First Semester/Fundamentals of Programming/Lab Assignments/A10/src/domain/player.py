class Player:
    def __init__(self, name, piece=None):
        self.name = name
        self.piece = piece

    def get_move(self, board):
        raise NotImplementedError("Subclasses must implement get_move method.")
