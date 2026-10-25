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
        game.players[0].clicks = 4
        game.players[0].score = 20
        game.players[0].streak = 2

        game.generate_cards()

        self.assertEqual(len(game.cards), 16)
        self.assertEqual(game.opened, [])
        self.assertEqual(game.matched_count, 0)
        self.assertEqual(game.seconds_passed, 0)
        self.assertEqual(game.current_player_id, 0)
        self.assertEqual(game.players[0].clicks, 0)
        self.assertEqual(game.players[0].score, 0)
        self.assertEqual(game.players[0].streak, 0)
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
    def test_click_rejects_cards_outside_the_board(self):
        game = GameLogic(2, make_players())
        game.generate_cards()
        foreign_card = Card("🍎", 9, 9)

        self.assertFalse(game.on_click(foreign_card))
        self.assertEqual(game.opened, [])
        self.assertEqual(game.current_player().clicks, 0)

    def test_click_rejects_a_third_card_while_a_pair_is_open(self):
        game = GameLogic(2, make_players())
        game.generate_cards()
        first, second, third = game.cards[:3]

        self.assertTrue(game.on_click(first))
        self.assertTrue(game.on_click(second))
        self.assertFalse(game.on_click(third))

        self.assertEqual(game.opened, [first, second])
        self.assertEqual(game.current_player().clicks, 2)
        self.assertFalse(third.is_open)

    def test_check_match_requires_exactly_two_open_cards(self):
        game = GameLogic(2, make_players())

        for count in (0, 1, 3):
            with self.subTest(open_card_count=count):
                game.opened = [Card("🍎", 0, index) for index in range(count)]

                with self.assertRaisesRegex(ValueError, "exactly two open cards"):
                    game.check_match()

    def test_matching_pair_scores_and_ends_a_completed_game(self):
        players = make_players()
        game = GameLogic(2, players)
        first = Card("🍎", 0, 0)
        second = Card("🍎", 0, 1)
        game.cards = [first, second]
        game.opened = [first, second]
        game.timer_running = True

        result = game.check_match()

        self.assertTrue(result["is_match"])
        self.assertTrue(result["game_won"])
        self.assertTrue(first.is_matched)
        self.assertTrue(second.is_matched)
        self.assertEqual(players[0].score, 10)
        self.assertEqual(players[0].streak, 1)
        self.assertEqual(game.current_player_id, 0)
        self.assertFalse(game.timer_running)

        first.is_matched = False
        first.is_open = False
        self.assertFalse(game.on_click(first))

    def test_consecutive_matches_grow_streak_and_keep_the_turn(self):
        players = make_players()
        game = GameLogic(2, players)
        first_pair = [Card("🍎", 0, 0), Card("🍎", 0, 1)]
        second_pair = [Card("🍌", 1, 0), Card("🍌", 1, 1)]
        game.cards = first_pair + second_pair
        game.timer_running = True

        game.opened = list(first_pair)
        first_result = game.check_match()

        self.assertFalse(first_result["game_won"])
        self.assertEqual(players[0].score, 10)
        self.assertEqual(players[0].streak, 1)
        self.assertEqual(game.current_player_id, 0)
        self.assertTrue(game.timer_running)

        game.opened = list(second_pair)
        second_result = game.check_match()

        self.assertTrue(second_result["game_won"])
        self.assertEqual(players[0].score, 30)
        self.assertEqual(players[0].streak, 2)
        self.assertEqual(game.current_player_id, 0)
        self.assertFalse(game.timer_running)

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


class GameLogicWinnerTests(unittest.TestCase):
    def test_player_with_higher_score_wins(self):
        for first_score, second_score, expected_index in (
            (30, 10, 0),
            (10, 30, 1),
        ):
            with self.subTest(first_score=first_score, second_score=second_score):
                players = make_players()
                players[0].score = first_score
                players[1].score = second_score
                game = GameLogic(2, players)

                self.assertIs(game.get_winner(), players[expected_index])

    def test_equal_scores_are_a_draw(self):
        players = make_players()
        players[0].score = players[1].score = 30
        game = GameLogic(2, players)

        self.assertIsNone(game.get_winner())


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
