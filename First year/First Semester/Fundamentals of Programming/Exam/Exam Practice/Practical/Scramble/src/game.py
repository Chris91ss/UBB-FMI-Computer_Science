import random

from src.exceptions import GameError


class Game:

    def __init__(self, input_path: str):
        self.solved_word = Game.__get_random_word(input_path)
        self.scrambled_word = Game.__get_scrambled_word(self.solved_word, len(self.solved_word) // 2)
        self.score = Game.__get_score(self.solved_word)

        self.history = [self.scrambled_word]

    @staticmethod
    def __get_random_word(input_path: str) -> str:
        with open(input_path, "r") as input_file:
            lines = [line.strip() for line in input_file.readlines()]
            random_word = lines[random.randint(0, len(lines) - 1)]

            return random_word

    @staticmethod
    def __get_scrambled_word(solved_word: str, number_of_swaps: int) -> str:
        solved_word = list(solved_word)
        while number_of_swaps:
            position_1 = random.randint(1, len(solved_word) - 2)
            position_2 = random.randint(1, len(solved_word) - 2)

            if position_1 == position_2 or solved_word[position_1] == " " or solved_word[position_2] == " ":
                continue

            solved_word[position_1], solved_word[position_2] = solved_word[position_2], solved_word[position_1]

            number_of_swaps -= 1

        solved_word = "".join(solved_word)
        return solved_word

    @staticmethod
    def __get_score(solved_word: str) -> int:
        score = 0
        for letter in solved_word:
            if letter != " ":
                score += 1

        return score

    def swap(self, word_1_index: int, letter_1: int, word_2_index: int, letter_2: int) -> str:
        words = self.scrambled_word.split(" ")

        # same words
        if word_1_index == word_2_index:
            word = list(words[word_1_index])
            word[letter_1], word[letter_2] = word[letter_2], word[letter_1]
            word = "".join(word)

            words[word_1_index] = word

        # different words
        else:
            word_1, word_2 = list(words[word_1_index]), list(words[word_2_index])

            word_1[letter_1], word_2[letter_2] = word_2[letter_2], word_1[letter_1]
            word_1, word_2 = "".join(word_1), "".join(word_2)

            words[word_1_index], words[word_2_index] = word_1, word_2

        new_scrambled_word = ""
        for word in words:
            new_scrambled_word += word + " "
        new_scrambled_word = new_scrambled_word.strip()

        self.scrambled_word = new_scrambled_word
        self.score -= 1
        self.history.append(self.scrambled_word)

        if self.scrambled_word == self.solved_word or self.score == 0:
            return "GAME OVER"

        return "CONTINUE"

    def undo(self):
        if len(self.history) <= 1:
            raise GameError("no more undoes")

        self.history.pop()
        self.scrambled_word = self.history.pop(-1)
