from dataclasses import dataclass
from datetime import datetime


@dataclass
class Flight:
    id: str
    departure_city: str
    departure_time: datetime
    arrival_city: str
    arrival_time: datetime

    @property
    def duration_minutes(self):
        return (self.arrival_time - self.departure_time).total_seconds() // 60

    def __str__(self) -> str:
        departure_time = self.departure_time.strftime("%H:%M")
        arrival_time = self.arrival_time.strftime("%H:%M")
        return f"{self.id},{self.departure_city},{departure_time},{self.arrival_city},{arrival_time}"
