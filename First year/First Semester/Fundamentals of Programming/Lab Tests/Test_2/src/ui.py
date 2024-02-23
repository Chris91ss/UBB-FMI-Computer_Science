from src.services import Services
from src.domain import Player
from random import randint

class UI:
    def __init__(self, provided_repository):
        self.service = Services(provided_repository)
        self.read_input_from_file()

    def read_input_from_file(self):
        with open("input.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                player_id = values[0]
                player_name = values[1]
                player_strength = values[2]

                player = Player(player_id, player_name, player_strength)
                self.service.add(player)

    @staticmethod
    def print_ui():
        print("1. Display all players from input file sorted in descending order by player strength")
        print("2. Play tournament")

    def start(self):
        while True:
            self.print_ui()
            display_players_choice = "1"
            play_tournament_choice = "2"
            command = input("Enter a choice: ")
            if command == display_players_choice:
                players = self.service.get_all()
                sorted_player = sorted(players, key=lambda x: x.playing_strength)
                for player in sorted_player:
                    print(player)
            if command == play_tournament_choice:
                self.qualifying_round()
                players = self.service.get_all()
                self.play_tournament()

    def play_tournament(self):
        while True:
            players = self.service.get_all()
            quarter_finals = 8
            semi_finals = 4
            finals = 2
            if len(players) == quarter_finals:
                print("Last 8 - quarter finals")
            elif len(players) == semi_finals:
                print("Last 4 - semi finals")
            elif len(players) == finals:
                print("Last 2 - finals")
            paired_players = self.randomly_pair_the_players(players)
            round_index = 1
            while True:
                print(f"Round {round_index}")
                for player in paired_players:
                    print("Chose a winner: ")
                    name = input("Enter winner name")
                    return

    def qualifying_round(self):
        players = self.service.get_all()
        powers_of_two = [1, 2, 4, 8]
        if len(players) in powers_of_two:
            return
        while len(players) not in powers_of_two:
            print("Qualifying round")
            pair_of_player = []
            sorted_player = sorted(players, key=lambda x: x.playing_strength)
            if len(sorted_player) not in powers_of_two:
                index = 0
                pair_of_player.append(sorted_player[index])
                print(sorted_player[index])
                index += 1
                pair_of_player.append(sorted_player[index])
                print(sorted_player[index])
                index += 1
                print("Chose a winner: ")
                name = input("Enter winner name")
                player_to_eliminate_id = 0
                for player in pair_of_player:
                    if name in player.name:
                        print(f"The winner is Player {player.name}")
                        break
                    player_to_eliminate_id = player.id

                self.service.remove(player_to_eliminate_id)

    @staticmethod
    def randomly_pair_the_players(players):
        players = list(players)
        length_of_players = len(players)
        pairs_of_players = []
        positions = []
        while length_of_players > 0:
            length_of_players -= 2
            index = randint(0, len(players) - 1)
            if index not in positions:
                positions.append(index)
                index2 = randint(0, len(players) - 1)
                if index2 not in positions:
                    positions.append(index2)
                    pairs_of_players.append((players[index], players[index2]))

        return pairs_of_players
