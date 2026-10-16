import sys
import types
import unittest


sys.modules.setdefault("customtkinter", types.SimpleNamespace())

from client.game_controller import GameController


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


class GameControllerCallbackTests(unittest.TestCase):
    def test_cancels_pending_match_check(self):
        controller = GameController.__new__(GameController)
        controller.root = FakeRoot()
        controller.timer_after_id = None
        controller.match_after_id = "match-check"
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


if __name__ == "__main__":
    unittest.main()
