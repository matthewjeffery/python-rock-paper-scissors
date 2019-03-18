#!/usr/bin/env python3

import argparse
import getpass
import os
from random import randint
from tabulate import tabulate
import time

tabulate.PRESERVE_WHITESPACE = True
tabulate.WIDE_CHARS_MODE = True


class RockPaperScissors(object):
    SYMBOL_ROCK = "👊"  # \U0001F44A
    SYMBOL_PAPER = "🤚"  # \U0001F91A
    SYMBOL_SCISSORS = "✌️"  # \U0000270C
    SCORE_PATH = "./score.txt"

    def __init__(self):
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

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Play a game of Rock Paper Scissors!")
        parser.add_argument("-m", "--multiplayer", help="play the game with 2 players", action="store_true")
        parser.add_argument("-p", "--plaintext", help="play the game in plaintext mode", action="store_true")
        parser.add_argument("-s", "--score", help="display the total score against the computer", action="store_true")
        self.args = parser.parse_args()

    def repeat_string(self, string, multiplier):
        return string * multiplier

    def check_multiplayer(self):
        if self.args.multiplayer:
            self.player_1_name = "Player 1"
            self.player_2_name = "Player 2"
        else:
            self.player_1_name = "Player"

    def check_score(self):
        if self.args.score:
            self.display_score()
            exit()

    def display_score(self):
        if os.path.isfile(self.SCORE_PATH):
            with open(self.SCORE_PATH, "r") as score_file:
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

        score_table_headers = [
            "Wins",
            "Loses",
            "Draws",
            "Total Games"
        ]
        score_table = [
            [
                self.wins,
                self.loses,
                self.draws,
                self.total_games
            ]
        ]
        print(tabulate(score_table, score_table_headers, tablefmt="psql"))

    def get_attack_method(self, choice: int):
        name = {
            1: "ROCK",
            2: "PAPER",
            3: "SCISSORS"
        }
        symbol = {
            1: self.SYMBOL_ROCK,
            2: self.SYMBOL_PAPER,
            3: self.SYMBOL_SCISSORS,
        }
        return name.get(choice), symbol.get(choice)

    def set_attack_input_message(self):
        if self.args.plaintext:
            self.attack_input = "Rock (1), Paper (2), Scissors (3)? "
        else:
            self.attack_input = f"{self.SYMBOL_ROCK}  Rock (1)  {self.SYMBOL_PAPER}  Paper (2)  {self.SYMBOL_SCISSORS}  Scissors (3)? "

    def set_attack_choice(self):
        self.set_attack_input_message()

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

    def display_attack_choice(self):
        self.player_1_attack_name, self.player_1_attack_symbol = self.get_attack_method(self.player_1)
        self.player_2_attack_name, self.player_2_attack_symbol = self.get_attack_method(self.player_2)

        if self.args.plaintext:
            player_1_attack_message = self.player_1_attack_name
            player_2_attack_message = self.player_2_attack_name
        else:
            player_1_attack_message = self.player_1_attack_symbol + "  " + self.player_1_attack_name
            player_2_attack_message = self.player_2_attack_symbol + "  " + self.player_2_attack_name

        attack_table_headers = [
            f"     {self.player_1_name}     ",
            "vs",
            f"     {self.player_2_name}     "
        ]
        attack_table = [
            [
                player_1_attack_message,
                "",
                player_2_attack_message
            ]
        ]

        print("\n")
        print(tabulate(attack_table, attack_table_headers, tablefmt="simple", colalign=("center", "center", "center")))

        table_length_offset = 8
        attack_table_headers_length = 0
        for header in attack_table_headers:
            attack_table_headers_length += len(header)
        self.displayed_table_width = attack_table_headers_length + table_length_offset

    def display_attack_outcome(self):
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

        width = self.repeat_string(" ", self.displayed_table_width)
        print(tabulate([[attack_outcome]], [width], tablefmt="simple", colalign=("center",)))
        print("\n")

    def write_outcome_to_score_file(self):
        if not self.args.multiplayer:
            score_file = open(self.SCORE_PATH, "a")
            if self.round_is_draw:
                score_file.write("draw")
            elif self.player_1_wins:
                score_file.write("player")
            else:
                score_file.write("computer")
            score_file.write("\n")

    def start(self):
        self.parse_args()

        self.check_score()

        self.check_multiplayer()

        while(True):
            try:
                self.set_attack_choice()
                self.display_attack_choice()
                self.display_attack_outcome()
                self.write_outcome_to_score_file()
                time.sleep(0.75)
            except KeyboardInterrupt:
                print("\n")
                exit()


# Start Game
game = RockPaperScissors()
game.start()
