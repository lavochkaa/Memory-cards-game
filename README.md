# Memory Cards

A local two-player memory game built with Python and CustomTkinter.

## How it works

- Pick a board size (4x4, 6x6, 8x8)
- Click two cards to flip them
- If they match, they stay open; if not, they flip back
- Match all pairs to win

## Requirements

- Python 3
- `customtkinter`

## Run locally

Create an isolated environment and install the UI dependency:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install customtkinter
```

Start the desktop application:
```bash
python3 main.py
```

## Verification

The game rules and callback scheduling have unit coverage that does not require a graphical display:

```bash
python3 -m unittest discover -s tests -v
```

## Project structure

- `main.py` - app entry point
- `client/` - desktop client UI
  - `game_controller.py` - window setup, frames, buttons, labels, and UI updates
  - `server_client.py` - future client-side server requests
- `core/` - shared game logic that should not depend on UI or server code
  - `models.py` - `Card`, `User`, and `Player` models
  - `game_logic.py` - board generation, click handling, match checking, turns, score, and winner logic
  - `room.py` - room state and connection between players and game logic
- `server/` - future online multiplayer server
  - `server.py` - future server entry point
  - `room_manager.py` - future room creation/searching/storage logic

## Architecture

The project is split into three main parts: `client`, `core`, and `server`.

`client` is responsible only for what the player sees and does. It creates the CustomTkinter frames, handles button clicks, shows the login/menu/waiting/game/finish screens, and updates labels. The client should not decide game rules by itself. For example, it can send a card click to the logic, but it should not calculate scores or switch turns directly.

`core` contains the actual rules of the game. This is where cards are generated, clicks are counted, matches are checked, turns are switched, scores are updated, and the winner is selected. This code is meant to be shared by both the local client version and the future server version.

`server` is planned for online multiplayer. Later it should own rooms, connect users, wait until a second player joins, start the game, receive card-click actions from clients, update the room state, and send the new state back to both players.

Current game flow:

```text
Login -> Menu -> Waiting -> Game -> Finish
```

Future server flow:

```text
Client login -> Join room -> Server waits for second player -> Server starts room -> Clients render game state
```

Main data idea:

```text
User
  long-living account data, like username and future global stats

Player
  one user's temporary stats inside one room, like score, clicks, and streak

Room
  players, room status, and game logic for one match

GameLogic
  cards, opened cards, current player, match checking, turn switching, and winner logic
```

Important rule:

```text
GameController shows the game.
GameLogic decides the game.
Room groups players and game state.
Server will manage rooms later.
```

## TODO
- [x] Rewrite to OOP
- [ ] Online multiplayer mode
- [x] Proper card design (images/icons instead of numbers)
- [ ] Better UI/UX overall
- [ ] More game modes

## Project status

The local two-player mode is implemented. Online multiplayer remains a planned extension; the `server/` and `client/server_client.py` modules are placeholders for that future work.

![alt text](images/image.png)
