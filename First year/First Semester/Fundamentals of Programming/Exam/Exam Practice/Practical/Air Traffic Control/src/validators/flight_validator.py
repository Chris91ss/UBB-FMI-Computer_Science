from datetime import datetime

from src.exceptions.exceptions import InvalidFlightError


class FlightValidator:

    @staticmethod
    def validate_flight(flight_id: str, flight_departure_city: str, flight_departure_time: datetime,
                        flight_arrival_city: str, flight_arrival_time: datetime):

        errors = []

        if not flight_id:
            errors.append("Flight ID cannot be empty.")

        if not flight_departure_city:
            errors.append("Flight departure city cannot be empty.")

        if not flight_arrival_city:
            errors.append("Flight arrival city cannot be empty.")

        if flight_departure_time >= flight_arrival_time:
            errors.append("Flight arrival time must be after departure time.")

        flight_duration = flight_arrival_time - flight_departure_time
        flight_duration = flight_duration.total_seconds() / 60

        if flight_duration not in range(15, 91):
            errors.append("Flight duration must be between 15 and 90 minutes.")

        if errors:
            raise InvalidFlightError(errors)
