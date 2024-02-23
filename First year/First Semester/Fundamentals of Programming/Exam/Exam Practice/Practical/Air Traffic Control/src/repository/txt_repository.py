from datetime import datetime

from src.domain.flight import Flight
from src.exceptions.exceptions import InvalidFlightError
from src.repository.generic_repository import GenericRepository
from src.validators.flight_validator import FlightValidator


class TxtRepository(GenericRepository):
    def __init__(self, file_path: str):
        super().__init__()
        self.__file_path = file_path
        self.__load_data()

    def __load_data(self):
        with open(self.__file_path, "r") as file:
            for line in file:
                data_arguments = line.split(",")
                data_arguments = [argument.strip() for argument in data_arguments]

                try:  # verify if we have the correct number of arguments
                    data_id = data_arguments[0]
                    data_departure_city = data_arguments[1]

                    data_departure_time = data_arguments[2]
                    data_departure_time = datetime.strptime(data_departure_time, "%H:%M")

                    data_arrival_city = data_arguments[3]

                    data_arrival_time = data_arguments[4]
                    data_arrival_time = datetime.strptime(data_arrival_time, "%H:%M")

                    if data_id in self.get_all_ids():
                        raise InvalidFlightError("Duplicate id.")

                    for flight in self.get_all():
                        if flight.departure_time == data_departure_time or flight.arrival_time == data_arrival_time:
                            raise InvalidFlightError("Duplicate time.")
                        if flight.departure_time == data_arrival_time or flight.arrival_time == data_departure_time:
                            raise InvalidFlightError("Duplicate time.")

                    FlightValidator.validate_flight(data_id, data_departure_city, data_departure_time,
                                                    data_arrival_city, data_arrival_time)

                    data = Flight(data_id, data_departure_city, data_departure_time,
                                  data_arrival_city, data_arrival_time)
                    self.add(data)

                except IndexError:  # if we don't have the correct number of arguments
                    continue
                except ValueError:  # if we have invalid arguments (like str instead of int)
                    continue
                except InvalidFlightError:  # validator failed
                    continue

    def __save_data(self):
        with open(self.__file_path, "w") as file:
            for data in self.get_all():
                file.write(f"{data}\n")

    def update(self):
        self.__save_data()

    # -------------------- #
    # -------------------- #
    # -------------------- #

    def add(self, data):
        super().add(data)
        self.__save_data()

    def remove(self, data):
        super().remove(data)
        self.__save_data()

    def remove_by_id(self, data_id: str):
        super().remove_by_id(data_id)
        self.__save_data()