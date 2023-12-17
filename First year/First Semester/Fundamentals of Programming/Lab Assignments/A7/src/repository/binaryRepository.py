import pickle
from src.domain.books import Book
from src.repository.memoryRepository import MemoryRepository


class BinaryRepository(MemoryRepository):
    def __init__(self, _file_name="books.bin"):
        super().__init__()
        self._file_name = _file_name
        self._load_from_file()

    def add(self, new_book: Book):
        super().add(new_book)
        self._save_to_file()

    def clear_stack(self):
        super().clear_stack()
        self._save_to_file()

    def clear_data(self):
        super().clear_data()
        self._save_to_file()

    def filter(self, title):
        super().filter(title)
        self._save_to_file()

    def add_books(self, list_of_books):
        super().add_books(list_of_books)
        self._save_to_file()

    def undo_operation(self):
        super().undo_operation()
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
