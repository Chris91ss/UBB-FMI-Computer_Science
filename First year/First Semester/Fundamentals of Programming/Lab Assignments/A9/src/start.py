from src.ui.ui import UI
from src.repository.repository import Repository
from src.repository.textFileRepository import TextFileRepository
from src.repository.binaryRepository import BinaryRepository
from src.repository.repositoryException import RepositoryException


class ProvideRepository:
    def __init__(self, client_repository, movie_repository, rental_repository):
        self.client_repository = client_repository
        self.movie_repository = movie_repository
        self.rental_repository = rental_repository


def get_repository_type():
    with open("settings.properties", "r") as f:
        repository_type = f.readline()
        client_file_name = f.readline().split()[2]
        movie_file_name = f.readline().split()[2]
        rental_file_name = f.readline().split()[2]
        try:
            if repository_type.split()[2] == "in_memory":
                return ProvideRepository(Repository(), Repository(), Repository())
            elif repository_type.split()[2] == "text_file":
                return ProvideRepository(TextFileRepository(client_file_name), TextFileRepository(movie_file_name),
                                         TextFileRepository(rental_file_name))
            elif repository_type.split()[2] == "binary_file":
                return ProvideRepository(BinaryRepository(client_file_name), BinaryRepository(movie_file_name),
                                         BinaryRepository(rental_file_name))
            else:
                raise ValueError("Invalid repository type!")
        except RepositoryException as re:
            print(re)
            exit()


provided_repository = get_repository_type()
ui = UI(provided_repository)
ui.run()
