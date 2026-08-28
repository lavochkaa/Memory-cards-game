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
- `models.py` - card selfs, (Users class) etc..

## TODO
- [x] Rewrite to OOP
- [ ] Online multiplayer mode
- [x] Proper card design (images/icons instead of numbers)
- [ ] Better UI/UX overall
- [ ] More game modes

## More info

I coocked this demo-game without AI (im prouding myself)

UPD4: Начал перестройку СССР под P2P, обавил логику топорную. Если щас не в лом будет, то обновлю уже до полноценного P2P, у меня как раз завалялся один VPS, поэтому игра станет бесплатной, с онлайном, но на небольшое врем ~неделя.

P.S. я не дизайнер и с ним будут траблы. я не хочу использовать ии, поэтому стоит что то придумать

![alt text](images/image.png)