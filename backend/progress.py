"""Progress management for Mompy."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .missions import MISSIONS, MISSIONS_BY_ID, PLANNED_TOTAL_MISSIONS
from .storage import PROGRESS_PATH, read_json, write_json
from .xp import calculate_level


def default_progress() -> dict:
    return {
        "current_mission_index": 0,
        "completed_mission_ids": [],
        "completed_briefing_ids": [],
        "skipped_briefing_ids": [],
        "total_xp": 0,
        "planned_total_missions": PLANNED_TOTAL_MISSIONS,
        "last_updated_at": None,
    }


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mission_xp(mission_id: str) -> int:
    mission = MISSIONS_BY_ID.get(mission_id)
    return mission.xp if mission else 0


def _sanitize_progress(progress: dict | None) -> dict:
    clean = default_progress()
    if not isinstance(progress, dict):
        return clean

    valid_ids = {mission.id for mission in MISSIONS}
    completed = progress.get("completed_mission_ids", [])
    if isinstance(completed, list):
        clean["completed_mission_ids"] = [
            mission_id for mission_id in dict.fromkeys(completed) if mission_id in valid_ids
        ]

    for key in ("completed_briefing_ids", "skipped_briefing_ids"):
        values = progress.get(key, [])
        if isinstance(values, list):
            clean[key] = [str(value) for value in dict.fromkeys(values)]

    index = progress.get("current_mission_index", 0)
    if isinstance(index, int):
        clean["current_mission_index"] = min(max(index, 0), max(0, len(MISSIONS) - 1))

    clean["total_xp"] = sum(_mission_xp(mission_id) for mission_id in clean["completed_mission_ids"])
    clean["last_updated_at"] = progress.get("last_updated_at")
    return clean


def load_progress(path: Path = PROGRESS_PATH) -> dict:
    progress = _sanitize_progress(read_json(path, default_progress()))
    progress["level_info"] = calculate_level(progress["total_xp"])
    return progress


def save_progress(progress: dict, path: Path = PROGRESS_PATH) -> None:
    write_json(path, _sanitize_progress(progress))


def complete_mission(mission_id: str, path: Path = PROGRESS_PATH) -> dict:
    if mission_id not in MISSIONS_BY_ID:
        raise ValueError(f"Unknown mission id: {mission_id}")

    progress = load_progress(path)
    completed = progress["completed_mission_ids"]
    if mission_id not in completed:
        completed.append(mission_id)

    mission_index = next(index for index, mission in enumerate(MISSIONS) if mission.id == mission_id)
    progress["current_mission_index"] = min(mission_index + 1, len(MISSIONS) - 1)
    progress["total_xp"] = sum(_mission_xp(item) for item in completed)
    progress["last_updated_at"] = _timestamp()
    save_progress(progress, path)
    return load_progress(path)


def mark_briefing_completed(briefing_id: str, path: Path = PROGRESS_PATH) -> dict:
    progress = load_progress(path)
    completed = progress["completed_briefing_ids"]
    if briefing_id not in completed:
        completed.append(briefing_id)
    progress["last_updated_at"] = _timestamp()
    save_progress(progress, path)
    return load_progress(path)


def reset_progress(path: Path = PROGRESS_PATH) -> dict:
    progress = default_progress()
    progress["last_updated_at"] = _timestamp()
    write_json(path, progress)
    return load_progress(path)
