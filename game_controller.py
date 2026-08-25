import customtkinter as ctk
from game_logic import GameLogic

# -- Constants --
LABEL_SIZE = 20
SEGMENT_SIZE = 20
CARD_SIZE = 70
MENU_BUTTON_SIZE = 20
BUTTON_SIZE = 5
FLIP_DELAY = 30
FLIP_STEPS = 6
CHECK_DELAY = 700
TIMER_DELAY = 1000
TIMER_MIN = 60

# -- Game controller --
class GameController:
    # -- Inits --
    def __init__(self, root):
        self.root = root

        # -- Frames --
        self.menu_frame = ctk.CTkFrame(root)
        self.game_frame = ctk.CTkFrame(root)
        self.finish_frame = ctk.CTkFrame(root)

        # -- Values --
        self.game_logic = None
        self.timer_after_id = None
        self.selected_size = "4x4"
        self.buttons = []
        self.animation_after_ids = []

        # -- Atributs --
        self._build_menu_ui()
        self._build_finish_ui()
        self._show_menu()

    # Start game
    def start_game(self):
        # Clear pids
        self._cancel_pending_callbacks()

        # Size to int value
        size = int(self.selected_size.split('x')[0])

        # Start logic
        self.game_logic = GameLogic(size)
        self.game_logic.generate_cards()

        # Start funcions
        self._build_game_ui(size)
        self._update_timer()
        self._show_game()

    # Close all and open menu
    def _show_menu(self):
        self._switch_frame(self.menu_frame)

    # Close all and open gmae
    def _show_game(self):
        self._switch_frame(self.game_frame)

    # Close all and open finish
    def _show_finish(self):
        self._switch_frame(self.finish_frame)

    # Create main menu
    def _build_menu_ui(self):
        self.menu_frame.grid_columnconfigure(0, weight=1)

        # -- Labels --
        menu_main_lbl = ctk.CTkLabel(self.menu_frame, text="Select range buttons")
        menu_main_lbl.grid(row=0, column=0, padx=LABEL_SIZE, pady=LABEL_SIZE, sticky="ew")

        # -- Segments --
        menu_range_seg = ctk.CTkSegmentedButton(
            self.menu_frame,
            values=["4x4", "6x6", "8x8"],
            command=self._on_size_change
        )
        menu_range_seg.set(self.selected_size)
        menu_range_seg.grid(row=1, column=0, padx=SEGMENT_SIZE, pady=SEGMENT_SIZE, sticky="ew")

        # -- Buttons --
        menu_start_btn = ctk.CTkButton(self.menu_frame, text="Start", command=self.start_game)
        menu_start_btn.grid(row=2, column=0, padx=MENU_BUTTON_SIZE, pady=MENU_BUTTON_SIZE, sticky="ew")

    # Build only widgets
    def _build_game_ui(self, size):
        # Clear all
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.buttons.clear()

        # Create buttons
        for row in range(size):
            for col in range(size):
                btn = ctk.CTkButton(
                    self.game_frame,
                    text="?",
                    width=CARD_SIZE,
                    height=CARD_SIZE,
                    command=lambda r=row, c=col: self.on_card_click(r, c))
                btn.grid(row=row, column=col, padx=BUTTON_SIZE, pady=BUTTON_SIZE)
                self.buttons.append(btn)

        # Timer
        self.game_timer_lbl = ctk.CTkLabel(self.game_frame, text="Time: 0:00")
        self.game_timer_lbl.grid(row=size, column=0, columnspan=size, pady=(10, 0))

        # Click counter
        self.game_clicks_lbl = ctk.CTkLabel(self.game_frame, text="Clicks: 0")
        self.game_clicks_lbl.grid(row=size + 1, column=0, columnspan=size, pady=(10, 0))

        # Score counter
        self.game_score_lbl = ctk.CTkLabel(self.game_frame, text="Score: 0, Streak: 0")
        self.game_score_lbl.grid(row=size + 2, column=0, columnspan=size, pady=(10, 0))

        # Back button
        game_back_btn = ctk.CTkButton(self.game_frame, text="Back", command=self.back_to_menu)
        game_back_btn.grid(row=size + 3, column=0, columnspan=size, pady=(10, 0))

    # Create finish UI
    def _build_finish_ui(self):
        # -- Labels --
        self.finish_main_lbl = ctk.CTkLabel(self.finish_frame, text="", justify="center")
        self.finish_main_lbl.grid(row=0, column=0, padx=LABEL_SIZE, pady=LABEL_SIZE)

        # -- Buttons --
        finish_back_btn = ctk.CTkButton(self.finish_frame, text="Back", command=self.back_to_menu)
        finish_back_btn.grid(row=1, column=0, padx=BUTTON_SIZE, pady=BUTTON_SIZE)

    # Check logic in GameLogic
    def on_card_click(self, row, col):
        # Indexing
        idx = self._card_index(row, col)
        card = self.game_logic.cards[idx]

        # Open button
        opened_now = self.game_logic.on_click(card)
        if not opened_now:
            return

        # Flip animation
        self._animate_flip(idx, card.value)

        # Clicks update
        self.game_clicks_lbl.configure(text=f"Clicks: {self.game_logic.clicks}")

        # Check first_card == second_cars
        if len(self.game_logic.opened) == 2:
            self.root.after(CHECK_DELAY, self._resolve_check)

    # Animation flips
    def _animate_flip(self, idx, new_text, steps=FLIP_STEPS, delay=FLIP_DELAY):
        # Get button
        btn = self.buttons[idx]
        original_width = btn.cget("width")

        # Hard math, 1 -> 0.5 -> change text
        def shrink(step):
            if step <= steps // 2:
                width = original_width * (1 - step / (steps // 2))
                btn.configure(width=max(int(width), 1))
                aid = self.root.after(delay, lambda: shrink(step + 1))
                self.animation_after_ids.append(aid)
            else:
                btn.configure(text=new_text)
                grow(step)

        # Reverse hard math, 0.5 -> 1
        def grow(step):
            if step <= steps:
                progress = (step - steps // 2) / (steps // 2)
                width = original_width * progress
                btn.configure(width=max(int(width), 1))
                aid = self.root.after(delay, lambda: grow(step + 1))
                self.animation_after_ids.append(aid)
            else:
                btn.configure(width=original_width)

        shrink(0)

    # Check to True
    def _resolve_check(self):
        # Get return in check_match
        result = self.game_logic.check_match()
        self._update_score(result)
        # Get first and second
        for card in(result["first_card"], result["second_card"]):
            idx = self._card_index(card.row, card.col)
            btn = self.buttons[idx]
            if result["is_match"]:
                # Change bg color if True
                btn.configure(fg_color="green")
            else:
                self._animate_flip(idx, "?")

        # Check to win
        if result["game_won"]:
            self.finish_game(result)

    # UI update timer
    def _update_timer(self):
        # if false or false -> Stop
        if not self.game_logic or not self.game_logic.timer_running:
            return
        
        # Get lact tick
        self.game_logic.tick()

        # Get min and sec
        minutes, seconds = divmod(self.game_logic.seconds_passed, TIMER_MIN)

        # Change timer in the last time
        self.game_timer_lbl.configure(text=f"Time: {minutes}:{seconds:02d}")
        self.timer_after_id = self.root.after(TIMER_DELAY, self._update_timer)

    # Stop all logics
    def _cancel_pending_callbacks(self):
        # Check IDs
        if self.timer_after_id:
            self.root.after_cancel(self.timer_after_id)
            self.timer_after_id = None

        # For pid close
        for aid in self.animation_after_ids:
            self.root.after_cancel(aid)
        self.animation_after_ids.clear()

    # Stop logic
    def finish_game(self, result):
        # Stop processes
        self._cancel_pending_callbacks()
        self.game_logic.stop_timer()

        # Get min and sec to change in finish
        minutes, seconds = divmod(self.game_logic.seconds_passed, TIMER_MIN)

        # Cange finish label
        self.finish_main_lbl.configure(
            text=f"You are stupid guy!\n\nTime: {minutes}:{seconds:02d}\nClicks: {self.game_logic.clicks}\nScore: {result["score"]}"
        )

        # Show finish Ui
        self._show_finish()

    # Logic back to menu
    def back_to_menu(self):
        # Stop processes
        self._cancel_pending_callbacks()
        if self.game_logic:
            self.game_logic.stop_timer()

        # Change to bacis value
        self.game_logic = None

        # Change Ui to menu
        self._show_menu()

    # Hide all frames, show only the given one
    def _switch_frame(self, frame):
        for f in (self.menu_frame, self.game_frame, self.finish_frame):
            f.pack_forget()
        frame.pack(expand=True)

    # Logic changing size place
    def _on_size_change(self, value):
        self.selected_size = value

    # Row/col -> flat index
    def _card_index(self, row, col):
        return row * self.game_logic.size + col

    # Update label score, streak
    def _update_score(self, result):
        self.game_score_lbl.configure(text=f"Score: {result["score"]}, Streak: {result["streak"]}")