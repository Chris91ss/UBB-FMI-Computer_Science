from src.controller import Controller
from src.repository.txt_repository import TxtRepository
from src.ui import Ui

if __name__ == "__main__":
    file_path = "data/master_questions_list.txt"

    question_repository = TxtRepository(file_path)
    controller = Controller(question_repository)
    ui = Ui(controller)

    ui.run_ui()
