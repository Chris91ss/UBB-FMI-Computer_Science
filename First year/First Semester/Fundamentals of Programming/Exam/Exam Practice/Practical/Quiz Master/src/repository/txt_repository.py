from src.domain.question import Question
from src.exceptions.exceptions import QuestionError
from src.repository.general_repository import GeneralRepository
from src.validators.question_validator import QuestionValidator


class TxtRepository(GeneralRepository):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

        self.load_data()

    def load_data(self):
        with open(self.file_path, "r") as input_file:
            for line in input_file.readlines():
                line = line.strip()
                args = line.split(";")

                data_id = int(args[0])
                data_text = args[1]
                data_answers = [args[2], args[3], args[4]]
                data_correct_answer = args[5]
                data_difficulty = args[6]

                try:
                    QuestionValidator.validate_question(data_id, data_text, data_answers,
                                                        data_correct_answer, data_difficulty)
                except QuestionError:
                    continue

                data = Question(data_id, data_text, data_answers, data_correct_answer, data_difficulty)
                self.all_data[data_id] = data

    def save_data(self):
        with open(self.file_path, "w") as output_file:
            for data in self.all_data.values():
                output_file.write(f"{data}\n")

    def add(self, data):
        super().add(data)
        self.save_data()

    def delete(self, data):
        super().delete(data)
        self.save_data()

    def delete_by_id(self, data_id: int):
        super().delete_by_id(data_id)
        self.save_data()
