from src.services.bookService import BookService


class UI:
    def __init__(self, repository):
        self.book_service = BookService(repository)

    def run(self):
        choice_number_one = "1"
        choice_number_two = "2"
        choice_number_three = "3"
        choice_number_four = "4"
        choice_number_five = "5"

        self.book_service.generate_random_values_at_startup()
        self.book_service.clear_stack()
        while True:
            print("1. Add book")
            print("2. Display")
            print("3. Filter books by first word in a title")
            print("4. Undo operation")
            print("5. Exit")
            user_choice = input("Enter your choice: ")
            if user_choice == choice_number_one:
                self.add_book()
            elif user_choice == choice_number_two:
                self.display_books()
            elif user_choice == choice_number_three:
                self.filter_books_by_first_word_in_title()
            elif user_choice == choice_number_four:
                self.undo_operation()
            elif user_choice == choice_number_five:
                break
            else:
                print("Invalid choice!")

    def add_book(self):
        try:
            length_of_isbn = 13

            isbn = input("Enter isbn: ")
            if len(isbn) == 0:
                raise ValueError("Invalid input!")
            if len(isbn.replace("-", "")) != length_of_isbn:
                raise ValueError("Invalid isbn!")

            title = input("Enter title: ")
            if len(title) == 0:
                raise ValueError("Invalid input!")

            author = input("Enter author: ")
            if len(author) == 0 or author.isalpha() is False:
                raise ValueError("Invalid input!")

            self.book_service.add_book(isbn, title, author)
        except ValueError as ve:
            print(ve)

    def filter_books_by_first_word_in_title(self):
        try:
            word_in_title = input("Enter first word of a title: ")
            if len(word_in_title) == 0:
                raise ValueError("Invalid input!")

            self.book_service.filter_books_by_first_word_in_title(word_in_title)
        except ValueError as ve:
            print(ve)

    def display_books(self):
        books = self.book_service.get_all_books()
        for book in books:
            print(book)

    def undo_operation(self):
        try:
            self.book_service.undo_operation()
        except ValueError as ve:
            print(ve)
