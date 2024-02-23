class GenericRepository:

    def __init__(self):
        self.__all_data = {}

    # -------------------- #
    # -------------------- #
    # -------------------- #

    def add(self, data):
        self.__all_data[data.id] = data

    def remove(self, data):
        del self.__all_data[data.id]

    def remove_by_id(self, data_id: str):
        del self.__all_data[data_id]

    # -------------------- #
    # -------------------- #
    # -------------------- #

    def get_by_id(self, data_id: str):
        return self.__all_data[data_id]

    def get_all(self) -> list:
        return list(self.__all_data.values())

    def get_all_ids(self) -> list:
        return list(self.__all_data.keys())
