from src.domain.room import Room
from src.repository.general_repository import GeneralRepository


class RoomRepository(GeneralRepository):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.load_data()

    def load_data(self):
        with open(self.file_path, "r") as input_file:
            for line in input_file.readlines():
                args = [argument.strip() for argument in line.split(";")]

                room_id = args[0]
                room_type = args[1]

                room = Room(room_id, room_type)
                self.all_data[room_id] = room
