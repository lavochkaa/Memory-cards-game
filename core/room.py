from core.game_logic import GameLogic

class Room:
    # -- Inits --
    def __init__(self, size, players):
        # Get players
        self.players = players

        # -- Values --
        self.status = "waiting"

        # Start room
        self.game_logic = GameLogic(size, self.players)
