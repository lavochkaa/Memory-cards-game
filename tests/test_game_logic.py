import unittest

from core.game_logic import GameLogic
from core.models import Card, Player, User


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


class GameLogicMatchTests(unittest.TestCase):
    def test_matching_pair_scores_and_ends_a_completed_game(self):
        players = make_players()
        game = GameLogic(2, players)
        first = Card("🍎", 0, 0)
        second = Card("🍎", 0, 1)
        game.cards = [first, second]
        game.opened = [first, second]

        result = game.check_match()

        self.assertTrue(result["is_match"])
        self.assertTrue(result["game_won"])
        self.assertTrue(first.is_matched)
        self.assertTrue(second.is_matched)
        self.assertEqual(players[0].score, 10)
        self.assertEqual(players[0].streak, 1)
        self.assertEqual(game.current_player_id, 0)

    def test_mismatched_pair_closes_cards_and_switches_turn(self):
        players = make_players()
        game = GameLogic(2, players)
        first = Card("🍎", 0, 0)
        second = Card("🍌", 0, 1)
        first.is_open = True
        second.is_open = True
        players[0].streak = 2
        game.cards = [first, second]
        game.opened = [first, second]

        result = game.check_match()

        self.assertFalse(result["is_match"])
        self.assertFalse(first.is_open)
        self.assertFalse(second.is_open)
        self.assertEqual(players[0].streak, 0)
        self.assertEqual(game.current_player_id, 1)


class GameLogicTimerTests(unittest.TestCase):
    def test_tick_does_not_advance_after_timer_stops(self):
        game = GameLogic(4, make_players())
        game.generate_cards()
        game.tick()

        game.stop_timer()
        game.tick()

        self.assertEqual(game.seconds_passed, 1)


class GameLogicPlayerValidationTests(unittest.TestCase):
    def test_requires_exactly_two_players(self):
        one_player = [Player(User("Alice"))]
        three_players = make_players() + [Player(User("Cara"))]

        with self.assertRaises(ValueError):
            GameLogic(4, one_player)

        with self.assertRaises(ValueError):
            GameLogic(4, three_players)


if __name__ == "__main__":
    unittest.main()
