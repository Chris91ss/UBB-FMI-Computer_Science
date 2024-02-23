import random

from src.domain.sentence import SentenceError, Sentence
from src.domain.sentence_validator import SentenceValidator
from src.repository.txt_repository import TxtRepository


class Controller:

    def __init__(self, sentence_repository: TxtRepository):
        self.sentence_repository = sentence_repository

        self.selected_sentence = random.choice(self.sentence_repository.get_all())

        self.game_over = False
        self.lost = False
        self.hangman = "HANGMAN"
        self.mistakes = 0

    def add_sentence(self, new_sentence: str):
        SentenceValidator.validate_sentence(new_sentence)
        if new_sentence in self.sentence_repository.get_all():
            raise SentenceError("duplicate sentence")

        sentence_id = len(self.sentence_repository.get_all())
        sentence = Sentence(sentence_id, new_sentence)

        self.sentence_repository.add(sentence)

    def add_letter(self, letter: str):
        if self.selected_sentence.duplicate_letter(letter):
            raise ControllerError("duplicate letter")

        if self.selected_sentence.found_letter(letter):
            self.selected_sentence.show_letter(letter)

            if self.get_shown_line() == self.selected_sentence.true_line:
                self.game_over = True

        else:
            self.mistakes += 1
            if self.mistakes == len(self.hangman):
                self.game_over = True
                self.lost = True

    def get_shown_line(self) -> str:
        shown_line = self.selected_sentence.shown_line
        shown_line = "".join(shown_line)

        return shown_line

    def get_true_line(self) -> str:
        return self.selected_sentence.true_line

    def get_hangman(self) -> str:
        return self.hangman[0:self.mistakes]


class ControllerError(Exception):
    pass
