# Memory Cards

A simple memory (matching pairs) card game built with Python and CustomTkinter.

## How it works

- Pick a board size (4x4, 6x6, 8x8)
- Click two cards to flip them
- If they match, they stay open; if not, they flip back
- Match all pairs to win

## Requirements

- Python 3
- `customtkinter`

Install dependencies:
```bash
pip install customtkinter
```

Run:
```bash
python main.py
```

## Project structure

- `main.py` — start
- `game_logic.py` - board generation, click handling, match checking
- `game_controller.py` - window setup, menu, and frame switching
- `models.py` - card selfs, Users class, TODO - Room

## TODO
- [x] Rewrite to OOP
- [ ] Online multiplayer mode
- [x] Proper card design (images/icons instead of numbers)
- [ ] Better UI/UX overall
- [ ] More game modes

## More info

I coocked this demo-game without AI (im prouding myself)

UPD5: Максимум который смог выжать из клиента сделан. Завтра напишу сервер на шедевропитоне и выгружу. Большую часть багов я пофиксил, ну и саму логику поправил, думаю норм игрулька наподобие тех, что раньше были для игры на одном девайсе, ностальгия...

P.S. я не дизайнер и с ним будут траблы. я не хочу использовать ии, поэтому стоит что то придумать

![alt text](images/image.png)