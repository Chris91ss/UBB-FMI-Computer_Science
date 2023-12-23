class Movie:
    def __init__(self, movie_id, title, description, genre):
        self.id = movie_id
        self.title = title
        self.description = description
        self.genre = genre

    def __str__(self):
        return f"Movie: {self.id}, {self.title}, {self.description}, {self.genre}"
