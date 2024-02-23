from unittest import TestCase
from src.ui import UI
from src.game import Game


class Tests(TestCase):
    def setUp(self):
        self.game = Game()
        self.ui = UI(self.game)

    def test_sell_or_buy_acres(self):
        """
        tests the sell or buy acres function, checking if the acres of land was updating after the Hammurabi
        bought or sold land
        """
        self.game.sell_or_buy_acres(-100)
        self.assertEqual(self.game.acres_of_land, 900)
        self.game.sell_or_buy_acres(100)
        self.assertEqual(self.game.acres_of_land, 1000)
        self.game.sell_or_buy_acres(-500)
        self.assertEqual(self.game.acres_of_land, 500)
        self.game.sell_or_buy_acres(200)
        self.assertEqual(self.game.acres_of_land, 700)
        self.game.sell_or_buy_acres(-600)
        self.assertEqual(self.game.acres_of_land, 100)
        self.game.sell_or_buy_acres(1500)
        self.assertEqual(self.game.acres_of_land, 1600)
        self.game.sell_or_buy_acres(-600)
        self.assertNotEqual(self.game.acres_of_land, 1200)

    def test_advancing_to_the_next_year(self):
        """
        tests the advancing to the next year function, testing the data reported by the trusted advisor for each year
        """
        game_status = self.game.advance_to_the_next_year(-100, 2000, 800)
        self.assertEqual(game_status, "Continue advancing years.")
        self.assertEqual(self.game.year, 2)
        self.assertEqual(self.game.year, 2)
        self.assertEqual(self.game.people_starved, 0)
        self.assertEqual(self.game.acres_of_land, 900)
        self.game.population = 100
        game_status = self.game.advance_to_the_next_year(-100, 1000, 0)
        self.assertEqual(game_status, "Continue advancing years.")
        self.assertEqual(self.game.year, 3)
        self.assertEqual(self.game.acres_of_land, 800)
        self.assertEqual(self.game.people_came, 0)
        self.assertEqual(self.game.people_starved, 50)
        self.assertEqual(self.game.population, 50)
        game_status = self.game.advance_to_the_next_year(20, 980, 500)
        self.assertEqual(game_status, "Continue advancing years.")
        self.assertEqual(self.game.year, 4)
        self.assertEqual(self.game.acres_of_land, 820)
        self.assertEqual(self.game.people_came, 0)
        self.assertEqual(self.game.people_starved, 1)
        self.assertEqual(self.game.population, 49)
        game_status = self.game.advance_to_the_next_year(-20, 1500, 250)
        self.assertEqual(self.game.year, 5)
        self.assertEqual(self.game.acres_of_land, 800)
        self.assertNotEqual(self.game.people_came, 0)
        self.assertEqual(self.game.people_starved, 0)
        self.assertNotEqual(self.game.population, 49)
        self.assertEqual(game_status, "Game Over.")




