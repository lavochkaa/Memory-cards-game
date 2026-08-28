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
    # -- Inits __
    def __init__(self, name):
        self.name = name
        self.clicks = 0
        self.score = 0
        self.streak = 0

# TODO - multiplayer room 
class Room:
    def __init__(self):
        pass
