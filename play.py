#!/usr/bin/env python3

import argparse
import getpass
import os
from random import randint
from tabulate import tabulate

# Define global options
divider_length = 48

# Define the game symbols
SYMBOL_ROCK = "👊"  # \U0001F44A
SYMBOL_PAPER = "🤚"  # \U0001F91A
SYMBOL_SCISSORS = "✌️"  # \U0000270C


class RockPaperScissors(object):

    def __init__(self, divider_length):
        super(RockPaperScissors, self).__init__()
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.player_1 = ""
        self.player_1_name = "Player"
        self.player_2 = ""
        self.player_2_name = "Computer"
        self.round_is_draw = False
        self.player_1_wins = False
        self.score_path = "./score.txt"
        self.divider_length = divider_length

    def parse_args(self):
        """Define the script arguments"""
        parser = argparse.ArgumentParser(description="Play a game of Rock Paper Scissors!")
        parser.add_argument("-m", "--multiplayer", help="play the game with 2 players", action="store_true")
        parser.add_argument("-p", "--plaintext", help="play the game in plaintext mode", action="store_true")
        parser.add_argument("-s", "--score", help="display the total score against the computer", action="store_true")
        self.args = parser.parse_args()

    def attack_method(self, int):
        """Get the readable attack method name and symbol"""
        name = {
            1: "ROCK",
            2: "PAPER",
            3: "SCISSORS"
        }
        symbol = {
            1: SYMBOL_ROCK,
            2: SYMBOL_PAPER,
            3: SYMBOL_SCISSORS,
        }
        return name.get(int), symbol.get(int)

    def repeat_to_length(self, str, multiplier):
        """Repeat a string X times"""
        return str * multiplier

    def output_victor(self, message, max_length, flourish_symbol="*"):
        """Print a pretty message for the victor"""
        flourish_length = int((max_length - len(message)) / 2)
        flourish = flourish_symbol * flourish_length
        output = flourish + " " + message + " " + flourish
        print(output[:max_length])
        print("\n")

    def load_scores(self):
        """Load scores"""
        if os.path.isfile(self.score_path):
            with open(self.score_path, "r") as score_file:
                outcome = score_file.readline()
                while outcome:
                    outcome = outcome.strip()
                    if outcome == "draw":
                        self.draws += 1
                    elif outcome == "player":
                        self.wins += 1
                    else:
                        self.loses += 1
                    outcome = score_file.readline()
        self.total_games = self.wins + self.loses + self.draws

    def display_score(self):
        """Display the player vs computer score"""
        self.load_scores()
        score_table_headers = [
            "Wins",
            "Loses",
            "Draws",
            "Total Games"
        ]
        score_table = [
            [self.wins, self.loses, self.draws, self.total_games]
        ]
        print(tabulate(score_table, score_table_headers, tablefmt="psql"))

    def check_score(self):
        """Determine if the score should be displayed"""
        if self.args.score:
            self.display_score()
            exit()

    def check_multiplayer(self):
        """Determine if that game will be multiplayer"""
        if self.args.multiplayer:
            self.player_1_name = "Player 1"
            self.player_2_name = "Player 2"
        else:
            self.player_1_name = "Player"

    def display_attack_choices(self):
        """Set the attack choices input"""
        if self.args.plaintext:
            self.attack_input = "Rock (1), Paper (2), Scissors (3)? "
        else:
            self.attack_input = f"{SYMBOL_ROCK}  Rock (1)  {SYMBOL_PAPER}  Paper (2)  {SYMBOL_SCISSORS}  Scissors (3)? "

    def get_attack_choice(self):
        """Get the player/s attack choice and set name"""
        # Get self.player_1 attack choice and set name
        self.player_1 = ""
        while self.player_1 not in [1, 2, 3]:
            if self.args.multiplayer:
                self.player_1 = getpass.getpass(self.player_1_name + ":  " + self.attack_input)
            else:
                self.player_1 = input(self.attack_input)
            if self.player_1.isnumeric():
                self.player_1 = int(self.player_1)

        # Get self.player_2 attack choice
        if self.args.multiplayer:
            self.player_2 = ""
            while self.player_2 not in [1, 2, 3]:
                self.player_2 = getpass.getpass(self.player_2_name + ":  " + self.attack_input)
                if self.player_2.isnumeric():
                    self.player_2 = int(self.player_2)
        else:
            self.player_2 = randint(1, 3)

    def set_attack_choice_message(self):
        """Set the players attack choice message"""
        self.player_1_attack_name, self.player_1_attack_symbol = self.attack_method(self.player_1)
        self.player_2_attack_name, self.player_2_attack_symbol = self.attack_method(self.player_2)
        if self.args.plaintext:
            self.player_1_attack = f"{self.player_1_attack_name} ({self.player_1_name})"
            self.player_2_attack = f"{self.player_2_attack_name} ({self.player_2_name})"
        else:
            self.player_1_attack = f"{self.player_1_attack_name}  {self.player_1_attack_symbol}  ({self.player_1_name})"
            self.player_2_attack = f"{self.player_2_attack_name}  {self.player_2_attack_symbol}  ({self.player_2_name})"

    def output_attack_message(self):
        """Output the attack choices"""
        attack_message = f"{self.player_1_attack}  vs  {self.player_2_attack}"
        if self.args.plaintext:
            self.divider_length = len(attack_message)
        elif self.args.multiplayer:
            self.divider_length += 8
        print(self.repeat_to_length("-", self.divider_length))
        print(attack_message)
        print(self.repeat_to_length("-", self.divider_length))

    def output_attack_outcome(self):
        """Output the attack outcome"""
        if self.player_1 == self.player_2:
            attack_outcome = "DRAW"
            self.round_is_draw = True
        elif self.player_1 == 1 and self.player_2 == 3:
            attack_outcome = f"{self.player_1_name} wins!"
            self.player_1_wins = True
        elif self.player_1 == 1 and self.player_2 == 2:
            attack_outcome = f"{self.player_2_name} wins!"
        elif self.player_1 == 2 and self.player_2 == 1:
            attack_outcome = f"{self.player_1_name} wins!"
            self.player_1_wins = True
        elif self.player_1 == 2 and self.player_2 == 3:
            attack_outcome = f"{self.player_2_name} wins!"
        elif self.player_1 == 3 and self.player_2 == 2:
            attack_outcome = f"{self.player_1_name} wins!"
            self.player_1_wins = True
        elif self.player_1 == 3 and self.player_2 == 1:
            attack_outcome = f"{self.player_2_name} wins!"
        self.output_victor(attack_outcome, self.divider_length)

    def write_output_to_score_file(self):
        """Write the output to the score text file"""
        if not self.args.multiplayer:
            score_file = open(self.score_path, "a")
            if self.round_is_draw:
                score_file.write("draw")
            elif self.player_1_wins:
                score_file.write("player")
            else:
                score_file.write("computer")
            score_file.write("\n")

    def start(self):
        """Play the game"""
        self.parse_args()

        self.check_score()

        self.check_multiplayer()

        while(True):
            try:
                self.display_attack_choices()
                self.get_attack_choice()
                self.set_attack_choice_message()
                self.output_attack_message()
                self.output_attack_outcome()
                self.write_output_to_score_file()
            except KeyboardInterrupt:
                print("\n")
                exit()


# Start Game
game = RockPaperScissors(divider_length)
game.start()
