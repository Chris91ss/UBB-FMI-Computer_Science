class CoordinatesConverter:

    str_keys = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8}
    int_keys = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H"}

    @staticmethod
    def str_to_tuple(str_coordinates: str) -> tuple[int, int]:
        row, column = str_coordinates[0].upper(), int(str_coordinates[1])
        row = CoordinatesConverter.str_keys[row]

        return row, column

    @staticmethod
    def int_to_str(integer: int) -> str:
        return CoordinatesConverter.int_keys[integer]
