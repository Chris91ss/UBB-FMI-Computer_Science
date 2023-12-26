from src.domain.movie import Movie
from src.repository.repositoryException import RepositoryException
from random import randint


class MovieServices:
    def __init__(self, provide_movie_repository):
        self._repository = provide_movie_repository
        self.generate_random_movies()

    def generate_random_movies(self):
        movie_list = ["The Lord of the Rings: The Return of the King", "The Godfather", "The Dark Knight", "Fast & Furious 7",
                      "The Redemption", "Pulp Fiction", "Schindler's List",
                      "The Godfather: Part II", "The Lord of the Rings: The Fellowship of the Ring", "Fight Club",
                      "Forrest Gump", "Inception", "The Lord of the Rings: The Two Towers", "The Matrix",
                      "Good-fellas", "Star Wars: Episode V - The Empire Strikes Back", "One Flew Over the Cuckoo's Nest",
                      "Seven Samurai", "Se7en", "Life Is Beautiful"]
        description_list = ["Find the ring", "It focuses on the transformation of his youngest son",
                            "Batman, Gordon and Harvey Dent are forced to deal with the chaos unleashed by an anarchist mastermind known only as"
                            " the Joker", "Deck-ard Shaw seeks revenge against Dominic Tore-tto and his family for his comatose brother"]
        genre_list = ["Action", "Adventure", "Comedy", "Crime", "Drama", "Fantasy", "Historical", "Historical fiction"]

        number_of_movies = 20
        for i in range(number_of_movies):
            random_number = randint(251, 500)
            movie = Movie(random_number, movie_list[i],
                          description_list[randint(0, len(description_list) - 1)],
                          genre_list[randint(0, len(genre_list) - 1)])
            self.add_movie(movie.id, movie.title, movie.description, movie.genre)

    def add_movie(self, movie_id, movie_title, movie_description, movie_genre):
        movie = Movie(movie_id, movie_title, movie_description, movie_genre)
        try:
            self._repository.add(movie)
        except RepositoryException as ex:
            print(ex)

    def remove_movie(self, movie_id):
        try:
            self._repository.remove(movie_id)
        except RepositoryException as ex:
            print(ex)

    def update_movie(self, movie_id, movie_title, movie_description, movie_genre):
        movie = Movie(movie_id, movie_title, movie_description, movie_genre)
        self._repository.update(movie)

    def undo(self):
        try:
            self._repository.undo()
        except RepositoryException as re:
            print(re)

    def redo(self):
        try:
            self._repository.redo()
        except RepositoryException as re:
            print(re)

    def get_all_movies(self):
        return self._repository.get_all()

    def clear_stacks(self):
        self._repository.clear_stacks()

    def search_movie_by_id(self, movie_id):
        return self._repository.search_by_id(movie_id)

    def search_movie_by_title(self, movie_title):
        return self._repository.search_by_title(movie_title)

    def search_movie_by_description(self, movie_description):
        return self._repository.search_by_description(movie_description)

    def search_movie_by_genre(self, movie_genre):
        return self._repository.search_by_genre(movie_genre)
