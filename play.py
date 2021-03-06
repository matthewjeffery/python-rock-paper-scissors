#!/usr/bin/env python3

import argparse
import getpass
import os
from random import randint
from tabulate import tabulate
import time

tabulate.PRESERVE_WHITESPACE = True
tabulate.WIDE_CHARS_MODE = True

if os.getenv('GUI_ENABLED') not in ["false", "False", "FALSE", "n", "N", "no", "No", "NO", "off", "Off", "OFF"]:
    GUI_ENABLED = True
    import tkinter as tk
else:
    GUI_ENABLED = False


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
        self.displayed_table_width = 0
        self.reset_attack_outcome()

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Play a game of Rock Paper Scissors!")
        parser.add_argument("-m", "--multiplayer", help="play the game with 2 players", action="store_true")
        parser.add_argument("-p", "--plaintext", help="play the game in plaintext mode", action="store_true")
        parser.add_argument("-s", "--score", help="display the total score against the computer", action="store_true")
        if GUI_ENABLED:
            parser.add_argument("-g", "--gui", help="display a GUI for single player mode", action="store_true")
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
            self.display_score_table()
            print("\n")
            self.display_score_chart()
            exit()

    def display_score_table(self):
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

    def display_score_chart(self):
        data = [
            ('Wins', self.wins),
            ('Loses', self.loses),
            ('Draws', self.draws)
        ]

        max_value = max(count for _, count in data)
        score_table_width = 38
        increment = max_value / score_table_width if max_value > 0 else 1

        longest_label_length = max(len(label) for label, _ in data)

        for label, count in data:
            # The ASCII block elements come in chunks of 8, so we work out how
            # many fractions of 8 we need.
            # https://en.wikipedia.org/wiki/Block_Elements
            bar_chunks, remainder = divmod(int(count * 8 / increment), 8)

            # First draw the full width chunks
            bar = '█' * bar_chunks

            # Then add the fractional part. The Unicode code points for
            # block elements are (8/8), (7/8), (6/8), etc. so we need to
            # work backwards.
            if remainder > 0:
                bar += chr(ord('█') + (8 - remainder))

            # If the bar is empty, add a left one-eighth block
            bar = bar or '▏'

            print(f'{label.rjust(longest_label_length)}: {bar}')

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

    def set_attack_choice(self, player_1_choice="", player_2_choice=""):
        self.set_attack_input_message()

        # Get self.player_1 attack choice and set name
        self.player_1 = player_1_choice
        while self.player_1 not in [1, 2, 3]:
            if self.args.multiplayer:
                self.player_1 = getpass.getpass(self.player_1_name + ":  " + self.attack_input)
            else:
                self.player_1 = input(self.attack_input)
            if self.player_1.isnumeric():
                self.player_1 = int(self.player_1)

        # Get self.player_2 attack choice
        if self.args.multiplayer:
            self.player_2 = player_2_choice
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

    def reset_attack_outcome(self):
        self.round_is_draw = False
        self.player_1_wins = False

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

    def check_gui(self):
        if GUI_ENABLED and self.args.gui and not self.args.multiplayer:
            self.set_attack_input_message()
            print(self.attack_input)
            self.use_gui()

    def use_gui(self):
        window = tk.Tk()
        window.title("Attack Method")
        window.protocol('WM_DELETE_WINDOW', exit)

        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True)

        button_rock = tk.Button(frame, text="Rock", width=10, command=lambda: self.handle_gui_attack(1))
        button_rock.pack(side=tk.LEFT, padx=5, pady=5)

        button_paper = tk.Button(frame, text="Paper", width=10, command=lambda: self.handle_gui_attack(2))
        button_paper.pack(side=tk.LEFT, padx=0, pady=5)

        button_scissors = tk.Button(frame, text="Scissors", width=10, command=lambda: self.handle_gui_attack(3))
        button_scissors.pack(side=tk.LEFT, padx=5, pady=5)

        window.mainloop()

    def handle_gui_attack(self, choice):
        self.handle_attack(choice)
        print(self.attack_input)

    def handle_attack(self, player_1_choice="", player_2_choice="", interval=0.75):
        self.set_attack_choice(player_1_choice, player_2_choice)
        self.display_attack_choice()
        self.display_attack_outcome()
        self.write_outcome_to_score_file()
        self.reset_attack_outcome()
        time.sleep(interval)

    def start(self):
        self.parse_args()
        self.check_score()
        self.check_multiplayer()
        self.check_gui()

        while(True):
            try:
                self.handle_attack()
            except KeyboardInterrupt:
                print("\n")
                exit()


# Start Game
game = RockPaperScissors()
game.start()
