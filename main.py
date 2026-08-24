import customtkinter as ctk
import random

# -- Global values --
current_game = None
EMOJIS = [
    "🍎", "🍌", "🍇", "🍒", "🍉", "🥝", "🍑", "🍓",
    "🍋", "🍊", "🍍", "🥥", "🍈", "🍏", "🥭", "🍐",
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼",
    "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🦄"
]

# -- Constants --
CARD_SIZE = 70
BUTTON_SIZE = 5
FLIP_DELAY = 30
FLIP_STEPS = 6
CHECK_DELAY = 700
TIMER_DELAY = 1000
TIMER_MIN = 60

# -- Classes --
class GameController:
    def __init__(self):
        # TODO - ref all UI here
        pass

class Card:
    # Basic selfs
    def __init__(self, value, row, col, button):
        self.value = value
        self.row = row
        self.col = col
        self.button = button
        self.is_open = False
        self.is_matched = False

    # Imitate flip to open
    def open(self, steps=FLIP_STEPS, delay=FLIP_DELAY):
        self.is_open = True
        original_width = self.button.cget("width")

        # Hard math, in 1 -> 0.5 -> change card
        def shrink(step):
            if step <= steps // 2:
                width = original_width * (1 - step / (steps // 2))
                self.button.configure(width=max(int(width), 1))
                self.button.after(delay, lambda: shrink(step + 1))
            else:
                self.button.configure(text=self.value)
                grow(step)

        # Hard math part 2, 0.5 -> 1
        def grow(step):
            if step <= steps:
                progress = (step - steps // 2) / (steps // 2)
                width = original_width * progress
                self.button.configure(width=max(int(width), 1))
                self.button.after(delay, lambda: grow(step + 1))
            else:
                self.button.configure(width=original_width)

        shrink(0)

    # Imitate flip to close
    def hide(self, steps=FLIP_STEPS, delay=FLIP_DELAY):
        self.is_open = False
        original_width = self.button.cget("width")

        # Hard math, in 1 -> 0.5 -> change card
        def shrink(step):
            if step <= steps // 2:
                width = original_width * (1 - step / (steps // 2))
                self.button.configure(width=max(int(width), 1))
                self.button.after(delay, lambda: shrink(step + 1))
            else:
                self.button.configure(text="?")
                grow(step)

        # Hard math part 2, 0.5 -> 1
        def grow(step):
            if step <= steps:
                progress = (step - steps // 2) / (steps // 2)
                width = original_width * progress
                self.button.configure(width=max(int(width), 1))
                self.button.after(delay, lambda: grow(step + 1))
            else:
                self.button.configure(width=original_width)

        shrink(0)

    # If pair -> green
    def mark_matched(self):
        self.is_matched = True
        self.button.configure(fg_color="green")

class GameLogic:
    # Basic selfs
    def __init__(self, root, game_frame, finish_frame, size):
        self.root = root # ref
        self.game_frame = game_frame # ref
        self.finish_frame = finish_frame # ref
        self.size = size
        self.cards = []
        self.opened = []
        self.buttons = [] # ref
        self.clicks = 0
        self.matched_count = 0
        self.seconds_passed = 0
        self.timer_running = False
        self.timer_if = None

    # Start to generate cards
    def generate_cards(self):
        # Clear widgets
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        # Clear massives
        self.cards.clear()
        self.buttons.clear()
        self.opened.clear()

        # Decompine to int
        pairs_count = (self.size ** 2) // 2

        # Create massive with NxN btn -> (N ** 2) // 2 pairs
        values_flat = (EMOJIS[:pairs_count]) * 2
        random.shuffle(values_flat)

        # Sigma value
        index = 0

        # Generate logic
        for pos_x in range(self.size):
            for pos_y in range(self.size):
                # Get value and write
                val = values_flat[index]

                # Create button
                btn = ctk.CTkButton(self.game_frame, text="?", width=CARD_SIZE, height=CARD_SIZE)
                btn.grid(row=pos_x, column=pos_y, padx=BUTTON_SIZE, pady=BUTTON_SIZE)

                # Create card
                card = Card(val, pos_x, pos_y, btn)
                self.cards.append(card)

                # Create button
                btn.configure(command=lambda c=card: self.on_click(c))
                self.buttons.append(btn)

                # This sigma value forever
                index += 1

        # Create timer
        self.timer_lbl = ctk.CTkLabel(self.game_frame, text="Time: 0:00")
        self.timer_lbl.grid(row=self.size, column=0, columnspan=self.size, pady=(10, 0))

        # Create clicks counter
        self.clicks_lbl = ctk.CTkLabel(self.game_frame, text="Clicks: 0")
        self.clicks_lbl.grid(row=self.size + 1, column=0, columnspan=self.size, pady=(10, 0))

        # Create "Back" button
        game_back_btn = ctk.CTkButton(self.game_frame, text="Back", command=back_to_menu)
        game_back_btn.grid(row=self.size + 2, column=0, columnspan=self.size, pady=(10, 0))

        # Start timer
        self.seconds_passed = 0
        self.timer_running = True
        self.start_timer()

    # Click logic
    def on_click(self, card):
        # Check oppend or matched
        if card.is_open or card.is_matched or (len(self.opened) >= 2):
            return

        # Do a flip and block
        card.open()
        self.opened.append(card)

        self.clicks += 1
        self.clicks_lbl.configure(text=f"Clicks: {self.clicks}")

        # If two cards flipped -> check T / F
        if len(self.opened) == 2:
            self.root.after(CHECK_DELAY, self.check_match)

    # Ckeck values
    def check_match(self):
        # Get value1, value2
        first_card, second_card = self.opened

        # if first_card == second_card -> cool
        if first_card.value == second_card.value:
            first_card.mark_matched()
            second_card.mark_matched()
            self.matched_count += 2
        else:
            first_card.hide()
            second_card.hide()

        # Clear opened cards and close
        self.opened.clear()

        # Check to win
        if self.matched_count == len(self.cards):
            self.timer_running = False

            minutes = self.seconds_passed // TIMER_MIN
            seconds = self.seconds_passed % TIMER_MIN

            # Update values 
            finish_main_lbl.configure(text=f"You are stupid guy !\n\nTime: {minutes}:{seconds:02d}\nClicks: {self.clicks}")

            # Cahnge frame to win
            self.game_frame.pack_forget()
            self.finish_frame.pack(expand=True)

    # This func starting timer
    def start_timer(self):
        if not self.timer_running:
            return

        # Calc time
        minutes = self.seconds_passed // TIMER_MIN
        secs = self.seconds_passed % TIMER_MIN
        self.timer_lbl.configure(text=f"Time: {minutes}:{secs:02d}")

        # Recursion update
        self.seconds_passed += 1
        self.timer_id = self.root.after(TIMER_DELAY, self.start_timer)

    def stop_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

# -- Defines --
def start_game():
    global current_game

    # Change frame to game
    menu_frame.pack_forget()
    game_frame.pack(expand=True)

    # Agruments to class
    size = get_size()
    current_game = GameLogic(root, game_frame, finish_frame, size)
    current_game.generate_cards()

# Idk how u not understand what this func do
def back_to_menu():
    if current_game:
        current_game.stop_timer()
        current_game = None

    # Close all frames and open main menu
    game_frame.pack_forget()
    finish_frame.pack_forget()
    menu_frame.pack(expand=True)

# Auto change size to button
def change_size(new_val):
    global menu_seg_selected

    menu_seg_selected = new_val

# Global value (string) -> Func (int)
def get_size():
    return int(menu_seg_selected.split('x')[0])

# -- Root window --
root = ctk.CTk()
root.title("Memory game")
root.geometry("900x800")

# -- Frames --
menu_frame = ctk.CTkFrame(root)
game_frame = ctk.CTkFrame(root)
finish_frame = ctk.CTkFrame(root)

# -- Segments --
menu_seg = ctk.CTkSegmentedButton(
    menu_frame, 
    values=["4x4", "6x6", "8x8"],
    command=change_size
)
# Basic segment
menu_seg_selected = "4x4"
menu_seg.set("4x4")

# -- Labels --
menu_start_lbl = ctk.CTkLabel(menu_frame, text="Pick range buttons")
finish_main_lbl = ctk.CTkLabel(finish_frame, text="You are stupid guy !\nTime:\nClicks:")

# -- Buttons --
menu_start_btn = ctk.CTkButton(menu_frame, text="Start", command=start_game)
finish_btn = ctk.CTkButton(finish_frame, text="Back", command=back_to_menu)

# -- Packs --
finish_main_lbl.grid(padx=20, pady=20)
finish_btn.grid(padx=20, pady = 20)
menu_start_lbl.grid(row=0, column=0)
menu_seg.grid(row=1, column=0, padx=20, pady=20)
menu_start_btn.grid(row=2, column=0, padx=20, pady=20)

# Start all logic
if __name__ == "__main__":
    menu_frame.pack(expand=True) # Start with menu frame
    root.mainloop()