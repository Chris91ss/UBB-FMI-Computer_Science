from datetime import datetime

from src.domain.reservation import Reservation
from src.domain.room import Room
from src.exceptions.exceptions import ControllerError
from src.repository.reservation_repository import ReservationRepository
from src.repository.room_repository import RoomRepository
from src.validators.reservation_validator import ReservationValidator


class Controller:

    def __init__(self, reservations_repository: ReservationRepository, room_repository: RoomRepository):
        self.reservations_repository = reservations_repository
        self.room_repository = room_repository

        self.reservation_validator = ReservationValidator(room_repository)

    def get_all_reservations(self) -> dict[str, list[Reservation]]:
        all_reservations = self.reservations_repository.get_all()
        all_reservations.sort(key=lambda reservation: (reservation.arrival_date, reservation.name))

        sorted_by_month_reservations = {}
        for month in ["January", "February", "March", "April", "May", "June", "July",
                      "August", "September", "October", "November", "December"]:
            sorted_by_month_reservations[month] = []

        for reservation in all_reservations:
            sorted_by_month_reservations[reservation.arrival_month].append(reservation)
            if reservation.arrival_month != reservation.departure_month:
                sorted_by_month_reservations[reservation.departure_month].append(reservation)

        return sorted_by_month_reservations

    def get_available_rooms(self, arrival_date: datetime, departure_date: datetime) -> list[Room]:
        all_rooms = self.room_repository.get_all()
        available_rooms = []

        for room in all_rooms:
            available = True
            for booked_interval in room.booked_intervals:
                if booked_interval[0] < arrival_date < booked_interval[1]:
                    available = False
                    break
                if booked_interval[0] < departure_date < booked_interval[1]:
                    available = False
                    break

            if available:
                available_rooms.append(room)

        return available_rooms

    def create_reservation(self, room_number: str, name: str, number_of_guests: int,
                           arrival_date: datetime, departure_date: datetime):
        self.reservation_validator.validate_reservation(room_number, name, number_of_guests,
                                                        arrival_date, departure_date)

        reservation_id = len(self.reservations_repository.get_all())
        reservation = Reservation(reservation_id, room_number, name, number_of_guests, arrival_date, departure_date)
        self.reservations_repository.add(reservation)

        room = self.room_repository.get(room_number)
        room.booked_intervals.append((arrival_date, departure_date))

    def delete_by_id(self, reservation_id: int):
        reservation = self.reservations_repository.get(reservation_id)
        self.reservations_repository.delete_by_id(reservation_id)

        room = self.room_repository.get(reservation.room_number)
        room.booked_intervals.remove((reservation.arrival_date, reservation.departure_date))

    def delete_by_date(self, arrival_date: datetime, departure_date: datetime, room_number: str):
        # validating
        if arrival_date > departure_date:
            raise ControllerError("invalid arrival/departure date")

        if room_number not in self.room_repository.get_ids():
            raise ControllerError("invalid room number")

        # getting the deleted reservations
        deleted_reservations = []
        deleted_reservations_by_months = {}
        for month in ["January", "February", "March", "April", "May", "June", "July",
                      "August", "September", "October", "November", "December"]:
            deleted_reservations_by_months[month] = []

        reservations = self.reservations_repository.get_all()
        for reservation in reservations:
            if reservation.room_number == room_number:
                if arrival_date <= reservation.arrival_date <= departure_date:
                    deleted_reservations_by_months[reservation.arrival_month].append(reservation)
                    if reservation.arrival_month != reservation.departure_month:
                        deleted_reservations_by_months[reservation.departure_month].append(reservation)

                    deleted_reservations.append(reservation)
                    continue
                if arrival_date <= reservation.departure_date <= departure_date:
                    deleted_reservations_by_months[reservation.arrival_month].append(reservation)
                    if reservation.arrival_month != reservation.departure_month:
                        deleted_reservations_by_months[reservation.departure_month].append(reservation)

                    deleted_reservations.append(reservation)
                    continue

        # actually deleting
        for deleted_reservation in deleted_reservations:
            self.reservations_repository.delete(deleted_reservation)

            room = self.room_repository.get(deleted_reservation.room_number)
            room.booked_intervals.remove((deleted_reservation.arrival_date, deleted_reservation.departure_date))

        return deleted_reservations_by_months

    def get_monthly_report(self, month: str):
        pass
