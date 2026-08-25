from dataclasses import dataclass

@dataclass
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

# TODO - multiplayer
class User:
    # -- Inits __
    def __init__(self):
        pass