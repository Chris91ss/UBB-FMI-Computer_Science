from src.repository.memoryRepository import MemoryRepository
from src.repository.binaryRepository import BinaryRepository
from src.repository.textFileRepository import TextFileRepository
from src.repository.jsonRepository import JsonRepository
from src.ui.ui import UI
from src.tests.tests import Test


def test_memory_repository():
    test = Test(MemoryRepository())
    test.run_tests()


def test_binary_repository():
    test = Test(BinaryRepository("test.bin"))
    test.run_tests()


def test_text_file_repository():
    test = Test(TextFileRepository("test.txt"))
    test.run_tests()


def test_json_repository():
    test = Test(JsonRepository("test.json"))
    test.run_tests()


def run_all_tests():
    test_memory_repository()
    test_binary_repository()
    test_text_file_repository()
    test_json_repository()


def get_repository_instance_from_settings():
    with open("settings.properties", "r") as f:
        line = f.readline()
        line = line.strip()
        try:
            if line == "memory":
                return MemoryRepository()
            elif line == "binary":
                return BinaryRepository()
            elif line == "text":
                return TextFileRepository()
            elif line == "json":
                return JsonRepository()
            else:
                raise ValueError("Invalid repository type!")
        except ValueError as ve:
            print(ve)
            exit()


run_all_tests()
UI(get_repository_instance_from_settings()).run()
