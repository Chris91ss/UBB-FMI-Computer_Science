class GenericRepository:

    def __init__(self):
        self.all_data = {}

    def add(self, data):
        self.all_data[data.id] = data

    def get(self, data_id):
        return self.all_data[data_id]

    def get_all(self) -> list:
        return list(self.all_data.values())
