class GeneralRepository:

    def __init__(self):
        self.all_data = {}

    def add(self, data):
        self.all_data[data.id] = data

    def delete(self, data):
        del self.all_data[data.id]

    def delete_by_id(self, data_id: int):
        del self.all_data[data_id]

    def get(self, data_id: int):
        return self.all_data[data_id]

    def get_all(self) -> list:
        return list(self.all_data.values())

    def get_all_ids(self) -> list[int]:
        return list(self.all_data.keys())
