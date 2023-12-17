import random
from src.domain.books import Book


class BookService:
    def __init__(self, repository):
        self.repository = repository

    def generate_random_values_at_startup(self):
        list_of_book_authors = ["J.K. Rowling", "J.R.R. Tolkien", "George R.R. Martin", "Stephen King", "Agatha Christie"]
        list_of_book_titles = ["East of Eden", "The Great Gatsby", "The Grapes of Wrath", "To Kill a Mockingbird", "War and Peace"]
        list_of_book_isbn = ["978-3-16-148410-0", "978-3-16-148411-0", "978-3-16-148412-0", "978-3-16-148413-0",
                             "978-3-16-148414-0", "978-3-16-148415-0", "978-3-16-148416-0", "978-3-16-148417-0",
                             "978-3-16-148418-0", "978-3-16-148419-0"]
        number_of_books = 10
        for i in range(number_of_books):
            random_book_isbn = list_of_book_isbn[i]
            random_book_author = random.choice(list_of_book_authors)
            random_book_title = random.choice(list_of_book_titles)
            self.add_book(random_book_isbn, random_book_title, random_book_author)

    def add_book(self, isbn: str, title: str, author: str):
        new_book = Book(isbn, title, author)
        try:
            self.repository.add(new_book)
        except Exception as ex:
            print(ex)

    def filter_books_by_first_word_in_title(self, author):
        self.repository.filter(author)

    def clear_stack(self):
        self.repository.clear_stack()

    def clear_data(self):
        self.repository.clear_data()

    def get_all_books(self):
        return self.repository.get_all()

    def undo_operation(self):
        self.repository.undo_operation()
