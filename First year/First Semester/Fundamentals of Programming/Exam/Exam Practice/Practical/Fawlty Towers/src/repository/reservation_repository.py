from datetime import datetime

from src.domain.reservation import Reservation
from src.repository.general_repository import GeneralRepository


class ReservationRepository(GeneralRepository):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.load_data()

    def load_data(self):
        with open(self.file_path, "r") as input_file:
            for line in input_file.readlines():
                args = [argument.strip() for argument in line.split(";")]

                reservation_id = int(args[0])
                room_number = args[1]
                name = args[2]
                number_of_guests = int(args[3])
                arrival_date = args[4]
                arrival_date = datetime.strptime(arrival_date, "%m.%d")
                departure_date = args[5]
                departure_date = datetime.strptime(departure_date, "%m.%d")

                reservation = Reservation(reservation_id, room_number, name, number_of_guests,
                                          arrival_date, departure_date)
                self.all_data[reservation_id] = reservation
