import tempfile
import unittest
from pathlib import Path

from backend.progress import complete_mission, load_progress, reset_progress


class ProgressTests(unittest.TestCase):
    def test_reset_progress_creates_default_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            progress = reset_progress(path)
            self.assertEqual(progress["current_mission_index"], 0)
            self.assertEqual(progress["completed_mission_ids"], [])
            self.assertEqual(progress["total_xp"], 0)

    def test_complete_mission_adds_xp_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            complete_mission("mission_001", path)
            progress = complete_mission("mission_001", path)
            self.assertEqual(progress["completed_mission_ids"], ["mission_001"])
            self.assertEqual(progress["total_xp"], 35)

    def test_load_progress_sanitizes_unknown_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            path.write_text(
                '{"completed_mission_ids":["bad","mission_001"],"current_mission_index":99}',
                encoding="utf-8",
            )
            progress = load_progress(path)
            self.assertEqual(progress["completed_mission_ids"], ["mission_001"])
            self.assertEqual(progress["current_mission_index"], 19)


if __name__ == "__main__":
    unittest.main()
