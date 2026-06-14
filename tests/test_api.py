import tempfile
import unittest
from pathlib import Path

from backend.api import MompyAPI


class ApiTests(unittest.TestCase):
    def test_api_lists_missions_and_lessons(self):
        api = MompyAPI()
        self.assertGreaterEqual(len(api.get_missions()), 20)
        self.assertGreaterEqual(len(api.get_lessons()), 6)

    def test_check_answer_can_complete_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            api = MompyAPI(progress_path=Path(tmp) / "progress.json")
            result = api.check_answer("mission_001", 'print("Hello, Mompy!")')
            self.assertTrue(result["correct"])
            self.assertIn("progress", result)
            self.assertEqual(result["progress"]["completed_mission_ids"], ["mission_001"])


if __name__ == "__main__":
    unittest.main()
