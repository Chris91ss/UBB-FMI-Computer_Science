from src.domain.client import Client
from src.repository.repositoryException import RepositoryException
from random import randint


class ClientServices:

    def __init__(self, provide_client_repository, provide_rental_repository):
        self.client_repository = provide_client_repository
        self.rental_repository = provide_rental_repository
        self.generate_random_clients()

    def generate_random_clients(self):
        client_list = ["John", "Mark", "Luke", "Matthew", "James", "Peter", "Paul", "Jude", "Simon", "Thomas",
                       "Andrew", "Philip", "Bartholomew", "Matthew", "James", "Thaddeus", "Simon", "Judas", "Matthias",
                       "Cleo", "Kratos"]
        number_of_clients = 20
        for i in range(number_of_clients):
            random_number = randint(10, 250)
            self.add_client(random_number, client_list[i])

    def add_client(self, client_id, client_name):
        client = Client(client_id, client_name)
        try:
            self.client_repository.add(client)
        except RepositoryException as ex:
            print(ex)

    def remove_client(self, client_id):
        try:
            self.client_repository.remove(client_id)
        except RepositoryException as ex:
            print(ex)

    def update_client(self, client_id, client_name):
        client = Client(client_id, client_name)
        self.client_repository.update(client)

    def undo(self):
        try:
            self.client_repository.undo()
        except RepositoryException as re:
            print(re)

    def redo(self):
        try:
            self.client_repository.redo()
        except RepositoryException as re:
            print(re)

    def get_all_clients(self):
        return self.client_repository.get_all()

    def clear_stacks(self):
        self.client_repository.clear_stacks()

    def search_client_by_id(self, client_id):
        return self.client_repository.search_by_id(client_id)

    def search_client_by_name(self, client_name):
        return self.client_repository.search_by_name(client_name)

    def most_active_clients(self):
        sorted_clients = []

        client_data = self.client_repository.get_all()
        rental_data = self.rental_repository.get_all()

        for client in client_data:
            rental_days = 0
            for rental in rental_data:
                if int(rental.client_id) == int(client.id) and rental.returned_date is not None:
                    returned_date = rental.returned_date.split()
                    rented_date = rental.rented_date.split()
                    rental_days += (int(returned_date[1]) - int(rented_date[1]))
            if rental_days != 0:
                sorted_clients.append((client.id, client.name, rental_days))

        sorted_clients.sort(key=lambda x: x[2], reverse=True)

        return sorted_clients
