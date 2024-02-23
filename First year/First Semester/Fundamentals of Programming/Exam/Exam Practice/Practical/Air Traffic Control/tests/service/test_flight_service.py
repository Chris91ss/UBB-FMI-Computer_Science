import unittest
from datetime import datetime

from src.exceptions.exceptions import InvalidFlightError
from src.repository.txt_repository import TxtRepository
from src.service.flight_service import FlightService


class TestFlightService(unittest.TestCase):
    def setUp(self) -> None:
        flight_repository = TxtRepository("data/test_flights.txt")
        self.__flight_service = FlightService(flight_repository)

    def test_add_flight(self):
        departure_time = "13:00"
        departure_time = datetime.strptime(departure_time, "%H:%M")
        arrival_time = "14:00"
        arrival_time = datetime.strptime(arrival_time, "%H:%M")

        self.__flight_service.add_flight("FR1234", "Bucharest", departure_time, "London", arrival_time)
        self.assertEqual(len(self.__flight_service.get_all()), 4)
        self.__flight_service.remove_flight("FR1234")  # Clean up

        departure_time = "13:00"
        departure_time = datetime.strptime(departure_time, "%H:%M")
        arrival_time = "13:05"
        arrival_time = datetime.strptime(arrival_time, "%H:%M")

        try:
            self.__flight_service.add_flight("FR1234", "Bucharest", departure_time, "London", arrival_time)
            self.fail()  # expected InvalidFlightError
        except InvalidFlightError:
            self.assertTrue(True)
