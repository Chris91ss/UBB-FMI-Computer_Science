
class Book:
    def __init__(self, isbn: str, title: str, author: str):
        self.book_isbn = isbn
        self.book_title = title
        self.book_author = author

    def __str__(self):
        return f"Book: {self.book_isbn}, {self.book_title}, {self.book_author}"
