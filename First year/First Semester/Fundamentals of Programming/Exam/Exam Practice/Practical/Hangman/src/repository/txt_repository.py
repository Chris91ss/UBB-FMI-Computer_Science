from src.domain.sentence import Sentence
from src.repository.generic_repository import GenericRepository


class TxtRepository(GenericRepository):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

        self.load_file()

    def load_file(self):
        try:
            with open(self.file_path, "r") as input_file:
                for index, line in enumerate(input_file.readlines()):
                    sentence = Sentence(index, line.strip())
                    self.all_data[index] = sentence
        except IOError:
            print("\nInvalid input file")

    def save_file(self):
        try:
            with open(self.file_path, "w") as output_file:
                for sentence in self.all_data.values():
                    output_file.write(f"{sentence.true_line}\n")
        except IOError:
            print("\nInvalid output file")

    def add(self, data):
        super().add(data)
        self.save_file()
