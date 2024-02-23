from src.controller import Controller
from src.domain.question import Question


class Ui:

    def __init__(self, controller: Controller):
        self.controller = controller

    def run_ui(self):
        Ui.print_title()

        commands = {
            "exit": Ui.exit,
            "add": self.add,
            "create": self.create,
            "start": Ui.start
        }

        while True:
            command, args = Ui.get_command()

            try:
                commands[command](*args)

            except Exception as error:
                print("\nInvalid input:", error)

    @staticmethod
    def exit():
        print("\nGoodbye!")
        exit(1)

    def add(self, question_id: str, text: str, choice_a: str, choice_b: str,
            choice_c: str, correct_choice: str, difficulty: str):

        question_id = int(question_id)
        answers = [choice_a, choice_b, choice_c]
        self.controller.add(question_id, text, answers, correct_choice, difficulty)

    def create(self, difficulty: str, number_of_questions: str, file_path: str):
        number_of_questions = int(number_of_questions)

        self.controller.create(difficulty, number_of_questions, file_path)

    @staticmethod
    def start(file_path: str):
        quiz = Controller.get_quiz(file_path)

        answers = []
        for question in quiz:
            Ui.print_question(question)

            answer = Ui.get_answer()
            answers.append(answer)

        score, max_score = Controller.compute_score(quiz, answers)
        print(f"\nYour score is {score} out of {max_score}")

    @staticmethod
    def get_command():
        command = input("\n>: ")
        first_word = command[0:command.find(" ")]

        if first_word == "add":
            arguments = command[command.find(" "):]
            arguments = [argument.strip() for argument in arguments.split(";")]
            return first_word, arguments

        else:
            command = [argument.strip() for argument in command.split(" ")]
            return command[0], command[1:]

    @staticmethod
    def get_answer() -> str:
        answer = input(">: ")
        return answer

    @staticmethod
    def print_title():
        print()
        print("# --------------------------- #")
        print("# ------- Quiz Master ------- #")
        print("# --------------------------- #")

    @staticmethod
    def print_question(question: Question):
        print(f"\n{question.text}")
        print(f"> {question.answers[0]}\n> {question.answers[1]}\n> {question.answers[2]}\n")
