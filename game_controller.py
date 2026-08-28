import customtkinter as ctk
from models import User, Player
from room import Room

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
        self.login_frame = ctk.CTkFrame(root)
        self.menu_frame = ctk.CTkFrame(root)
        self.waiting_frame = ctk.CTkFrame(root)
        self.game_frame = ctk.CTkFrame(root)
        self.finish_frame = ctk.CTkFrame(root)

        # -- Values --
        self.game_logic = None
        self.timer_after_id = None
        self.selected_size = "4x4"
        self.buttons = []
        self.animation_after_ids = []

        # -- Atributs --
        self._build_login_ui()
        self._build_menu_ui()
        self._build_waiting_ui()
        self._build_finish_ui()
        self._show_login()

    # Start game
    def start_game(self):
        # Clear pids
        self._cancel_pending_callbacks()

        # Size to int value
        size = int(self.selected_size.split('x')[0])

        # Start logic
        self.players = [
            Player(User(self.username)),
            Player(User("User2"))
        ]

        self.room = Room(size, self.players)
        self.game_logic = self.room.game_logic
        self.game_logic.generate_cards()

        # Start funcions
        self._build_game_ui(size)
        self._update_timer()
        self._show_game()

    def _show_login(self):
        self._switch_frame(self.login_frame)

    # Close all and open menu
    def _show_menu(self):
        self._switch_frame(self.menu_frame)

    def _show_waiting(self):
        self._switch_frame(self.waiting_frame)

    # Close all and open gmae
    def _show_game(self):
        self._switch_frame(self.game_frame)

    # Close all and open finish
    def _show_finish(self):
        self._switch_frame(self.finish_frame)

    def _build_login_ui(self):
        self.login_frame.grid_columnconfigure(0, weight=1)

        # -- Labels --
        login_main_lbl = ctk.CTkLabel(self.login_frame, text="Enter username")
        login_main_lbl.grid(row=0, column=0, padx=LABEL_SIZE, pady=LABEL_SIZE, sticky="ew")

        # -- Input --
        self.login_input_etr = ctk.CTkEntry(self.login_frame, placeholder_text="username")
        self.login_input_etr.grid(row=1, column=0)

        # -- Buttons --
        login_continue_btn = ctk.CTkButton(self.login_frame, text="Continue", command=self.login)
        login_continue_btn.grid(row=3, column=0, padx=MENU_BUTTON_SIZE, pady=MENU_BUTTON_SIZE, sticky="ew")

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
        menu_start_btn = ctk.CTkButton(self.menu_frame, text="Start", command=self.join_room)
        menu_start_btn.grid(row=2, column=0, padx=MENU_BUTTON_SIZE, pady=MENU_BUTTON_SIZE, sticky="ew")

    def _build_waiting_ui(self):
        self.waiting_frame.grid_columnconfigure(0, weight=1)

        # -- Labels --
        waiting_main_lbl = ctk.CTkLabel(self.waiting_frame, text="Waiting...")
        waiting_main_lbl.grid(row=0, column=0, padx=LABEL_SIZE, pady=LABEL_SIZE, sticky="ew")

    # Build only widgets
    def _build_game_ui(self, size):
        # -- Players --
        player1 = self.game_logic.players[0]
        player2 = self.game_logic.players[1]
        
        # Clear all
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.buttons.clear()

        self.game_frame.grid_columnconfigure(0, weight=1)
        self.game_frame.grid_columnconfigure(1, weight=0)
        self.game_frame.grid_columnconfigure(2, weight=1)
        self.game_frame.grid_rowconfigure(0, weight=1)

        self.left_user_frame = ctk.CTkFrame(self.game_frame)
        self.left_user_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=20)

        self.board_frame = ctk.CTkFrame(self.game_frame)
        self.board_frame.grid(row=0, column=1, padx=20, pady=20)

        self.right_user_frame = ctk.CTkFrame(self.game_frame)
        self.right_user_frame.grid(row=0, column=2, sticky="ne", padx=20, pady=20)

        # Create buttons
        for row in range(size):
            for col in range(size):
                btn = ctk.CTkButton(
                    self.board_frame,
                    text="?",
                    width=CARD_SIZE,
                    height=CARD_SIZE,
                    command=lambda r=row, c=col: self.on_card_click(r, c))
                btn.grid(row=row, column=col, padx=BUTTON_SIZE, pady=BUTTON_SIZE)
                self.buttons.append(btn)

        # Timer
        self.game_timer_lbl = ctk.CTkLabel(self.board_frame, text="Time: 0:00")
        self.game_timer_lbl.grid(row=size, column=0, columnspan=size, pady=(10, 0))

        # Turn label
        self.game_current_turn_lbl = ctk.CTkLabel(self.board_frame, text=f"Turn: {player1.user.username}")
        self.game_current_turn_lbl.grid(row=size + 1, column=0, columnspan=size, pady=(10, 0))

        # Users status
        self.game_player1_lbl = ctk.CTkLabel(self.left_user_frame, text=f"{player1.user.username}\n- Score: 0\n- Streak: 0\n- Clicks: 0")
        self.game_player1_lbl.pack(padx=15, pady=15)
        
        self.game_player2_lbl = ctk.CTkLabel(self.right_user_frame, text=f"{player2.user.username}\n- Score: 0\n- Streak: 0\n- Clicks: 0")
        self.game_player2_lbl.pack(padx=15, pady=15)

        # Back button
        game_back_btn = ctk.CTkButton(self.board_frame, text="Back", command=self.back_to_menu)
        game_back_btn.grid(row=size + 4, column=0, columnspan=size, pady=(10, 0))

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
        self._update_players_info()

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
        self._update_players_info()
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
            self.finish_game()

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
    def finish_game(self):
        # Stop processes
        self._cancel_pending_callbacks()
        self.game_logic.stop_timer()

        # Check winner
        winner = self.game_logic.get_winner()
        minutes, seconds = divmod(self.game_logic.seconds_passed, TIMER_MIN)

        if winner is None:
            finish_text = (
                "DRAW!\n\n"
                f"Time: {minutes}:{seconds:02d}"
            )
        else:
            finish_text = (
                f"Winner: {winner.user.username}\n\n"
                f"Clicks: {winner.clicks}\n"
                f"Score: {winner.score}\n"
                f"Time: {minutes}:{seconds:02d}"
            )

        # Cange finish label
        self.finish_main_lbl.configure(text=finish_text)

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
        # All frames
        frames = [
            self.login_frame,
            self.menu_frame,
            self.waiting_frame,
            self.game_frame,
            self.finish_frame
        ]

        for f in frames:
            f.pack_forget()
        if frame == self.game_frame:
            frame.pack(fill="both", expand=True)
        else:
            frame.pack(expand=True)

    # Logic changing size place
    def _on_size_change(self, value):
        self.selected_size = value

    # Row/col -> flat index
    def _card_index(self, row, col):
        return row * self.game_logic.size + col

    def _update_players_info(self):
        # -- Players --
        player1 = self.game_logic.players[0]
        player2 = self.game_logic.players[1]
        current_player = self.game_logic.current_player()

        self.game_current_turn_lbl.configure(text=f"Turn: {current_player.user.username}")

        self.game_player1_lbl.configure(
            text=f"{player1.user.username}\n- Score: {player1.score}\n- Streak: {player1.streak}\n- Clicks: {player1.clicks}"
        )

        self.game_player2_lbl.configure(
            text=f"{player2.user.username}\n- Score: {player2.score}\n- Streak: {player2.streak}\n- Clicks: {player2.clicks}"
        )

    def join_room(self):
        self._show_waiting()
        # TODO - server GET
        self.root.after(TIMER_DELAY * 3, self.start_game)

    def login(self):
        self.username = self.login_input_etr.get()

        if self.username == "":
            self.username = "User1"

        self._show_menu()