"""Application-facing Python API for Mompy."""

from __future__ import annotations

from pathlib import Path

from .briefings import briefing_for_mission_index, get_briefing, get_briefings
from .code_runner import run_user_code_safely
from .lessons import get_lessons
from .missions import get_current_mission, get_mission, get_missions
from .profile import load_profile, logout_profile, save_profile
from .progress import complete_mission, load_progress, reset_progress
from .validator import validate_mission


class MompyAPI:
    """Small in-process API that pywebview can expose in phase 10.3."""

    def __init__(self, progress_path: Path | None = None) -> None:
        self.progress_path = progress_path

    def get_bootstrap_state(self) -> dict:
        return {
            "backend": {
                "name": "Mompy Python Backend",
                "phase": "10.3",
                "connected": True,
            },
            "profile": self.get_profile(),
            "progress": self.get_progress(),
            "current_mission": self.get_current_mission(),
            "missions": self.get_missions(),
            "lessons": self.get_lessons(),
            "briefings": self.get_briefings(),
            "next_briefing": self.get_next_briefing(),
        }

    def get_missions(self) -> list[dict]:
        return get_missions()

    def get_lessons(self) -> list[dict]:
        return get_lessons()

    def get_briefings(self) -> list[dict]:
        return get_briefings()

    def get_briefing(self, briefing_id: str) -> dict | None:
        return get_briefing(briefing_id)

    def get_next_briefing(self) -> dict | None:
        progress = self.get_progress()
        return briefing_for_mission_index(progress["current_mission_index"])

    def get_profile(self) -> dict:
        return load_profile()

    def save_profile(self, profile: dict) -> dict:
        return save_profile(profile)

    def logout_profile(self) -> dict:
        return logout_profile()

    def get_progress(self) -> dict:
        if self.progress_path is None:
            return load_progress()
        return load_progress(self.progress_path)

    def get_current_mission(self) -> dict:
        progress = self.get_progress()
        return get_current_mission(progress["current_mission_index"]).to_dict()

    def validate_mission(self, mission_id: str, user_code: str) -> dict:
        return validate_mission(mission_id, user_code)

    def complete_mission(self, mission_id: str) -> dict:
        if get_mission(mission_id) is None:
            raise ValueError(f"Unknown mission id: {mission_id}")
        if self.progress_path is None:
            return complete_mission(mission_id)
        return complete_mission(mission_id, self.progress_path)

    def reset_progress(self) -> dict:
        if self.progress_path is None:
            return reset_progress()
        return reset_progress(self.progress_path)

    def run_user_code_safely(self, user_code: str) -> dict:
        return run_user_code_safely(user_code)

    def check_answer(self, mission_id: str, user_code: str) -> dict:
        validation = self.validate_mission(mission_id, user_code)
        if validation["correct"]:
            validation["progress"] = self.complete_mission(mission_id)
        return validation
