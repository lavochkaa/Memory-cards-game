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

UPD2: я заебался это все почти с нуля переписывать. но вроде это того стоило. Сейчас я могу начать полноценно без сигмо хардкода добавлять фичи в нормальный код со структурой, но архитектуру я бы все равно изменил, но это может быть позже. Думаю добавить сначала некий Death-режим, где условно тебе нужно пройти за минуту, или систему очков, но для этого нужно будет делть бд (и лучше сразу бд, раз я хочу на онлайн выйти)

P.S. я не дизайнер и с ним будут траблы. я не хочу использовать ии, поэтому стоит что то придумать

![alt text](images/image.png)