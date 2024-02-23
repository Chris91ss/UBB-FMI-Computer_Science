from dataclasses import dataclass


@dataclass
class Cell:
    row: int
    column: int
    occupied: bool = False
    resident: str = ""
    near_endeavour: bool = False

    def occupy(self, resident: str):
        self.occupied = True
        self.resident = resident

    def deoccupy(self):
        self.occupied = False
        self.resident = ""
