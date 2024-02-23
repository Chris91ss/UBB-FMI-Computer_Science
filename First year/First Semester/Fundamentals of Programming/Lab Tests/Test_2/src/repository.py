
class Repository:
    def __init__(self):
        self.data = {}

    def add(self, entity):
        self.data[entity.id] = entity

    def update(self, entity):
        self.data[entity.id] = entity

    def remove(self, _id):
        del self.data[_id]

    def get_all(self):
        return self.data.values()

