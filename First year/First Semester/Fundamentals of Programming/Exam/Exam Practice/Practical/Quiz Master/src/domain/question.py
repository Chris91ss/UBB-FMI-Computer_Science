from dataclasses import dataclass


@dataclass
class Question:

    id: int
    text: str
    answers: list[str, str, str]
    correct_answer: str
    difficulty: str

    def __str__(self) -> str:
        return f"{self.id};{self.text};{self.answers[0]};{self.answers[1]};" \
               f"{self.answers[2]};{self.correct_answer};{self.difficulty}"
