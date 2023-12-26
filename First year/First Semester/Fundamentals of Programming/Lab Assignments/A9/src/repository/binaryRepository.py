from src.repository.repository import Repository
import pickle


class BinaryRepository(Repository):
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
        with open(self._file_name, "wb") as f:
            pickle.dump(self._data, f)

    def _load_from_file(self):
        try:
            with open(self._file_name, "rb") as f:
                self._data = pickle.load(f)
        except FileNotFoundError:
            self._data = {}
        except EOFError:
            self._data = {}
