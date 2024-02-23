from src.controller.controller import Controller
from src.repository.reservation_repository import ReservationRepository
from src.repository.room_repository import RoomRepository
from src.ui.ui import Ui

if __name__ == "__main__":
    rooms_path = "data/room_configurations.txt"
    reservations_path = "data/reservations.txt"

    reservations_repository = ReservationRepository(reservations_path)
    room_repository = RoomRepository(rooms_path)
    controller = Controller(reservations_repository, room_repository)
    ui = Ui(controller)

    ui.run_ui()
