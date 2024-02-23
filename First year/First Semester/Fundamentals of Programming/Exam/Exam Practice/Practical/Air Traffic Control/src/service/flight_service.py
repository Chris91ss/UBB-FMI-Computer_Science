from datetime import datetime

from src.domain.flight import Flight
from src.exceptions.exceptions import FlightServiceError
from src.repository.txt_repository import TxtRepository
from src.validators.flight_validator import FlightValidator


class FlightService:

    def __init__(self, flight_repository: TxtRepository):
        self.__flight_repository = flight_repository

    def get_all(self) -> list[Flight]:
        return self.__flight_repository.get_all()

    def add_flight(self, flight_id: str, departure_city: str, departure_time: datetime,
                   flight_arrival_city: str, flight_arrival_time: datetime):
        """
        Adds a flight to the repository.
        :param flight_id: str, the id of the flight
        :param departure_city: str, the departure city of the flight
        :param departure_time: datetime, the departure time of the flight
        :param flight_arrival_city: str, the arrival city of the flight
        :param flight_arrival_time: datetime, the arrival time of the flight

        :raises FlightServiceError: if the flight id already exists
        :raises FlightServiceError: if there exists a duplicate time in the repository
        :raises InvalidFlightError: if the flight is invalid
        """

        if flight_id in self.__flight_repository.get_all_ids():
            raise FlightServiceError("Flight ID already exists.")

        for flight in self.__flight_repository.get_all():
            if flight.departure_time == departure_time or flight.arrival_time == flight_arrival_time:
                raise FlightServiceError("Duplicate time.")
            if flight.departure_time == flight_arrival_time or flight.arrival_time == departure_time:
                raise FlightServiceError("Duplicate time.")

        FlightValidator.validate_flight(flight_id, departure_city, departure_time,
                                        flight_arrival_city, flight_arrival_time)

        new_flight = Flight(flight_id, departure_city, departure_time, flight_arrival_city, flight_arrival_time)
        self.__flight_repository.add(new_flight)

    def remove_flight(self, flight_id: str):
        if flight_id not in self.__flight_repository.get_all_ids():
            raise FlightServiceError("Flight ID does not exist.")

        self.__flight_repository.remove_by_id(flight_id)

    def get_airports(self) -> list[str]:
        airports = {}
        for flight in self.__flight_repository.get_all():
            if flight.departure_city not in airports:
                airports[flight.departure_city] = 0
            if flight.arrival_city not in airports:
                airports[flight.arrival_city] = 0

            airports[flight.departure_city] += 1
            airports[flight.arrival_city] += 1

        airports = self.__sort_airports(airports)

        return airports

    @staticmethod
    def __sort_airports(airports: dict) -> list[str]:
        airports_list = list(airports.keys())
        airports_list.sort(key=lambda airport: airports[airport], reverse=True)

        return airports_list

    def get_free_time_intervals(self) -> list[str]:
        flights = self.__flight_repository.get_all()
        flights.sort(key=lambda flight: flight.departure_time)

        free_time_intervals = []
        for index in range(len(flights) - 1):
            if flights[index].arrival_time < flights[index + 1].departure_time:
                start_time = flights[index].arrival_time.strftime("%H:%M")
                end_time = flights[index + 1].departure_time.strftime("%H:%M")

                free_time_intervals.append(f"{start_time} - {end_time}")

        return free_time_intervals

    def get_max_flights_broken_radar(self) -> list[str]:
        flights = self.__flight_repository.get_all()
        flights.sort(key=lambda flight: flight.arrival_time)

        last_arrival_time = flights[0].arrival_time
        max_flights_ids = []

        for flight in flights[1:]:
            if flight.departure_time >= last_arrival_time:
                max_flights_ids.append(flight.id)

                last_arrival_time = flight.arrival_time

        max_flights = []
        for flight_id in max_flights_ids:
            flight = self.__flight_repository.get_by_id(flight_id)
            departure_time = flight.departure_time.strftime("%H:%M")
            arrival_time = flight.arrival_time.strftime("%H:%M")

            flight_string = f"{departure_time} | {arrival_time} | {flight_id} | " \
                            f"{flight.departure_city} - {flight.arrival_city}"

            max_flights.append(flight_string)

        return max_flights
