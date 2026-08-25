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

# -- Game logic --
class GameLogic:
    # Basic selfs
    def __init__(self, size):
        # Get size
        self.size = size

        # -- Masives --
        self.cards = []
        self.opened = []

        # -- Basic values --
        self.clicks = 0
        self.matched_count = 0
        self.seconds_passed = 0
        self.score = 0
        self.streak = 0

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
        self.clicks += 1

        return True

    # Ckeck values
    def check_match(self):
        # Get value1, value2
        first_card, second_card = self.opened
        is_match = first_card.value == second_card.value

        # if first_card == second_card -> cool
        graind = 0
        if is_match:
            first_card.is_matched = True
            second_card.is_matched = True
            self.matched_count += 2

            self.streak += 1
            graind = POINTS_MATCH * self.streak
            self.score += graind
        else:
            first_card.is_open = False
            second_card.is_open = False
            self.streak = 0

        # Clear opened cards and close
        self.opened.clear()

        # Return this shit
        return {
            "is_match": is_match,
            "first_card": first_card,
            "second_card": second_card,
            "game_won": self.matched_count == len(self.cards),
            "score": self.score,
            "streak": self.streak,
        }

    # Advance the clock by one second
    def tick(self):
        self.seconds_passed += 1

    # Stop the clock
    def stop_timer(self):
        self.timer_running = False