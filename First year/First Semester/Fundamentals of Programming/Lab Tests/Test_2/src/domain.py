class Player:
    def __init__(self, _id, name, playing_strength):
        self.id = _id
        self.name = name
        self.playing_strength = playing_strength

    def __str__(self):
        return f"Player with {self.id} named {self.name} has a playing strength of {self.playing_strength}"

