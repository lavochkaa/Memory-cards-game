from game_logic import GameLogic

class Room:
    def __init__(self, size, players):
        self.players = players
        self.status = "waiting"

        self.game_logic = GameLogic(size, self.players)
