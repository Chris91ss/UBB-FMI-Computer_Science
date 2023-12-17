from src.domain.books import Book
from src.repository.memoryRepository import MemoryRepository

import json


class JsonRepository(MemoryRepository):
    def __init__(self, _file_name="books.json"):
        super().__init__()
        self._file_name = _file_name
        try:
            self._load_from_file()
        except json.decoder.JSONDecodeError:
            print("File is empty! There is nothing to load from the file!")

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
        books = []
        with open(self._file_name, "w") as f:
            for book in self._data.values():
                books.append(book.__dict__)
            json.dump(books, f, indent=4)

    def _load_from_file(self):
        try:
            with open(self._file_name, "r") as f:
                books = json.load(f)
                for book in books:
                    new_book = Book(book["book_isbn"], book["book_title"], book["book_author"])
                    self._data[new_book.book_isbn] = new_book
        except FileNotFoundError:
            self._data = {}
        except EOFError:
            self._data = {}
