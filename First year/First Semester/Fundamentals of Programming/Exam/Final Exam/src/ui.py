

class UI:
    def __init__(self, game):
        self.game = game

    def start(self):
        UI.display_title_screen()
        while self.game.year < 5:
            self.print_report()
            try:
                acres_to_buy_or_sell, units_to_feed_population, acres_to_plant = UI.receive_input()
                game_status = self.game.advance_to_the_next_year(acres_to_buy_or_sell, units_to_feed_population, acres_to_plant)

                if game_status == "Game over. People Starved :(":
                    self.game_over(1)

            except Exception as exceptions:
                print(exceptions)

        self.game_over(0)

    def print_report(self):
        print(f"In year {self.game.year}, {self.game.people_starved} people starved.")
        print(f"{self.game.people_came} people came to the city.")
        print(f"City population is {self.game.population}")
        print(f"City owns {self.game.acres_of_land} acres of land.")
        print(f"Harvest was {self.game.harvest_rate} units per acre")
        print(f"Rats ate {self.game.rats_ate} units")
        print(f"Land price is {self.game.land_price} units per acre.")
        print(f"Grain stocks are {self.game.grain_stock} units")
        print("\n")

    @staticmethod
    def receive_input():
        acres_to_buy_or_sell = int(input("Acres to buy/sell (+/-) -> "))
        units_to_feed_population = int(input("Units to feed the population -> "))
        acres_to_plant = int(input("Acres to plant -> "))

        return acres_to_buy_or_sell, units_to_feed_population, acres_to_plant

    @staticmethod
    def display_title_screen():
        print("############################################################")
        print("#####               Welcome to Hammurabi              ######")
        print("## You have been elected for a five year term as ruler of ##")
        print("#-------------------     *SUMERIA*      -------------------#")
        print("############# GOOD LUCK MANAGING YOUR CAPITAL ##############")
        print("\n")

    def game_over(self, people_starved=0):
        if people_starved:
            print("Game over. People Starved :(. Next time remember to feed the population ^^")
        else:
            you_did_well_ending = False
            if self.game.population > 100 and self.game.grain_stock > 1000:
                you_did_well_ending = True

            if you_did_well_ending:
                print("Congratulations. You did well. Sumeria is happy to have you as the mighty Hammurabi")
            else:
                print("Game over. You did not do well :(")
                print("Try again")

        exit(1)
