class GeneralRepository:

    def __init__(self):
        self.all_data = {}

    def add(self, data):
        self.all_data[data.id] = data

    def delete(self, data):
        del self.all_data[data.id]

    def delete_by_id(self, data_id):
        del self.all_data[data_id]

    def get(self, data_id):
        return self.all_data[data_id]

    def get_all(self) -> list:
        return list(self.all_data.values())

    def get_ids(self) -> list:
        return list(self.all_data.keys())
