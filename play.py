#!/usr/bin/env python3

import argparse
import getpass
from random import randint


# Get the readable attack method name
def attack_method(int):
    switcher = {
        1: "ROCK",
        2: "PAPER",
        3: "SCISSORS"
    }
    return switcher.get(int)


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
args = parser.parse_args()

# Determine if that game will be multiplayer
multiplayer = False
if args.multiplayer:
    multiplayer = True
    player_2_name = "Player 2"
else:
    player_2_name = "Computer"

# Set the attack choices input
attack_input = "Rock (1), Paper (2), Scissors (3)? "

# Get player_1 attack choice and set name
player_1 = ""
while player_1 not in [1, 2, 3]:
    if multiplayer:
        player_1_name = "Player 1"
        player_1 = int(getpass.getpass(player_1_name + ": " + attack_input))
    else:
        player_1_name = "Player"
        player_1 = int(input(attack_input))

# Get player_2 attack choice
if multiplayer:
    player_2 = ""
    while player_2 not in [1, 2, 3]:
        player_2 = int(getpass.getpass("Player 2: " + attack_input))
else:
    player_2 = randint(1, 3)

# Output the attack choices
attack_message = f"{attack_method(player_1)} ({player_1_name}) vs {attack_method(player_2)} ({player_2_name})"
attack_message_length = len(attack_message)
print(repeat_to_length("-", attack_message_length))
print(attack_message)
print(repeat_to_length("-", attack_message_length))

# Output the attack outcome
if player_1 == player_2:
    attack_outcome = "DRAW"
elif player_1 == 1 and player_2 == 3:
    attack_outcome = f"{player_1_name} wins!"
elif player_1 == 1 and player_2 == 2:
    attack_outcome = f"{player_2_name} wins!"
elif player_1 == 2 and player_2 == 1:
    attack_outcome = f"{player_1_name} wins!"
elif player_1 == 2 and player_2 == 3:
    attack_outcome = f"{player_2_name} wins!"
elif player_1 == 3 and player_2 == 2:
    attack_outcome = f"{player_1_name} wins!"
elif player_1 == 3 and player_2 == 1:
    attack_outcome = f"{player_2_name} wins!"

output_victor(attack_outcome, attack_message_length)
