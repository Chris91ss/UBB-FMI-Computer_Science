from src.services.clientServices import ClientServices
from src.services.movieServices import MovieServices
from src.services.rentalServices import RentalServices
from src.repository.repositoryException import RepositoryException
from src.repository.repository import Repository

class UI:
    def __init__(self):
        self._client_repository = Repository()
        self._rental_repository = Repository()
        self._movie_repository = Repository()
        self._client_services = ClientServices(self._client_repository, self._rental_repository)
        self._movie_services = MovieServices(self._movie_repository)
        self._rental_services = RentalServices(self._rental_repository)

    @staticmethod
    def print_menu():
        print("=====================================================================")
        print("1. Manage clients and movies")
        print("2. Rent or return a movie")
        print("3. Search for clients or movies")
        print("4. Show statistics")
        print("=====================================================================")

    def run(self):
        while True:
            self.print_menu()
            command_input = input("Enter a command: ")
            if command_input == "1":
                print("=====================================================================")
                print("1. Manage clients")
                print("2. Manage movies")
                print("=====================================================================")
                command_input = input("Enter a command: ")
                if command_input == "1":
                    self.manage_clients()
                if command_input == "2":
                    self.manage_movies()
            elif command_input == "2":
                print("=====================================================================")
                print("1. Rent a movie")
                print("2. Return a movie")
                print("=====================================================================")
                command_input = input("Enter a command: ")
                if command_input == "1":
                    self.rent_movie()
                elif command_input == "2":
                    self.return_movie()
                else:
                    print("Invalid command!")
            elif command_input == "3":
                print("=====================================================================")
                print("1. Search for clients")
                print("2. Search for movies")
                print("=====================================================================")
                command_input = input("Enter a command: ")
                if command_input == "1":
                    print("=====================================================================")
                    print("1. Search by ID")
                    print("2. Search by name")
                    print("=====================================================================")
                    command_input = input("Enter a command: ")
                    if command_input == "1":
                        client_id = input("Enter client ID: ")
                        clients = self._client_services.search_client_by_id(client_id)
                        for client in clients:
                            print(client)
                    if command_input == "2":
                        client_name = input("Enter client name: ")
                        clients = self._client_services.search_client_by_name(client_name)
                        for client in clients:
                            print(client)
                    else:
                        print("Invalid command!")
                elif command_input == "2":
                    print("=====================================================================")
                    print("1. Search by ID")
                    print("2. Search by title")
                    print("3. Search by description")
                    print("4. Search by genre")
                    print("=====================================================================")
                    command_input = input("Enter a command: ")
                    if command_input == "1":
                        movie_id = input("Enter movie ID: ")
                        movies = self._movie_services.search_movie_by_id(movie_id)
                        for movie in movies:
                            print(movie)
                    elif command_input == "2":
                        movie_title = input("Enter movie title: ")
                        movies = self._movie_services.search_movie_by_title(movie_title)
                        for movie in movies:
                            print(movie)
                    elif command_input == "3":
                        movie_description = input("Enter movie description: ")
                        movies = self._movie_services.search_movie_by_description(movie_description)
                        for movie in movies:
                            print(movie)
                    elif command_input == "4":
                        movie_genre = input("Enter movie genre: ")
                        movies = self._movie_services.search_movie_by_genre(movie_genre)
                        for movie in movies:
                            print(movie)
                    else:
                        print("Invalid command!")
                else:
                    print("Invalid command!")
            elif command_input == "4":
                print("=====================================================================")
                print("1. Most rented movies")
                print("2. Most active clients")
                print("3. Late rentals")
                print("=====================================================================")
                command_input = input("Enter a command: ")
                if command_input == "1":
                    rentals = self._rental_services.most_rented_movies()
                    movies = self._movie_services.get_all_movies()
                    for rental in rentals:
                        for movie in movies:
                            if rental.movie_id == movie.id:
                                print(movie)
                elif command_input == "2":
                    clients = self._client_services.most_active_clients()
                    for client in clients:
                        print(client)
                elif command_input == "3":
                    rentals = self._rental_services.late_rentals()
                    for rental in rentals:
                        print(rental)
            else:
                print("Invalid command!")

    def manage_clients(self):
        print("=====================================================================")
        print("1. Add a client")
        print("2. Remove a client")
        print("3. Update a client")
        print("4. List all clients")
        print("=====================================================================")
        command_input = input("Enter a command: ")
        if command_input == "1":
            client_id = input("Enter client ID: ")
            client_name = input("Enter client name: ")
            self._client_services.add_client(client_id, client_name)
        elif command_input == "2":
            client_id = input("Enter client ID: ")
            self._client_services.remove_client(client_id)
        elif command_input == "3":
            client_id = input("Enter client ID: ")
            client_name = input("Enter client name: ")
            self._client_services.update_client(client_id, client_name)
        elif command_input == "4":
            clients = self._client_services.get_all_clients()
            for client in clients:
                print(client)
        else:
            print("Invalid command!")

    def manage_movies(self):
        print("=====================================================================")
        print("1. Add a movie")
        print("2. Remove a movie")
        print("3. Update a movie")
        print("4. List all movies")
        print("=====================================================================")
        command_input = input("Enter a command: ")
        if command_input == "1":
            movie_id = input("Enter movie ID: ")
            movie_title = input("Enter movie title: ")
            movie_description = input("Enter movie description: ")
            movie_genre = input("Enter movie genre: ")
            self._movie_services.add_movie(movie_id, movie_title, movie_description, movie_genre)
        elif command_input == "2":
            movie_id = input("Enter movie ID: ")
            self._movie_services.remove_movie(movie_id)
        elif command_input == "3":
            movie_id = input("Enter movie ID: ")
            movie_title = input("Enter movie title: ")
            movie_description = input("Enter movie description: ")
            movie_genre = input("Enter movie genre: ")
            self._movie_services.update_movie(movie_id, movie_title, movie_description, movie_genre)
        elif command_input == "4":
            movies = self._movie_services.get_all_movies()
            for movie in movies:
                print(movie)
        else:
            print("Invalid command!")

    def rent_movie(self):
        rental_id = input("Enter rental ID: ")
        movie_id = input("Enter movie ID: ")
        client_id = input("Enter client ID: ")
        rented_date = input("Enter rented date: ")
        due_date = input("Enter due date: ")

        try:
            self._rental_services.rent_a_movie(rental_id, movie_id, client_id, rented_date, due_date, None)
        except RepositoryException as ex:
            print(ex)

    def return_movie(self):
        rental_id = input("Enter rental ID: ")
        movie_id = input("Enter movie ID: ")
        client_id = input("Enter client ID: ")
        rented_date = input("Enter rented date: ")
        due_date = input("Enter due date: ")
        returned_date = input("Enter returned date: ")

        self._rental_services.return_a_movie(rental_id, movie_id, client_id, rented_date, due_date, returned_date)


