import tempfile
import unittest
from pathlib import Path

from backend.api import MompyAPI


class ApiTests(unittest.TestCase):
    def test_api_lists_missions_and_lessons(self):
        api = MompyAPI()
        self.assertEqual(len(api.get_missions()), 30)
        self.assertGreaterEqual(len(api.get_lessons()), 6)
        mission = api.get_missions()[0]
        self.assertIn("starterCode", mission)
        self.assertIn("expectedOutput", mission)

    def test_check_answer_can_complete_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            api = MompyAPI(progress_path=Path(tmp) / "progress.json")
            result = api.check_answer("mission_001", 'print("Hello, Mompy!")')
            self.assertTrue(result["correct"])
            self.assertIn("progress", result)
            self.assertEqual(result["progress"]["completed_mission_ids"], ["mission_001"])

    def test_bootstrap_state_contains_frontend_bridge_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            api = MompyAPI(progress_path=Path(tmp) / "progress.json")
            state = api.get_bootstrap_state()

            self.assertTrue(state["backend"]["connected"])
            self.assertEqual(state["backend"]["phase"], "10.5")
            self.assertIn("profile", state)
            self.assertIn("progress", state)
            self.assertEqual(state["current_mission"]["id"], "mission_001")
            self.assertEqual(len(state["missions"]), 30)
            self.assertGreaterEqual(len(state["lessons"]), 6)


if __name__ == "__main__":
    unittest.main()
