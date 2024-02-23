from src.exceptions.exceptions import QuestionError


class QuestionValidator:

    @staticmethod
    def validate_question(question_id: int, text: str, answers: list[str, str, str],
                          correct_answer: str, difficulty: str):

        errors = []

        if correct_answer not in answers:
            errors.append("correct answer not in answers")

        if difficulty not in ["easy", "medium", "hard"]:
            errors.append('difficulty not in ["easy", "medium", "hard"]')

        if errors:
            raise QuestionError(errors)
