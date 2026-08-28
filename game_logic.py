import random
from models import Card
from models import User

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
    def __init__(self, size):
        # Get size
        self.size = size

        # -- Users --
        self.users = [
            User("User1"),
            User("User2")
        ]

        # -- Masives --
        self.cards = []
        self.opened = []

        # -- Basic values --
        self.matched_count = 0
        self.seconds_passed = 0
        self.current_user_id = 0

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
        self.current_user().clicks += 1

        return True

    # Ckeck values
    def check_match(self):
        # Get value1, value2
        first_card, second_card = self.opened
        is_match = first_card.value == second_card.value

        # Save user
        user = self.current_user()

        # if first_card == second_card -> cool
        if is_match:
            first_card.is_matched = True
            second_card.is_matched = True
            self.matched_count += 2

            user.streak += 1
            graind = POINTS_MATCH * user.streak
            user.score += graind
        else:
            first_card.is_open = False
            second_card.is_open = False
            user.streak = 0
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

    def current_user(self):
        return self.users[self.current_user_id]

    def switch_turn(self):
        self.current_user_id = 1 - self.current_user_id

    def get_winner(self):
        # Get metrics
        user1 = self.users[0]
        user2 = self.users[1]
        
        # Get min and sec to change in finish
        minutes, seconds = divmod(self.seconds_passed, TIMER_MIN)

        if user1.score == user2.score:
            finish_text = (
                f"DRAW!\n\n"
                f"Time: {minutes}:{seconds:02d}\n\n"
                f"{user1.name} - Clicks: {user1.clicks} - Score: {user1.score}\n"
                f"{user2.name} - Clicks: {user2.clicks} - Score: {user2.score}"
            )
        elif user1.score > user2.score:
            winner = user1
            finish_text = (
                f"Winner: {winner.name}\n\n"
                f"Time: {minutes}:{seconds:02d}\n"
                f"Clicks: {winner.clicks}\n"
                f"Score: {winner.score}"
            )
        else:
            winner = user2
            finish_text = (
                f"Winner: {winner.name}\n\n"
                f"Time: {minutes}:{seconds:02d}\n"
                f"Clicks: {winner.clicks}\n"
                f"Score: {winner.score}"
            )
            
        return finish_text
