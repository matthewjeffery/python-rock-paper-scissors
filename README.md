# Python Rock Paper Scissors
A basic game of Rock Paper Scissors that can be played against the computer or another opponent.

## Installation
This python script is configured to run within a docker container. Execute the following to build the docker image:
```
docker build -t rock-paper-scissors .
```

## Play time!
Once the docker image has been successfully built, run the container:
```
docker run -it rock-paper-scissors
```

## Multiplayer
Fed up of losing to the computer? Challenge the person next to you!
```
docker run -it rock-paper-scissors -m
```
