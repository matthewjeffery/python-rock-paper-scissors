# Python Rock Paper Scissors
A basic game of Rock Paper Scissors that can be played against the computer or another opponent.

## Installation
This python script is configured to run within a docker container. Execute the following to build the docker image:
```
docker build -t rock-paper-scissors .
```
Alternatively, simplify things with `docker-compose`:
```
docker-compose build
```

## Play time!
Once the docker image has been successfully built, run the container:
```
docker run -it rock-paper-scissors
```
```
docker-compose run game
```

## Multiplayer
Fed up of losing to the computer? Challenge the person next to you!
```
docker run -it rock-paper-scissors --multiplayer
```
```
docker-compose run game --multiplayer
```

## Graphics
Fancy playing old school? Remove the graphics by playing in plaintext mode!
```
docker run -it rock-paper-scissors --plaintext
```
```
docker-compose run game --plaintext
```

## Scoring
Feeling competitive? See how your skills stack up against the computer!
```
docker run -it rock-paper-scissors --score
```
```
docker-compose run game --score
```

### Persistence
When running the _rock-paper-scissors_ container via `docker` you will notice that without a _volume_ scores will never be tracked. This is due to the underlying way `docker` handles files. However, this can be avoided by initialising a volume at runtime or by using `docker-compose` which has a predefined volume configuration:
```
docker run -itv "$PWD":/rock-paper-scissors rock-paper-scissors
```
```
docker-compose run game
```

## Running Natively
Prefer playing games natively? Execute the following via the command line:
```
./play.py
```

### Requirements
To run the game natively the following dependencies must be installed:
- [Python 3](https://www.python.org/downloads/)
- [Tabulate](https://pypi.org/project/tabulate/)
- [Tkinter](https://tkdocs.com/tutorial/install.html)

### Graphical Interface
Play with a graphical interface by adding the `--gui` option flag during execution.
```
./play.py --gui
```
