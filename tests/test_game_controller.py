import sys
import types
import unittest


sys.modules.setdefault("customtkinter", types.SimpleNamespace())

from client.game_controller import GameController


class FakeRoot:
    def __init__(self):
        self.cancelled_callbacks = []

    def after_cancel(self, callback_id):
        self.cancelled_callbacks.append(callback_id)


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


if __name__ == "__main__":
    unittest.main()
