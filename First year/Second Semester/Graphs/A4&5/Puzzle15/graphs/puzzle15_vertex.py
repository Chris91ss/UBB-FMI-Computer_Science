from copy import copy

from texttable import Texttable


class Puzzle15Vertex:
    def __init__(self, state: list[int]):
        self.__state = state

    @property
    def state(self):
        return self.__state

    def __swap(self, line1, column1, line2, column2):
        new_state = copy(self.__state)
        new_state[line1 * 4 + column1], new_state[line2 * 4 + column2] =\
            new_state[line2 * 4 + column2], new_state[line1 * 4 + column1]
        return new_state

    def get_neighbors(self):
        for line in range(4):
            for column in range(4):
                if self.__state[line * 4 + column] == 0:
                    if line > 0:
                        yield Puzzle15Vertex(self.__swap(line, column, line - 1, column))
                    if line < 3:
                        yield Puzzle15Vertex(self.__swap(line, column, line + 1, column))
                    if column > 0:
                        yield Puzzle15Vertex(self.__swap(line, column, line, column - 1))
                    if column < 3:
                        yield Puzzle15Vertex(self.__swap(line, column, line, column + 1))
                    break

    def __hash__(self):
        hash_value = 0
        for line in range(4):
            for column in range(4):
                hash_value += self.__state[line * 4 + column] * (line * 4 + column)
        return hash_value

    def __eq__(self, other):
        if not isinstance(other, Puzzle15Vertex):
            return False
        return self.__state == other.__state

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.__state < other.__state

    def __le__(self, other):
        return self.__state <= other.__state

    def __gt__(self, other):
        return self.__state > other.__state

    def __ge__(self, other):
        return self.__state >= other.__state

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        table = Texttable()
        for line in range(4):
            added_line = self.__state[line * 4: line * 4 + 4].copy()
            added_line = [str(x) if x != 0 else ' ' for x in added_line]
            table.add_row(added_line)

        return table.draw()
