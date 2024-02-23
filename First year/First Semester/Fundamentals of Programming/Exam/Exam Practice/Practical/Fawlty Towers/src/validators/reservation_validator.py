from datetime import datetime

from src.exceptions.exceptions import ReservationError
from src.repository.room_repository import RoomRepository


class ReservationValidator:

    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def validate_reservation(self, room_number: str, name: str, number_of_guests: int,
                             arrival_date: datetime, departure_date: datetime):
        errors = []

        if not len(name):
            errors.append("name can not be empty")

        room = self.room_repository.get(room_number)
        if number_of_guests > room.capacity:
            errors.append("too many people")
        if number_of_guests <= 0:
            errors.append("reservation must have guests")

        if arrival_date > departure_date:
            errors.append("invalid arrival and departure dates")

        if errors:
            raise ReservationError(errors)
