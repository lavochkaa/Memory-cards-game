from dataclasses import dataclass

class User:
    # -- Inits --
    def __init__(self, username):
        # Get username
        self.username = username

        # -- Values --
        self.global_score = 0
        self.game_played = 0
        self.wins = 0

class Player:
    # -- Inits --
    def __init__(self, user):
        # Get user
        self.user = user

        # -- Values --
        self.clicks = 0
        self.score = 0
        self.streak = 0

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
