#!/usr/bin/env python3

import argparse
import getpass
import os
from random import randint
from tabulate import tabulate

# Define global options
score_path = "./score.txt"
divider_length = 47

# Define the game symbols
symbol_rock = "👊"  # \U0001F44A
symbol_paper = "🤚"  # \U0001F91A
symbol_scissors = "✌️"  # \U0000270C


# Get the readable attack method name and symbol
def attack_method(int):
    name = {
        1: "ROCK",
        2: "PAPER",
        3: "SCISSORS"
    }
    symbol = {
        1: symbol_rock,
        2: symbol_paper,
        3: symbol_scissors,
    }
    return name.get(int), symbol.get(int)


# Repeat a string X times
def repeat_to_length(str, multiplier):
    return str * multiplier


# Print a pretty message for the victor
def output_victor(message, max_length, flourish_symbol="*"):
    flourish_length = int((max_length - len(message)) / 2)
    flourish = flourish_symbol * flourish_length
    output = flourish + " " + message + " " + flourish
    print(output[:max_length])


# Define the script arguments
parser = argparse.ArgumentParser(description="Play a game of Rock Paper Scissors!")
parser.add_argument("-m", "--multiplayer", help="play the game with 2 players", action="store_true")
parser.add_argument("-p", "--plaintext", help="play the game in plaintext mode", action="store_true")
parser.add_argument("-s", "--score", help="display the total score against the computer", action="store_true")
args = parser.parse_args()

# Display the player vs computer score
if args.score:
    # Counters
    wins = 0
    loses = 0
    draws = 0

    # Load scores
    if os.path.isfile(score_path):
        with open(score_path, "r") as score_file:
            outcome = score_file.readline()
            while outcome:
                outcome = outcome.strip()
                if outcome == "draw":
                    draws += 1
                elif outcome == "player":
                    wins += 1
                else:
                    loses += 1
                outcome = score_file.readline()
    total_games = wins + loses + draws

    # Output scores
    score_table_headers = [
        "Wins",
        "Loses",
        "Draws",
        "Total Games"
    ]
    score_table = [
        [wins, loses, draws, total_games]
    ]
    print(tabulate(score_table, score_table_headers, tablefmt="psql"))

    # Force quit
    exit()

# Determine if that game will be multiplayer
if args.multiplayer:
    multiplayer = True
    player_2_name = "Player 2"
else:
    multiplayer = False
    player_2_name = "Computer"

# Set the attack choices input
if args.plaintext:
    attack_input = "Rock (1), Paper (2), Scissors (3)? "
else:
    attack_input = f"{symbol_rock}  Rock (1)  {symbol_paper}  Paper (2)  {symbol_scissors}  Scissors (3)? "

# Get player_1 attack choice and set name
player_1 = ""
while player_1 not in [1, 2, 3]:
    if multiplayer:
        player_1_name = "Player 1"
        player_1 = getpass.getpass(player_1_name + ": " + attack_input)
    else:
        player_1_name = "Player"
        player_1 = input(attack_input)
    if player_1.isnumeric():
        player_1 = int(player_1)

# Get player_2 attack choice
if multiplayer:
    player_2 = ""
    while player_2 not in [1, 2, 3]:
        player_2 = getpass.getpass(player_2_name + ": " + attack_input)
        if player_2.isnumeric():
            player_2 = int(player_2)
else:
    player_2 = randint(1, 3)

# Set the players attack choice message
player_1_attack_name, player_1_attack_symbol = attack_method(player_1)
player_2_attack_name, player_2_attack_symbol = attack_method(player_2)
if args.plaintext:
    player_1_attack = f"{player_1_attack_name} ({player_1_name})"
    player_2_attack = f"{player_2_attack_name} ({player_2_name})"
else:
    player_1_attack = f"{player_1_attack_name}  {player_1_attack_symbol}  ({player_1_name})"
    player_2_attack = f"{player_2_attack_name}  {player_2_attack_symbol}  ({player_2_name})"

# Output the attack choices
attack_message = f"{player_1_attack}  vs  {player_2_attack}"
if args.plaintext:
    divider_length = len(attack_message)
elif multiplayer:
    divider_length += 8
print(repeat_to_length("-", divider_length))
print(attack_message)
print(repeat_to_length("-", divider_length))

# Output the attack outcome
round_is_draw = False
player_1_wins = False

if player_1 == player_2:
    attack_outcome = "DRAW"
    round_is_draw = True
elif player_1 == 1 and player_2 == 3:
    attack_outcome = f"{player_1_name} wins!"
    player_1_wins = True
elif player_1 == 1 and player_2 == 2:
    attack_outcome = f"{player_2_name} wins!"
elif player_1 == 2 and player_2 == 1:
    attack_outcome = f"{player_1_name} wins!"
    player_1_wins = True
elif player_1 == 2 and player_2 == 3:
    attack_outcome = f"{player_2_name} wins!"
elif player_1 == 3 and player_2 == 2:
    attack_outcome = f"{player_1_name} wins!"
    player_1_wins = True
elif player_1 == 3 and player_2 == 1:
    attack_outcome = f"{player_2_name} wins!"

output_victor(attack_outcome, divider_length)

# Write the output to the score text file
if not multiplayer:
    score_file = open(score_path, "a")
    if round_is_draw:
        score_file.write("draw")
    elif player_1_wins:
        score_file.write("player")
    else:
        score_file.write("computer")
    score_file.write("\n")
