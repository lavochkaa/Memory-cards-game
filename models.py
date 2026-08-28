from dataclasses import dataclass

class Card:
    # -- Inits --
    def __init__(self, value, row, col):
        # Get values
        self.value = value
        self.row = row
        self.col = col

        # -- Flags --
        self.is_open = False
        self.is_matched = False

class User:
    # -- Inits --
    def __init__(self, username):
        self.username = username
        self.global_score = 0
        self.game_played = 0
        self.wins = 0

class Player:
    def __init__(self, user):
        self.user = user
        self.clicks = 0
        self.score = 0
        self.streak = 0
