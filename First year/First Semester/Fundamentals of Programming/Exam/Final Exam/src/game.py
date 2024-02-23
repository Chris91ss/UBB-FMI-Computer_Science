import random
from src.exceptions import GameException


class Game:
    def __init__(self):
        self.year = 1
        self.people_starved = 0
        self.people_came = 0
        self.population = 100
        self.acres_of_land = 1000
        self.harvest_rate = 3
        self.rats_ate = 200
        self.land_price = 20
        self.grain_stock = 2800
        self.acres_planted = 0

    def advance_to_the_next_year(self, acres_to_buy_or_sell, units_to_feed_population, acres_to_plant):
        """
        This method advances the game to the next year. By following the Hammurabi game rules.
        :param acres_to_buy_or_sell: the number of acres the Hammurabi decides buy or sell
        :param units_to_feed_population: the number of units the Hammurabi decides to feed the population
        :param acres_to_plant: the number of acres the Hammurabi decides to plant
        :return: The game state, either a game over state because the people starved or a "continue advancing
        the years" state, until the 5 years are done
        """
        self.validator_for_decision(acres_to_buy_or_sell, units_to_feed_population, acres_to_plant)

        self.sell_or_buy_acres(acres_to_buy_or_sell)

        people_fed = units_to_feed_population // 20
        if people_fed > self.population:
            self.population = people_fed
        self.grain_stock -= units_to_feed_population
        if people_fed < self.population // 2:
            return "Game over. People Starved :("
        self.people_starved = self.population - people_fed
        if self.people_starved == 0:
            self.people_came = random.randint(0, 10)
        else:
            self.people_came = 0

        self.population = self.population - self.people_starved + self.people_came

        self.grain_stock -= acres_to_plant
        self.acres_planted = acres_to_plant

        self.land_price = random.randint(15, 25)
        self.harvest_rate = random.randint(1, 6)

        self.grain_stock += self.acres_planted * self.harvest_rate

        self.rats_infestation()

        self.year += 1

        if self.year == 5:
            return "Game Over."

        return "Continue advancing years."

    def sell_or_buy_acres(self, acres_to_buy_or_sell):
        """
        Function that updates the acres of land after the Hammurabi either sold or bought land, and updates the
        grain stock accordingly
        :param acres_to_buy_or_sell: the number of acres the Hammurabi decides buy or sell
        """
        self.acres_of_land += acres_to_buy_or_sell
        self.grain_stock -= acres_to_buy_or_sell * self.land_price

    def rats_infestation(self):
        rats_chance = random.randint(1, 5)
        if rats_chance == 1:
            rats_percentage_ate = random.randint(0, 10)
            self.rats_ate = rats_percentage_ate // 100 * self.grain_stock
            self.grain_stock -= self.rats_ate
        else:
            self.rats_ate = 0

    def validator_for_decision(self, acres_to_buy_or_sell, units_to_feed_population, acres_to_plant):
        """
        Function that validates the user input, raising exceptions depending on the conditions and rules of Hammurabi
        :param acres_to_buy_or_sell: the number of acres the Hammurabi decides buy or sell
        :param units_to_feed_population: the number of units the Hammurabi decides to feed the population
        :param acres_to_plant: the number of acres the Hammurabi decides to plant
        """
        total_grains = acres_to_buy_or_sell * self.land_price + units_to_feed_population + acres_to_plant

        if self.grain_stock - total_grains < 0:
            raise GameException("You can't buy more land than you have grain for.")

        if self.acres_of_land + acres_to_buy_or_sell < 0:
            raise GameException("You cannot sell more land than you have.")

        if units_to_feed_population > self.grain_stock:
            raise GameException("You cannot feed people with grain that you don't have.")

        if self.grain_stock < acres_to_plant:
            raise GameException("You cannot plant grain that you do not have")

        if self.population * 10 < acres_to_plant:
            raise GameException("You don't have enough people to plant that much, each person can plant at most 10 grain.")

        if self.acres_of_land + acres_to_buy_or_sell < acres_to_plant:
            raise GameException("You cannot plant more acres than you have.")

