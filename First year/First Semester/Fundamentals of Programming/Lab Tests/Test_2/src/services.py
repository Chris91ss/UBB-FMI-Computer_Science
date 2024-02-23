class Services:
    def __init__(self, provided_repository):
        self.repository = provided_repository

    def add(self, entity):
        self.repository.add(entity)

    def get_all(self):
        return self.repository.get_all()

    def remove(self, _id):
        self.repository.remove(_id)

    def update(self, entity):
        self.repository.update(entity)


