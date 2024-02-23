from unittest import TestCase

from src.controller.controller import Controller
from src.repository.txt_repository import TxtRepository


class TestController(TestCase):

    def setUp(self):
        self.txt_repository = TxtRepository("controller/test.txt")
        self.controller = Controller(self.txt_repository)

    def test_randomize_sentence(self):
        self.controller.randomize_sentence()
        self.assertIsNotNone(self.controller.selected_sentence)

    def test_add_sentence(self):
        self.controller.add_sentence("cars are cool")
        self.assertEqual(len(self.controller.sentence_repository.get_all()), 2)
        self.assertEqual(self.controller.sentence_repository.get_all()[1].true_line, "cars are cool")
        self.txt_repository.remove(1)
