from unittest import TestCase

from src.domain.sentence import Sentence


class TestSentence(TestCase):

    def setUp(self):
        self.sentence = Sentence(1, 'anna has apples')

    def test_show_first_last_letters(self):
        self.assertEqual(self.sentence.shown_line, ['a', '_', '_', 'a', ' ', 'h', 'a', 's', ' ', 'a', '_', '_', '_', '_', 's'])
