from src.repository.repository import Repository
from src.domain.rental import Rental
from src.repository.repositoryException import RepositoryException
from random import randint


class RentalServices:
    def __init__(self, provide_rental_repository):
        self._repository = provide_rental_repository
        self.generate_random_rentals()

    def generate_random_rentals(self):
        number_of_rentals = 20
        list_of_rented_dates = ["2023 10 11", "2023 11 11", "2023 12 11", "2023 13 11", "2023 14 11", "2023 15 11"]
        list_of_due_dates = ["2023 23 11", "2023 24 11", "2023 25 11", "2023 26 11", "2023 27 11", "2023 28 11"]
        list_of_returned_dates = ["2023 27 11", "2023 28 11", "2023 29 11", "2023 30 11"]
        for i in range(number_of_rentals):
            try:
                self.rent_a_movie(randint(501, 750), randint(251, 500), randint(1, 250),
                                  list_of_rented_dates[randint(0, 4)],
                                  list_of_due_dates[randint(0, 5)],
                                  list_of_returned_dates[randint(0, 3)])
            except RepositoryException as ex:
                print(ex)

    def check_if_client_can_rent(self, client_id):
        rentals = self._repository.get_all()
        for rental in rentals:
            if rental.returned_date is not None:
                if rental.client_id == client_id and (rental.returned_date[0] > rental.due_date[0] or
                                                      rental.returned_date[1] > rental.due_date[1] or
                                                      rental.returned_date[2] > rental.due_date[2]):
                    return False
        return True

    def rent_a_movie(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date):
        if not self.check_if_client_can_rent(client_id):
            raise RepositoryException("Client with ID: " + str(client_id) + " cannot rent another movie")
        rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
        self._repository.add(rental)

    def return_a_movie(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date):
        rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
        self._repository.update(rental)

    def most_rented_movies(self):
        rental_dictionary = self._repository.get_data_dictionary()
        sorted_movies = sorted(rental_dictionary.values(), key=lambda x: int(x.due_date.split()[1]) - int(x.rented_date.split()[1]),
                               reverse=True)

        return sorted_movies

    def late_rentals(self):
        rental_dictionary = self._repository.get_all()
        late_rentals = []

        for rental in rental_dictionary:
            returned_date = rental.returned_date.split()
            due_date = rental.due_date.split()
            if int(returned_date[1]) > int(due_date[1]):
                late_rentals.append(rental)

        return late_rentals

    def get_all_rentals(self):
        return self._repository.get_all()
