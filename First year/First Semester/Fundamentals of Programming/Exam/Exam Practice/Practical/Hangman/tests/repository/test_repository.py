from unittest import TestCase

from src.domain.sentence import Sentence
from src.repository.generic_repository import GenericRepository
from src.repository.txt_repository import TxtRepository


class TestGenericRepository(TestCase):

    def setUp(self):
        self.generic_repository = GenericRepository()

    def test_add(self):
        self.generic_repository.add(Sentence(1, "test"))
        self.assertEqual(len(self.generic_repository.get_all()), 1)

    def test_get(self):
        sentence = Sentence(1, "test")
        self.generic_repository.add(sentence)
        self.assertEqual(self.generic_repository.get(1), sentence)

    def test_get_all(self):
        self.generic_repository.add(Sentence(1, "test"))
        self.generic_repository.add(Sentence(2, "test"))
        self.assertEqual(len(self.generic_repository.get_all()), 2)


class TestTxtRepository(TestCase):

    def setUp(self):
        self.txt_repository = TxtRepository("repository/test.txt")

    def test_load_file(self):
        self.assertEqual(len(self.txt_repository.get_all()), 1)

    def test_save_file(self):
        self.txt_repository.add(Sentence(1, "cars are cool"))
        self.assertEqual(len(self.txt_repository.get_all()), 2)
        self.txt_repository.remove(1)
