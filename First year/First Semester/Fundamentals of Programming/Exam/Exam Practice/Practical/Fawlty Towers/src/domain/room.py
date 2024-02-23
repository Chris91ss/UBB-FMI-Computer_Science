class Room:

    TYPES = {"single": 1, "double": 2, "family": 4}

    def __init__(self, room_id: str, room_type: str):
        self.id = room_id
        self.type = room_type

        self.capacity = Room.TYPES[room_type]
        self.booked_intervals = []
