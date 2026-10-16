import unittest

from core.models import User


class UserTests(unittest.TestCase):
    def test_strips_whitespace_from_usernames(self):
        user = User("  Alice  ")

        self.assertEqual(user.username, "Alice")

    def test_rejects_blank_usernames(self):
        with self.assertRaisesRegex(ValueError, "must not be blank"):
            User("   ")


if __name__ == "__main__":
    unittest.main()
