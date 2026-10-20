import sys
import types
import unittest


sys.modules.setdefault("customtkinter", types.SimpleNamespace())

from client.game_controller import CHECK_DELAY, FLIP_DELAY, FLIP_STEPS, GameController
from core.models import Card


class FakeRoot:
    def __init__(self):
        self.cancelled_callbacks = []
        self.scheduled_callbacks = []

    def after_cancel(self, callback_id):
        self.cancelled_callbacks.append(callback_id)

    def after(self, delay, callback):
        callback_id = f"callback-{len(self.scheduled_callbacks)}"
        self.scheduled_callbacks.append((callback_id, delay, callback))
        return callback_id


class FakeLabel:
    def __init__(self):
        self.text = None

    def configure(self, *, text):
        self.text = text


class FakeGameLogic:
    def __init__(self):
        self.seconds_passed = 0
        self.timer_running = True

    def tick(self):
        self.seconds_passed += 1

    def stop_timer(self):
        self.timer_running = False


class FakeClickGameLogic:
    def __init__(self):
        self.size = 2
        self.cards = [Card("🍎", 0, 0)]
        self.opened = []
        self.click_attempts = 0

    def on_click(self, card):
        self.click_attempts += 1
        self.opened.append(card)
        return True


class FakeMismatchGameLogic:
    def __init__(self):
        self.size = 2
        self.first_card = Card("🍎", 0, 0)
        self.second_card = Card("🍌", 0, 1)

    def check_match(self):
        return {
            "is_match": False,
            "first_card": self.first_card,
            "second_card": self.second_card,
            "game_won": False,
        }


class GameControllerCallbackTests(unittest.TestCase):
    def test_join_room_schedules_only_one_game_start(self):
        controller = GameController.__new__(GameController)
        controller.root = FakeRoot()
        controller.waiting_after_id = None
        controller._show_waiting = lambda: None
        starts = []
        controller.start_game = lambda: starts.append(True)

        controller.join_room()
        controller.join_room()

        self.assertEqual(len(controller.root.scheduled_callbacks), 1)
        controller.root.scheduled_callbacks[0][2]()
        self.assertEqual(starts, [True])
        self.assertIsNone(controller.waiting_after_id)

    def test_ignores_card_clicks_while_pair_resolution_is_locked(self):
        controller = GameController.__new__(GameController)
        controller.game_logic = FakeClickGameLogic()
        controller.input_locked = True

        controller.on_card_click(0, 0)

        self.assertEqual(controller.game_logic.click_attempts, 0)

    def test_mismatched_pair_keeps_input_locked_until_flip_back_finishes(self):
        controller = GameController.__new__(GameController)
        controller.root = FakeRoot()
        controller.game_logic = FakeMismatchGameLogic()
        controller.match_after_id = "match-check"
        controller.input_locked = True
        controller.buttons = [object(), object()]
        animated_cards = []
        controller._update_players_info = lambda: None
        controller._animate_flip = lambda index, text: animated_cards.append((index, text))

        controller._resolve_check()

        self.assertTrue(controller.input_locked)
        self.assertEqual(animated_cards, [(0, "?"), (1, "?")])
        self.assertEqual(controller.root.scheduled_callbacks[0][1], FLIP_DELAY * (FLIP_STEPS + 2))

        controller.root.scheduled_callbacks[0][2]()

        self.assertFalse(controller.input_locked)

    def test_cancels_pending_match_check(self):
        controller = GameController.__new__(GameController)
        controller.root = FakeRoot()
        controller.timer_after_id = None
        controller.match_after_id = "match-check"
        controller.input_unlock_after_id = None
        controller.waiting_after_id = None
        controller.input_locked = True
        controller.animation_after_ids = []

        controller._cancel_pending_callbacks()

        self.assertEqual(controller.root.cancelled_callbacks, ["match-check"])
        self.assertIsNone(controller.match_after_id)

    def test_timer_displays_zero_before_the_first_second(self):
        controller = GameController.__new__(GameController)
        controller.root = FakeRoot()
        controller.game_logic = FakeGameLogic()
        controller.game_timer_lbl = FakeLabel()

        controller._update_timer()

        self.assertEqual(controller.game_timer_lbl.text, "Time: 0:00")
        self.assertEqual(controller.game_logic.seconds_passed, 0)
        self.assertEqual(controller.root.scheduled_callbacks[0][1], 1000)

        controller.root.scheduled_callbacks[0][2]()

        self.assertEqual(controller.game_timer_lbl.text, "Time: 0:01")
        self.assertEqual(controller.game_logic.seconds_passed, 1)

    def test_returning_to_menu_cancels_game_callbacks_and_stops_timer(self):
        controller = GameController.__new__(GameController)
        controller.root = FakeRoot()
        controller.timer_after_id = "timer"
        controller.match_after_id = "match-check"
        controller.input_unlock_after_id = "input-unlock"
        controller.waiting_after_id = "waiting-start"
        controller.input_locked = True
        controller.animation_after_ids = ["flip-animation"]
        game_logic = FakeGameLogic()
        controller.game_logic = game_logic
        controller.menu_was_shown = False
        controller._show_menu = lambda: setattr(controller, "menu_was_shown", True)

        controller.back_to_menu()

        self.assertEqual(
            controller.root.cancelled_callbacks,
            ["timer", "match-check", "input-unlock", "waiting-start", "flip-animation"],
        )
        self.assertFalse(game_logic.timer_running)
        self.assertIsNone(controller.game_logic)
        self.assertFalse(controller.input_locked)
        self.assertTrue(controller.menu_was_shown)


if __name__ == "__main__":
    unittest.main()
