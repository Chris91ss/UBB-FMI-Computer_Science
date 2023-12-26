import unittest
from src.services.clientServices import ClientServices
from src.services.movieServices import MovieServices
from src.services.rentalServices import RentalServices


class Tests(unittest.TestCase):
    def setUp(self):
        self._client_services = ClientServices()
        self._movie_services = MovieServices()
        self._rental_services = RentalServices()

    def test_client_services(self):
        # test add client
        self._client_services.add_client(1, "John")
        self.assertEqual(len(self._client_services.get_all_clients()), 21)
        self._client_services.add_client(2, "Mark")
        self.assertEqual(len(self._client_services.get_all_clients()), 22)
        self._client_services.add_client(3, "Luke")
        self.assertEqual(len(self._client_services.get_all_clients()), 23)
        self._client_services.add_client(4, "Matthew")
        self.assertEqual(len(self._client_services.get_all_clients()), 24)
        self._client_services.add_client(5, "James")
        self.assertEqual(len(self._client_services.get_all_clients()), 25)

        # test remove client
        self._client_services.remove_client(1)
        self.assertEqual(len(self._client_services.get_all_clients()), 24)
        self._client_services.remove_client(2)
        self.assertEqual(len(self._client_services.get_all_clients()), 23)
        self._client_services.remove_client(3)
        self.assertEqual(len(self._client_services.get_all_clients()), 22)
        self._client_services.remove_client(4)
        self.assertEqual(len(self._client_services.get_all_clients()), 21)
        self._client_services.remove_client(5)
        self.assertEqual(len(self._client_services.get_all_clients()), 20)

        # test update client
        self._client_services.add_client(1, "John")
        self._client_services.update_client(1, "Chris")
        self.assertEqual(len(self._client_services.get_all_clients()), 21)
        self._client_services.update_client(1, "Mark")
        self.assertEqual(len(self._client_services.get_all_clients()), 21)
        self._client_services.update_client(1, "Luke")
        self.assertEqual(len(self._client_services.get_all_clients()), 21)
        self._client_services.add_client(2, "John")
        self._client_services.update_client(2, "Matthew")
        self.assertEqual(len(self._client_services.get_all_clients()), 22)
        self._client_services.update_client(2, "James")
        self.assertEqual(len(self._client_services.get_all_clients()), 22)

        # test search client by id
        self._client_services.add_client(235, "John")
        self._client_services.add_client(2350, "Mark")
        clients = self._client_services.search_client_by_id(235)
        self.assertEqual(len(clients), 2)

        # test search client by name
        self._client_services.add_client(5001, "Gojo")
        self._client_services.add_client(5002, "Gojira")
        clients = self._client_services.search_client_by_name("Goj")
        self.assertEqual(len(clients), 2)

    def test_movie_services(self):
        # test add movie
        self._movie_services.add_movie(1, "The Godfather", "The aging patriarch of an organized crime dynasty",
                                       "Crime")
        self.assertEqual(len(self._movie_services.get_all_movies()), 21)
        self._movie_services.add_movie(2, "The Dark Knight", "Batman, Gordon and Harvey Dent deal with the chaos",
                                       "Action")
        self.assertEqual(len(self._movie_services.get_all_movies()), 22)

        # test remove movie
        self._movie_services.remove_movie(1)
        self.assertEqual(len(self._movie_services.get_all_movies()), 21)
        self._movie_services.remove_movie(2)
        self.assertEqual(len(self._movie_services.get_all_movies()), 20)

        # test update movie
        self._movie_services.add_movie(1, "The Godfather", "The aging patriarch of an organized crime dynasty",
                                       "Crime")
        self._movie_services.update_movie(1, "The Dark Knight", "Batman, Gordon and Harvey Dent deal with the chaos",
                                          "Action")
        self.assertEqual(len(self._movie_services.get_all_movies()), 21)

        # test search movie by id
        self._movie_services.add_movie(235, "The Godfather", "The aging patriarch of an organized crime dynasty",
                                       "Crime")
        self._movie_services.add_movie(2350, "The Dark Knight", "Batman, Gordon and Harvey Dent deal with the chaos",
                                       "Action")
        movies = self._movie_services.search_movie_by_id(235)
        self.assertEqual(len(movies), 2)

        # test search movie by title
        self._movie_services.add_movie(7001, "EVIL leader", "A hero fights the evil leader", "Unusual")
        self._movie_services.add_movie(7002, "EVIL world", "A hero fights the evil", "Unusual")
        movies = self._movie_services.search_movie_by_title("EVIL")
        self.assertEqual(len(movies), 2)

        # test search movie by description
        movies = self._movie_services.search_movie_by_description("A hero fights the evil")
        self.assertEqual(len(movies), 2)

        # test search movie by genre
        movies = self._movie_services.search_movie_by_genre("Unusual")
        self.assertEqual(len(movies), 2)

    def test_rental_services(self):
        # test rent a movie
        self._rental_services.rent_a_movie(1, 1, 1, "2023 10 11", "2023 11 11", "2023 13 11")
        self.assertEqual(len(self._rental_services.get_all_rentals()), 21)
        self._rental_services.rent_a_movie(2, 2, 2, "2023 10 11", "2023 11 11", "2023 13 11")
        self.assertEqual(len(self._rental_services.get_all_rentals()), 22)

        # test return a movie
        self._rental_services.return_a_movie(1, 1, 1, "2023 10 11", "2023 11 11", "2023 13 11")
        self.assertEqual(len(self._rental_services.get_all_rentals()), 22)
        self._rental_services.return_a_movie(2, 2, 2, "2023 10 11", "2023 11 11", "2023 13 11")
        self.assertEqual(len(self._rental_services.get_all_rentals()), 22)

        # test most rented movies
        self.assertEqual(len(self._rental_services.most_rented_movies()), 22)


if __name__ == '__main__':
    unittest.main()
