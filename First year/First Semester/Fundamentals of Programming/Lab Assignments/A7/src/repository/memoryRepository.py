from src.domain.books import Book


class MemoryRepository:
    def __init__(self):
        self._data = {}
        self._stack = []

    def add(self, new_book: Book):
        if new_book.book_isbn in self._data:
            raise Exception(f"Book with isbn {new_book.book_isbn} already exists!")
        self._data[new_book.book_isbn] = new_book
        operation = ["add"]
        self._stack.append(operation)

    def clear_stack(self):
        self._stack = []

    def clear_data(self):
        self._data.clear()

    def get_all(self):
        return list(self._data.values())

    def filter(self, title):
        operation = ["filter"]
        filtered_dictionary = {}
        unfiltered_dictionary = self._data.copy()
        for book in self._data.values():
            first_word = book.book_title.split()[0]
            if first_word != title:
                filtered_dictionary[book.book_isbn] = book

        self._data = filtered_dictionary.copy()
        operation.append(unfiltered_dictionary)
        self._stack.append(operation)

    def add_books(self, list_of_books):
        for new_book in list_of_books:
            self._data[new_book.book_isbn] = new_book

    def undo_operation(self):
        first_element_index = 0
        second_element_index = 1

        if len(self._stack) == 0:
            raise ValueError("No more undo operations!")

        operation_stack = self._stack[-1]
        self._stack.pop()

        if operation_stack[first_element_index] == "filter":
            self._data = operation_stack[second_element_index]
        else:
            data_list = list(self._data.items())
            data_list.pop()
            self._data = dict(data_list)
