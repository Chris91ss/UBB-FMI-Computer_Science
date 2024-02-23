from src.controller.controller import Controller
from src.repository.txt_repository import TxtRepository
from src.ui.ui import Ui

if __name__ == "__main__":
    file_path = "data/sentences.txt"

    sentence_repository = TxtRepository(file_path)
    controller = Controller(sentence_repository)
    ui = Ui(controller)

    ui.run_ui()
