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

- `main.py` — window setup, menu, and frame switching
- `game_logic.py` — board generation, click handling, match checking

## TODO
- [+] Rewrite to OOP
- [ ] Online multiplayer mode
- [+] Proper card design (images/icons instead of numbers)
- [ ] Better UI/UX overall
- [ ] More game modes

## Some info

I coocked this demo-game without AI (im prouding myself)

Короче это хардкод который работает чисто на добром слове, я не знаю, как буду это говно оптимизировать, ведь тут везде я передаю постоянно frames, size и тд, но чисто ради забавы сойдет

![alt text](images/image.png)