class WolfGoatCabbageVertex:

    """
    A vertex in the WofGoatCabbageGraph.

    It is represented by a 4 bit number.
    Each bit represents either the boat, the wolf, the goat or the cabbage and its value
    represents the side it is on (0 for the left side, 1 for the right side).

    The wolf is bit 0, the goat is bit 1, the cabbage is bit 2 and the boat is bit 3.
    """

    def __init__(self, state: int):
        self.__state = state

    @property
    def valid(self):
        """
        Checks if the vertex is valid.
        A vertex is valid [if the boat is on the same side as the goat] or
        [(if the boat isn't on the same side as the wolf) and (the goat isn't on the same side as the cabbage)]
        We got to this form by applying De Morgan's laws to the original form.

        :return: True if the vertex is valid, False otherwise.
        """

        return self.__on_same_side(1, 3) or (not self.__on_same_side(0, 1) and not self.__on_same_side(1, 2))

    def get_neighbors(self):
        """
        Gets the neighbors of the vertex in the WolfGoatCabbageGraph.

        :return: a generator that yields the neighbors of the vertex.
        """

        for i in range(4):
            vertex = WolfGoatCabbageVertex(self.__state ^ ((1 << i) | 8))
            if vertex.valid and self.__on_same_side(i, 3):
                yield vertex

    def __on_same_side(self, index1: int, index2: int):
        """
        Checks if two items are on the same side of the river.

        :param index1: The index of the first item.
        :param index2: The index of the second item.

        :return: True if the items are on the same side, False otherwise.
        """

        return ((self.__state >> index1) & 1) == ((self.__state >> index2) & 1)

    def __hash__(self):
        return self.__state

    def __eq__(self, other):
        if not isinstance(other, WolfGoatCabbageVertex):
            return False
        if other.__state == self.__state:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Gets a string representation of the vertex.
        For example, the vertex 0000 would be represented as "WGCB - ".
        It means that all the items are on the left side of the river.

        :return: string representation of the vertex.
        """

        left_side, right_side = "", ""

        for i in range(4):
            if self.__state & (1 << i):
                right_side += "WGCB"[i]
            else:
                left_side += "WGCB"[i]

        return left_side + " - " + right_side
