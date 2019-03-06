#!/usr/bin/env python3

from random import randint


# Get the readable attack method name
def attack_method(int):
    switcher = {
        1: "ROCK",
        2: "PAPER",
        3: "SCISSORS"
    }
    return switcher.get(int)


# Set the type of opponent
play_computer = ""
multiplayer = False
while play_computer not in ["y", "Y", "yes", "Yes", "n", "N", "no", "No"]:
    play_computer = input('Play the computer? [y/n] ')

# Set the opponent name
opponent_name = "Computer"
if play_computer not in ["y", "Y", "yes", "Yes"]:
    opponent_name = "Player 2"
    multiplayer = True

# Set the attack choices input
attack_input = "Rock (1), Paper (2), Scissors (3)? "

# Get player_1 attack choice and set name
player_1 = ""
while player_1 not in [1, 2, 3]:
    if multiplayer:
        player_name = "Player 1"
        player_1_input = "Player 1: " + attack_input
    else:
        player_name = "Player"
        player_1_input = attack_input
    player_1 = int(input(player_1_input))

# Get player_2 attack choice
if multiplayer:
    player_2 = ""
    while player_2 not in [1, 2, 3]:
        player_2 = int(input("Player 2: " + attack_input))
else:
    player_2 = randint(1, 3)

# Output the attack choices
print(f"{attack_method(player_1)} ({player_name}) vs {attack_method(player_2)} ({opponent_name})")

# Output the attack outcome
if player_1 == player_2:
    print("DRAW!")
elif player_1 == 1 and player_2 == 3:
    if multiplayer:
        print("Player 1 wins!")
    else:
        print("Player wins!")
elif player_1 == 1 and player_2 == 2:
    if multiplayer:
        print("Player 2 wins!")
    else:
        print("Computer wins!")
elif player_1 == 2 and player_2 == 1:
    if multiplayer:
        print("Player 1 wins!")
    else:
        print("Player wins!")
elif player_1 == 2 and player_2 == 3:
    if multiplayer:
        print("Player 2 wins!")
    else:
        print("Computer wins!")
elif player_1 == 3 and player_2 == 2:
    if multiplayer:
        print("Player 1 wins!")
    else:
        print("Player wins!")
elif player_1 == 3 and player_2 == 1:
    if multiplayer:
        print("Player 2 wins!")
    else:
        print("Computer wins!")
