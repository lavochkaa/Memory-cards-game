import random
from models import Card

# -- Constants --
EMOJIS = [
    "🍎", "🍌", "🍇", "🍒", "🍉", "🥝", "🍑", "🍓",
    "🍋", "🍊", "🍍", "🥥", "🍈", "🍏", "🥭", "🍐",
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼",
    "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🦄"
]
POINTS_MATCH = 10
TIMER_MIN = 60

# -- Game logic --
class GameLogic:
    # Basic selfs
    def __init__(self, size, players):
        # Get size
        self.size = size

        # -- Players --
        self.players = players

        # -- Masives --
        self.cards = []
        self.opened = []

        # -- Basic values --
        self.matched_count = 0
        self.seconds_passed = 0
        self.current_player_id = 0

        # -- Flags --
        self.timer_running = False

    # Start to generate cards
    def generate_cards(self):
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
                # Create card
                card = Card(values_flat[index], pos_x, pos_y)
                self.cards.append(card)

                # This sigma value forever
                index += 1

        # Start timer
        self.seconds_passed = 0
        self.timer_running = True

    # Click logic
    def on_click(self, card):
        # Check oppend or matched
        if card.is_open or card.is_matched or (len(self.opened) >= 2):
            return False

        # Do a flip and block
        card.is_open = True
        self.opened.append(card)

        # Save click
        self.current_player().clicks += 1

        return True

    # Ckeck values
    def check_match(self):
        # Get value1, value2
        first_card, second_card = self.opened
        is_match = first_card.value == second_card.value

        # Save to Player
        player = self.current_player()

        # if first_card == second_card -> cool
        if is_match:
            first_card.is_matched = True
            second_card.is_matched = True
            self.matched_count += 2

            player.streak += 1
            graind = POINTS_MATCH * player.streak
            player.score += graind
        else:
            first_card.is_open = False
            second_card.is_open = False
            player.streak = 0
            self.switch_turn()

        # Clear opened cards and close
        self.opened.clear()

        # Return this shit
        return {
            "is_match": is_match,
            "first_card": first_card,
            "second_card": second_card,
            "game_won": self.matched_count == len(self.cards),
        }

    # Advance the clock by one second
    def tick(self):
        self.seconds_passed += 1

    # Stop the clock
    def stop_timer(self):
        self.timer_running = False

    def current_player(self):
        return self.players[self.current_player_id]

    def switch_turn(self):
        self.current_player_id = 1 - self.current_player_id

    def get_winner(self):
        player1 = self.players[0]
        player2 = self.players[1]

        if player1.score == player2.score:
            return None

        if player1.score > player2.score:
            return player1

        return player2