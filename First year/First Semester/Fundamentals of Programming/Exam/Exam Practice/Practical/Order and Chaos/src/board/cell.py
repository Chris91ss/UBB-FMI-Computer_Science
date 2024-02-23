from dataclasses import dataclass


@dataclass
class Cell:

    row: int
    column: int
    occupied: bool = False
    __symbol: str = " "

    @property
    def symbol(self) -> str:
        return self.__symbol

    @symbol.setter
    def symbol(self, new_symbol: str):
        self.__symbol = new_symbol
        self.occupied = True

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.row, self.column
