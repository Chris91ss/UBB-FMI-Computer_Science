from datetime import datetime

from src.exceptions.exceptions import FlightServiceError, InvalidFlightError
from src.service.flight_service import FlightService


class ConsoleMenu:

    def __init__(self, flight_service: FlightService):
        self.__student_service = flight_service

    def start_ui(self):
        self.__print_title()

        options = {
            "1": self.__add_flight,
            "2": self.__remove_flight,
            "3": self.__list_airports,
            "4": self.__list_free_time_intervals,
            "5": self.__list_max_flights_broken_radar,
            "x": self.__exit
        }

        while True:
            self.__print_options()
            option = self.__get_option()

            try:
                options[option]()
            except KeyError:
                print("Invalid option!")
            except ValueError:
                print("Invalid input!")
            except InvalidFlightError as error:
                print(error)
            except FlightServiceError as error:
                print(error)

    # -------------------- #
    # -------------------- #
    # -------------------- #

    def __add_flight(self):
        flight_id = self.__get_flight_id()
        departure_city = self.__get_departure_city()
        departure_time = self.__get_departure_time()
        arrival_city = self.__get_arrival_city()
        arrival_time = self.__get_arrival_time()

        self.__student_service.add_flight(flight_id, departure_city, departure_time, arrival_city, arrival_time)

    def __remove_flight(self):
        flight_id = self.__get_flight_id()

        self.__student_service.remove_flight(flight_id)

    def __list_airports(self):
        airports = self.__student_service.get_airports()
        print("\nAirports:")
        for airport in airports:
            print(f"-> {airport}")

    def __list_free_time_intervals(self):
        free_time_intervals = self.__student_service.get_free_time_intervals()
        print("\nFree time intervals:")
        for free_time_interval in free_time_intervals:
            print(f"-> {free_time_interval}")

    def __list_max_flights_broken_radar(self):
        max_flights_broken_radar = self.__student_service.get_max_flights_broken_radar()
        print(f"\nThe maximum number of flights with a broken radar is {len(max_flights_broken_radar)}")
        print("The flights with a broken radar are:")
        for flight_id in max_flights_broken_radar:
            print(f"-> {flight_id}")

    @staticmethod
    def __exit():
        print("\nGoodbye!")
        exit(0)

    # -------------------- #
    # -------------------- #
    # -------------------- #

    @staticmethod
    def __get_option() -> str:
        option = input("\nOption: ")
        return option

    @staticmethod
    def __get_flight_id() -> str:
        flight_id = input("Flight ID: ")
        return flight_id

    @staticmethod
    def __get_departure_city() -> str:
        departure_city = input("Departure city: ")
        return departure_city

    @staticmethod
    def __get_departure_time() -> datetime:
        departure_time = input("Departure time: ")
        departure_time = datetime.strptime(departure_time, "%H:%M")
        return departure_time

    @staticmethod
    def __get_arrival_city() -> str:
        arrival_city = input("Arrival city: ")
        return arrival_city

    @staticmethod
    def __get_arrival_time() -> datetime:
        arrival_time = input("Arrival time: ")
        arrival_time = datetime.strptime(arrival_time, "%H:%M")
        return arrival_time

    # -------------------- #
    # -------------------- #
    # -------------------- #

    @staticmethod
    def __print_options():
        print("\n1: Add Flight")
        print("2: Remove Flight")
        print("3: List Airports")
        print("4: List free time intervals")
        print("5: List max flights with broken radar")
        print("x: Exit")

    @staticmethod
    def __print_title():
        print("\n# --------------------------------------------------- #")
        print("# --------------- Air Traffic Control --------------- #")
        print("# --------------------------------------------------- #")
