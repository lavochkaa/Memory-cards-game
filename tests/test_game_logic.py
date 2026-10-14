import unittest

from core.game_logic import GameLogic
from core.models import Player, User


def make_players():
    return [Player(User("Alice")), Player(User("Bob"))]


class GameLogicGenerateCardsTests(unittest.TestCase):
    def test_generate_cards_starts_a_fresh_round(self):
        game = GameLogic(4, make_players())
        game.generate_cards()

        game.opened.extend(game.cards[:2])
        game.matched_count = 2
        game.seconds_passed = 19
        game.current_player_id = 1

        game.generate_cards()

        self.assertEqual(len(game.cards), 16)
        self.assertEqual(game.opened, [])
        self.assertEqual(game.matched_count, 0)
        self.assertEqual(game.seconds_passed, 0)
        self.assertEqual(game.current_player_id, 0)
        self.assertTrue(game.timer_running)

    def test_generate_cards_rejects_board_larger_than_available_pairs(self):
        game = GameLogic(10, make_players())

        with self.assertRaises(ValueError):
            game.generate_cards()

    def test_generate_cards_rejects_odd_board_sizes(self):
        game = GameLogic(3, make_players())

        with self.assertRaises(ValueError):
            game.generate_cards()


if __name__ == "__main__":
    unittest.main()
