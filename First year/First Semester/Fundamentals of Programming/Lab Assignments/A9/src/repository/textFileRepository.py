from src.repository.repository import Repository
from src.domain.client import Client
from src.domain.movie import Movie
from src.domain.rental import Rental


class TextFileRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load_from_file()

    def add(self, element):
        super().add(element)
        self._save_to_file()

    def remove(self, element):
        super().remove(element)
        self._save_to_file()

    def update(self, element):
        super().update(element)
        self._save_to_file()

    def _save_to_file(self):
        with open(self._file_name, "w") as f:
            for element in self._data.values():
                if isinstance(element, Client):
                    f.write(f"client, {element.id}, {element.name}\n")
                elif isinstance(element, Movie):
                    f.write(f"movie, {element.id}, {element.title}, {element.description}, {element.genre}\n")
                elif isinstance(element, Rental):
                    f.write(f"rental, {element.id}, {element.client_id}, {element.movie_id}, {element.rented_date}, "
                            f"{element.due_date}, {element.returned_date}\n")

    def _load_from_file(self):
        self._data = {}
        try:
            with open(self._file_name, "r") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                    line = line.split(",")
                    if line[0] == "client":
                        client = Client(int(line[1]), line[2])
                        super().add(client)
                    elif line[0] == "movie":
                        movie = Movie(int(line[1]), line[2], line[3], line[4])
                        super().add(movie)
                    elif line[0] == "rental":
                        rental = Rental(int(line[1]), int(line[2]), int(line[3]), line[4], line[5], line[6])
                        super().add(rental)
        except FileNotFoundError:
            self._data = {}
        except EOFError:
            self._data = {}
