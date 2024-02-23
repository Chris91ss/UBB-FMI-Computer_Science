class Sentence:

    def __init__(self, sentence_id: int, true_line: str):
        self.id = sentence_id
        self.true_line = true_line

        self.shown_line = []
        for character in true_line:
            if character == " ":
                self.shown_line.append(character)

            else:
                self.shown_line.append("_")

        self.shown_letters = []
        self.show_first_last_letters()

    def show_first_last_letters(self):
        for index, letter in enumerate(self.true_line):
            if not self.duplicate_letter(letter) and letter != " ":
                if index == 0 or index == len(self.true_line) - 1:
                    self.show_letter(letter)

                if self.true_line[index - 1] == " " or self.true_line[index + 1] == " ":
                    self.show_letter(letter)

    def show_letter(self, letter: str):
        if self.found_letter(letter):
            for index, current_letter in enumerate(self.true_line):
                if current_letter == letter:
                    self.shown_line[index] = letter

            self.shown_letters.append(letter)

    def found_letter(self, letter: str) -> bool:
        return letter in self.true_line

    def duplicate_letter(self, letter: str) -> bool:
        return letter in self.shown_letters


class SentenceError(Exception):
    pass
