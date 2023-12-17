from src.domain.books import Book
from src.repository.memoryRepository import MemoryRepository


class TextFileRepository(MemoryRepository):
    def __init__(self, _file_name="books.txt"):
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
        with open(self._file_name, "w") as f:
            for book in self._data.values():
                f.write(f"{book.book_isbn}, {book.book_title}, {book.book_author}\n")

    def _load_from_file(self):
        try:
            with open(self._file_name, "r") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                    book_isbn, book_title, book_author = line.split(",")
                    new_book = Book(book_isbn, book_title, book_author)
                    self._data[new_book.book_isbn] = new_book
        except FileNotFoundError:
            self._data = {}
        except EOFError:
            self._data = {}
