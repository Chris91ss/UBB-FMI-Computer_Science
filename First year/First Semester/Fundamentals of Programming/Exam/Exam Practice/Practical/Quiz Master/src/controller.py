import random

from src.domain.question import Question
from src.exceptions.exceptions import ControllerError, QuestionError
from src.validators.question_validator import QuestionValidator


class Controller:

    def __init__(self, question_repository):
        self.question_repository = question_repository

    def add(self, question_id: int, text: str, answers: list[str, str, str], correct_answer: str, difficulty: str):
        QuestionValidator.validate_question(question_id, text, answers, correct_answer, difficulty)
        if question_id in self.question_repository.get_all_ids():
            raise QuestionError("duplicate id")

        question = Question(question_id, text, answers, correct_answer, difficulty)
        self.question_repository.add(question)

    def create(self, difficulty: str, number_of_questions: int, file_path: str):
        # validating
        if difficulty not in ["easy", "medium", "hard"]:
            raise ControllerError('difficulty not in ["easy", "medium", "hard"]')

        questions = self.question_repository.get_all()

        questions_with_same_difficulty = []
        questions_with_other_difficulty = []
        for question in questions:
            if question.difficulty == difficulty:
                questions_with_same_difficulty.append(question)
            else:
                questions_with_other_difficulty.append(question)

        if len(questions_with_same_difficulty) < number_of_questions // 2:
            raise ControllerError(f"not enough questions with {difficulty} difficulty")

        # creating quiz
        number_of_questions_with_same_difficulty = number_of_questions // 2
        number_of_questions_with_other_difficulty = number_of_questions - number_of_questions // 2
        quiz = []

        while number_of_questions_with_same_difficulty:
            random_index = random.randint(0, len(questions_with_same_difficulty) - 1)
            random_question_with_same_difficulty = questions_with_same_difficulty[random_index]

            quiz.append(random_question_with_same_difficulty)
            questions_with_same_difficulty.remove(random_question_with_same_difficulty)

            number_of_questions_with_same_difficulty -= 1

        while number_of_questions_with_other_difficulty:
            random_index = random.randint(0, len(questions_with_other_difficulty) - 1)
            random_question_with_other_difficulty = questions_with_other_difficulty[random_index]

            quiz.append(random_question_with_other_difficulty)
            questions_with_other_difficulty.remove(random_question_with_other_difficulty)

            number_of_questions_with_other_difficulty -= 1

        # saving the quiz into the file
        with open(f"data/{file_path}", "w") as output_file:
            for question in quiz:
                output_file.write(f"{question}\n")

    @staticmethod
    def get_quiz(file_path: str) -> list[Question]:
        quiz = []

        with open(f"data/{file_path}", "r") as input_file:
            for line in input_file.readlines():
                line = line.strip()
                args = line.split(";")

                question_id = int(args[0])
                text = args[1]
                answers = [args[2], args[3], args[4]]
                correct_answer = args[5]
                difficulty = args[6]

                try:
                    QuestionValidator.validate_question(question_id, text, answers,
                                                        correct_answer, difficulty)
                except QuestionError:
                    continue

                question = Question(question_id, text, answers, correct_answer, difficulty)
                quiz.append(question)

        return quiz

    @staticmethod
    def compute_score(quiz: list[Question], answers: list[str]) -> int:
        score = 0
        max_score = 0
        for (question, answers) in zip(quiz, answers):
            if question.correct_answer == answers:
                if question.difficulty == "easy":
                    score += 1
                elif question.difficulty == "medium":
                    score += 2
                elif question.difficulty == "hard":
                    score += 3

            if question.difficulty == "easy":
                max_score += 1
            elif question.difficulty == "medium":
                max_score += 2
            elif question.difficulty == "hard":
                max_score += 3

        return score, max_score
