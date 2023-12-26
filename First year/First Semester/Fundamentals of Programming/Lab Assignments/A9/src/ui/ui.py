from src.services.clientServices import ClientServices
from src.services.movieServices import MovieServices
from src.services.rentalServices import RentalServices
from src.repository.repositoryException import RepositoryException


class UI:
    def __init__(self, provided_repository):
        self._client_repository = provided_repository.client_repository
        self._rental_repository = provided_repository.rental_repository
        self._movie_repository = provided_repository.movie_repository
        self._client_services = ClientServices(self._client_repository, self._rental_repository)
        self._movie_services = MovieServices(self._movie_repository)
        self._rental_services = RentalServices(self._rental_repository)

        self._client_services.clear_stacks()
        self._movie_services.clear_stacks()
        self._rental_services.clear_stacks()

    @staticmethod
    def print_menu():
        print("=====================================================================")
        print("1. Manage clients and movies")
        print("2. Rent or return a movie")
        print("3. Search for clients or movies")
        print("4. Show statistics")
        print("5. Undo")
        print("6. Redo")
        print("=====================================================================")

    def run(self):
        while True:
            self.print_menu()
            manage_clients_and_movies_option = "1"
            rent_or_return_a_movie_option = "2"
            search_for_clients_or_movies_option = "3"
            show_statistics_option = "4"
            undo_option = "5"
            redo_option = "6"
            command_input = input("Enter a command: ")
            if command_input == manage_clients_and_movies_option:
                print("=====================================================================")
                print("1. Manage clients")
                print("2. Manage movies")
                print("=====================================================================")
                command_input = input("Enter a command: ")
                manage_clients_option = "1"
                manage_movies_option = "2"
                if command_input == manage_clients_option:
                    self.manage_clients()
                if command_input == manage_movies_option:
                    self.manage_movies()
            elif command_input == rent_or_return_a_movie_option:
                print("=====================================================================")
                print("1. Rent a movie")
                print("2. Return a movie")
                print("=====================================================================")
                command_input = input("Enter a command: ")
                rent_a_movie_option = "1"
                return_a_movie_option = "2"
                if command_input == rent_a_movie_option:
                    self.rent_movie()
                elif command_input == return_a_movie_option:
                    self.return_movie()
                else:
                    print("Invalid command!")
            elif command_input == search_for_clients_or_movies_option:
                print("=====================================================================")
                print("1. Search for clients")
                print("2. Search for movies")
                print("=====================================================================")
                command_input = input("Enter a command: ")
                search_for_clients_option = "1"
                search_for_movies_option = "2"
                if command_input == search_for_clients_option:
                    print("=====================================================================")
                    print("1. Search by ID")
                    print("2. Search by name")
                    print("=====================================================================")
                    command_input = input("Enter a command: ")
                    search_by_id_option = "1"
                    search_by_name_option = "2"
                    if command_input == search_by_id_option:
                        self.search_client_by_id()
                    if command_input == search_by_name_option:
                        self.search_client_by_name()
                    else:
                        print("Invalid command!")
                elif command_input == search_for_movies_option:
                    print("=====================================================================")
                    print("1. Search by ID")
                    print("2. Search by title")
                    print("3. Search by description")
                    print("4. Search by genre")
                    print("=====================================================================")
                    command_input = input("Enter a command: ")
                    search_by_id_option = "1"
                    search_by_title_option = "2"
                    search_by_description_option = "3"
                    search_by_genre_option = "4"
                    if command_input == search_by_id_option:
                        self.search_movie_by_id()
                    elif command_input == search_by_title_option:
                        self.search_movie_by_title()
                    elif command_input == search_by_description_option:
                        self.search_movie_by_description()
                    elif command_input == search_by_genre_option:
                        self.search_movie_by_genre()
                    else:
                        print("Invalid command!")
                else:
                    print("Invalid command!")
            elif command_input == show_statistics_option:
                print("=====================================================================")
                print("1. Most rented movies")
                print("2. Most active clients")
                print("3. Late rentals")
                print("=====================================================================")
                command_input = input("Enter a command: ")
                most_rented_movies_option = "1"
                most_active_clients_option = "2"
                late_rentals_option = "3"
                if command_input == most_rented_movies_option:
                    self.most_rented_movies()
                elif command_input == most_active_clients_option:
                    self.most_active_clients()
                elif command_input == late_rentals_option:
                    self.late_rentals()
            elif command_input == undo_option:
                self.undo()
            elif command_input == redo_option:
                self.redo()
            elif command_input == "7":
                rentals = self._rental_services.get_all_rentals()
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
        add_client_option = "1"
        remove_client_option = "2"
        update_client_option = "3"
        list_all_clients_option = "4"
        if command_input == add_client_option:
            client_id = input("Enter client ID: ")
            client_name = input("Enter client name: ")
            self._client_services.add_client(client_id, client_name)
        elif command_input == remove_client_option:
            client_id = input("Enter client ID: ")
            self._client_services.remove_client(client_id)
        elif command_input == update_client_option:
            client_id = input("Enter client ID: ")
            client_name = input("Enter client name: ")
            self._client_services.update_client(client_id, client_name)
        elif command_input == list_all_clients_option:
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
        add_movie_option = "1"
        remove_movie_option = "2"
        update_movie_option = "3"
        list_all_movies_option = "4"
        if command_input == add_movie_option:
            movie_id = input("Enter movie ID: ")
            movie_title = input("Enter movie title: ")
            movie_description = input("Enter movie description: ")
            movie_genre = input("Enter movie genre: ")
            self._movie_services.add_movie(movie_id, movie_title, movie_description, movie_genre)
        elif command_input == remove_movie_option:
            movie_id = input("Enter movie ID: ")
            self._movie_services.remove_movie(movie_id)
        elif command_input == update_movie_option:
            movie_id = input("Enter movie ID: ")
            movie_title = input("Enter movie title: ")
            movie_description = input("Enter movie description: ")
            movie_genre = input("Enter movie genre: ")
            self._movie_services.update_movie(movie_id, movie_title, movie_description, movie_genre)
        elif command_input == list_all_movies_option:
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

    def search_client_by_id(self):
        client_id = input("Enter client ID: ")
        clients = self._client_services.search_client_by_id(client_id)
        for client in clients:
            print(client)

    def search_client_by_name(self):
        client_name = input("Enter client name: ")
        clients = self._client_services.search_client_by_name(client_name)
        for client in clients:
            print(client)

    def search_movie_by_id(self):
        movie_id = input("Enter movie ID: ")
        movies = self._movie_services.search_movie_by_id(movie_id)
        for movie in movies:
            print(movie)

    def search_movie_by_title(self):
        movie_title = input("Enter movie title: ")
        movies = self._movie_services.search_movie_by_title(movie_title)
        for movie in movies:
            print(movie)

    def search_movie_by_description(self):
        movie_description = input("Enter movie description: ")
        movies = self._movie_services.search_movie_by_description(movie_description)
        for movie in movies:
            print(movie)

    def search_movie_by_genre(self):
        movie_genre = input("Enter movie genre: ")
        movies = self._movie_services.search_movie_by_genre(movie_genre)
        for movie in movies:
            print(movie)

    def most_rented_movies(self):
        rentals = self._rental_services.most_rented_movies()
        movies = self._movie_services.get_all_movies()
        for rental in rentals:
            for movie in movies:
                if rental.movie_id == movie.id:
                    print(movie)

    def most_active_clients(self):
        clients = self._client_services.most_active_clients()
        for client in clients:
            print(client)

    def late_rentals(self):
        rentals = self._rental_services.late_rentals()
        for rental in rentals:
            print(rental)

    def undo(self):
        print("=====================================================================")
        print("1. Undo for clients")
        print("2. Undo for movies")
        print("3. Undo for rentals")
        print("=====================================================================")
        command_input = input("Enter a command: ")
        undo_for_clients_option = "1"
        undo_for_movies_option = "2"
        undo_for_rentals_option = "3"
        if command_input == undo_for_clients_option:
            self._client_services.undo()
        elif command_input == undo_for_movies_option:
            self._movie_services.undo()
        elif command_input == undo_for_rentals_option:
            self._rental_services.undo()
        else:
            print("Invalid command!")

    def redo(self):
        print("=====================================================================")
        print("1. Redo for clients")
        print("2. Redo for movies")
        print("3. Redo for rentals")
        print("=====================================================================")
        command_input = input("Enter a command: ")
        redo_for_clients_option = "1"
        redo_for_movies_option = "2"
        redo_for_rentals_option = "3"
        if command_input == redo_for_clients_option:
            self._client_services.redo()
        elif command_input == redo_for_movies_option:
            self._movie_services.redo()
        elif command_input == redo_for_rentals_option:
            self._rental_services.redo()
        else:
            print("Invalid command!")
