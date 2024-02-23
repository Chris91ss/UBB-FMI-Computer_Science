from unittest import TestCase

from src.controller.controller import Controller
from src.repository.reservation_repository import ReservationRepository
from src.repository.room_repository import RoomRepository


class TestController(TestCase):

    def setUp(self):
        room_repository = RoomRepository("controller/room_repository_test.txt")
        reservation_repository = ReservationRepository("controller/reservation_repository_test.txt")
        self.controller = Controller(reservation_repository, room_repository)

    def test_create_reservation(self):
        self.controller.create_reservation("01", "name", 1, "01.01", "01.02")
        assert len(self.controller.reservations_repository.get_all()) == 1
        assert len(self.controller.room_repository.get("01").booked_intervals) == 1
