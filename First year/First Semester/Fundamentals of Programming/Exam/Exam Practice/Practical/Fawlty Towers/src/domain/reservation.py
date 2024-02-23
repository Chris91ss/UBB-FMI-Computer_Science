from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reservation:

    id: int
    room_number: str
    name: str
    number_of_guests: int
    arrival_date: datetime
    departure_date: datetime

    MONTHS = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
              7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

    @property
    def arrival_month(self) -> str:
        month = int(self.arrival_date.strftime("%m"))
        return Reservation.MONTHS[month]

    @property
    def departure_month(self) -> str:
        month = int(self.departure_date.strftime("%m"))
        return Reservation.MONTHS[month]
