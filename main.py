#!/usr/bin/env python3

import argparse
from random import randint


# Get the readable attack method name
def attack_method(int):
    switcher = {
        1: "ROCK",
        2: "PAPER",
        3: "SCISSORS"
    }
    return switcher.get(int)


# Define the script arguments
parser = argparse.ArgumentParser()
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
        player_1_attack_input = "Player 1: " + attack_input
    else:
        player_1_name = "Player"
        player_1_attack_input = attack_input
    player_1 = int(input(player_1_attack_input))

# Get player_2 attack choice
if multiplayer:
    player_2 = ""
    while player_2 not in [1, 2, 3]:
        player_2 = int(input("Player 2: " + attack_input))
else:
    player_2 = randint(1, 3)

# Output the attack choices
print(f"{attack_method(player_1)} ({player_1_name}) vs {attack_method(player_2)} ({player_2_name})")

# Output the attack outcome
if player_1 == player_2:
    print("DRAW!")
elif player_1 == 1 and player_2 == 3:
    print(f"{player_1_name} wins!")
elif player_1 == 1 and player_2 == 2:
    print(f"{player_2_name} wins!")
elif player_1 == 2 and player_2 == 1:
    print(f"{player_1_name} wins!")
elif player_1 == 2 and player_2 == 3:
    print(f"{player_2_name} wins!")
elif player_1 == 3 and player_2 == 2:
    print(f"{player_1_name} wins!")
elif player_1 == 3 and player_2 == 1:
    print(f"{player_2_name} wins!")
