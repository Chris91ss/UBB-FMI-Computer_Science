from src.domain.sentence import SentenceError


class SentenceValidator:

    @staticmethod
    def validate_sentence(sentence: str):
        errors = []

        words = sentence.split()
        if not words:
            errors.append("empty sentence")

        for word in words:
            if len(word) < 3:
                errors.append("word too short")
                break

        if errors:
            raise SentenceError(errors)
