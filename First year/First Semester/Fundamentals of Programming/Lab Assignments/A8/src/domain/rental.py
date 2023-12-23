class Rental:
    def __init__(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date):
        self.id = rental_id
        self.movie_id = movie_id
        self.client_id = client_id
        self.rented_date = rented_date
        self.due_date = due_date
        self.returned_date = returned_date

    def __str__(self):
        return f"Rental: {self.id}, {self.movie_id}, {self.client_id}, {self.rented_date}, {self.due_date}, {self.returned_date}"
