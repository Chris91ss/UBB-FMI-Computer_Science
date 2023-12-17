from src.services.bookService import BookService


class Test:
    def __init__(self, repository):
        self.book_service = BookService(repository)

    def run_tests(self):
        self.test_add()
        self.test_filter()
        self.test_undo_operation()

    def test_add(self):
        self.book_service.clear_data()
        self.book_service.add_book("123", "title", "author")
        assert len(self.book_service.get_all_books()) == 1
        self.book_service.add_book("123", "title", "author")
        assert len(self.book_service.get_all_books()) == 1
        self.book_service.add_book("124", "title", "author")
        assert len(self.book_service.get_all_books()) == 2

    def test_filter(self):
        self.book_service.clear_data()
        self.book_service.add_book("125", "title", "author")
        self.book_service.add_book("126", "title", "author")
        self.book_service.filter_books_by_first_word_in_title("title")
        assert len(self.book_service.get_all_books()) == 0

    def test_undo_operation(self):
        self.book_service.clear_data()
        self.book_service.add_book("127", "title", "author")
        self.book_service.add_book("128", "title", "author")
        self.book_service.undo_operation()
        assert len(self.book_service.get_all_books()) == 1
        self.book_service.undo_operation()
        assert len(self.book_service.get_all_books()) == 0
        try:
            self.book_service.undo_operation()
        except ValueError as ve:
            print(ve)
