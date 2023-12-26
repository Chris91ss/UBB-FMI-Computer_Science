class Client:
    def __init__(self, client_id, name):
        self.id = client_id
        self.name = name

    def __str__(self):
        return f"Client: {self.id}, {self.name}"
