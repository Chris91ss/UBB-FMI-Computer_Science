import random

from src.exceptions import GameError


class Game:

    def __init__(self):
        self.year = 1
        self.grains = 2800

        self.people_starved = 0
        self.people_came = 0
        self.population = 100

        self.acres = 1000
        self.acres_planted = 0
        self.yield_rate = 3
        self.land_price = 20

        self.rats = 200

    def advance_year(self, acres_decision: int, feed_decision: int, plant_decision: int) -> str:
        """
        This function advances the year and implements the decisions taken be the Hammurabi.
        It also randomizes the random variables
        :param acres_decision: int, amount of acres to buy/sell
        :param feed_decision: int, amount of grain to feed the people
        :param plant_decision: int, amount of acres to plant
        :return: str, used to determine if the starved ending is achieved
                 "STARVED ENDING", if the starved ending is achieved
                 "CONTINUE", if the starved ending is not achieved
        """

        self.verify_decisions(acres_decision, feed_decision, plant_decision)

        # selling/buying land
        self.acres += acres_decision
        self.grains -= acres_decision * self.land_price

        # feeding the population
        people_fed = feed_decision // 20
        self.grains -= feed_decision
        if people_fed < self.population // 2:
            return "STARVE ENDING"

        self.people_starved = self.population - people_fed
        if self.people_starved == 0:
            self.people_came = random.randint(0, 10)

        self.population = self.population - self.people_starved + self.people_came

        # planting
        self.grains -= plant_decision
        self.acres_planted = plant_decision

        # randomize prices and yield
        self.land_price = random.randint(15, 25)
        self.yield_rate = random.randint(1, 6)

        # harvesting
        self.grains += self.acres_planted * self.yield_rate

        # rats
        rats_chance = random.randint(1, 5)  # 20% is one out of five
        if rats_chance == 1:
            percentage_ate = random.randint(0, 10)
            self.rats = percentage_ate // 100 * self.grains
            self.grains -= self.rats

        # advance year
        self.year += 1

        return "CONTINUE"

    def verify_decisions(self, acres_decision: int, feed_decision: int, plant_decision: int):
        total_grains_spend = acres_decision * self.land_price + feed_decision + plant_decision
        if self.grains - total_grains_spend < 0:
            raise GameError("you can not spend more grains than you own")

        if self.acres + acres_decision < 0:
            raise GameError("you can not sell more acres than you have")

        if self.population * 10 < plant_decision:
            raise GameError("you do not have enough people to plant all the acres")

        if self.acres + acres_decision < plant_decision:
            raise GameError("you do not have enough acres to plant")
