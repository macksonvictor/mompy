import tempfile
import unittest
from pathlib import Path

from backend.briefings import briefing_for_mission_index, get_briefings
from backend.profile import load_profile, logout_profile, save_profile


class BriefingProfileTests(unittest.TestCase):
    def test_briefings_cover_current_blocks(self):
        briefings = get_briefings()
        self.assertGreaterEqual(len(briefings), 6)
        self.assertEqual(briefing_for_mission_index(0)["subtitle"], "Primeiros comandos em Python")

    def test_profile_name_is_sanitized(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "profile.json"
            profile = save_profile({"name": "  Mackson   Victor  "}, path)
            self.assertEqual(profile["name"], "Mackson Victor")
            self.assertEqual(load_profile(path)["name"], "Mackson Victor")

    def test_logout_resets_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "profile.json"
            save_profile({"name": "Mackson"}, path)
            profile = logout_profile(path)
            self.assertEqual(profile["name"], "Guest")


if __name__ == "__main__":
    unittest.main()
