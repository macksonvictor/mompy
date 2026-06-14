import unittest

from backend.xp import calculate_level, xp_required_for_level


class XpTests(unittest.TestCase):
    def test_level_one_starts_at_zero_xp(self):
        info = calculate_level(0)
        self.assertEqual(info["level"], 1)
        self.assertEqual(info["title"], "Beginner")

    def test_level_two_requires_more_than_one_mission(self):
        self.assertEqual(xp_required_for_level(2), 100)
        self.assertEqual(calculate_level(35)["level"], 1)
        self.assertEqual(calculate_level(100)["level"], 2)

    def test_level_titles_scale(self):
        self.assertEqual(calculate_level(xp_required_for_level(6))["title"], "Apprentice")
        self.assertEqual(calculate_level(xp_required_for_level(15))["title"], "Builder")


if __name__ == "__main__":
    unittest.main()
