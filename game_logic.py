import customtkinter as ctk
import random

# -- Global values --
cards_buttons = [] # buttons, indexes
cards_values = [] # randomed values
opened = [] # index openned cards (max = 2)
matched = [] # index cliamed cards 

# -- Defines --
# Change configurate button
def on_card_click(r, c, game_frame, finish_frame, size):
    if [r, c] in opened or [r, c] in matched:
        return

    if len(opened) >= 2:
        return
    
    cards_buttons[r][c].configure(text=str(cards_values[r][c]))
    opened.append([r, c])

    if len(opened) == 2:
        game_frame.after(700, lambda: check_match(size, game_frame, finish_frame))

# check correct or not
def check_match(size, game_frame, finish_frame):
    (r1, c1), (r2, c2) = opened
    if cards_values[r1][c1] == cards_values[r2][c2]:
        matched.append([r1, c1])
        matched.append([r2, c2])
        cards_buttons[r1][c1].configure(bg="green")
        cards_buttons[r2][c2].configure(bg="green")
    else:
        cards_buttons[r1][c1].configure(text="?")
        cards_buttons[r2][c2].configure(text="?")
    opened.clear()

    # If you win you are stupid
    if len(matched) == (size ** 2):
        game_frame.pack_forget()
        finish_frame.pack()

# Start genegate buttons aka cards
def start_game_logic(value, game_frame, finish_frame):
    global cards_buttons, cards_values, opened, matched

    # Clear massives
    cards_buttons = []
    cards_values = []
    opened = []
    matched = []

    # Debug
    print("size:", value)

    # Decompine to int
    size = int(value.split("x")[0])
    pairs_count = (size ** 2) // 2

    # Create pairs 4x4 -> 8 pairs
    values_flat = list(range(pairs_count)) * 2
    random.shuffle(values_flat)

    # Sigmo hardcode
    index = 0

    # Generate massives and buttons
    for x in range(size):
        row_values = []
        row_buttons = []
        for y in range(size):
            # Get value and write
            val = values_flat[index]
            index += 1
            row_values.append(val)

            # Create button
            btn = ctk.CTkButton(
                    game_frame, text="?",
                    command=lambda r=x, c=y: on_card_click(r, c, game_frame, finish_frame, size),
                    width=70, height=70
            )
            btn.grid(row=x, column=y, padx=5, pady=5)

            row_buttons.append(btn)
        cards_values.append(row_values)
        cards_buttons.append(row_buttons)

    return cards_buttons