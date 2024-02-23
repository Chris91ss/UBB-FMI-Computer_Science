from unittest import TestCase

from src.domain.reservation import Reservation
from src.repository.reservation_repository import ReservationRepository


class TestReservationRepository(TestCase):

    def setUp(self):
        self.reservation_repository = ReservationRepository("repository/reservation_repository_test.txt")

    def test_add(self):
        reservation = Reservation(1, "1", "name", 1, "01.01", "01.02")
        self.reservation_repository.add(reservation)
        assert len(self.reservation_repository.get_all()) == 1
