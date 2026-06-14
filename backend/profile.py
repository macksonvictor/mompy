"""Local user profile helpers."""

from __future__ import annotations

from pathlib import Path

from .storage import read_json, resolve_data_path, write_json


PROFILE_PATH = resolve_data_path("profile.json")
DEFAULT_PROFILE = {
    "name": "Guest",
    "created_at": None,
    "last_seen_at": None,
    "settings": {
        "music_enabled": True,
        "sfx_enabled": True,
        "music_volume": 0.10,
        "sfx_volume": 0.45,
    },
}


def _clean_name(name: str) -> str:
    clean = " ".join((name or "").strip().split())
    if not clean:
        return DEFAULT_PROFILE["name"]
    return clean[:24]


def load_profile(path: Path = PROFILE_PATH) -> dict:
    profile = read_json(path, DEFAULT_PROFILE.copy())
    if not isinstance(profile, dict):
        profile = DEFAULT_PROFILE.copy()
    merged = DEFAULT_PROFILE.copy()
    merged.update(profile)
    merged["name"] = _clean_name(str(merged.get("name", "")))
    settings = DEFAULT_PROFILE["settings"].copy()
    if isinstance(profile.get("settings"), dict):
        settings.update(profile["settings"])
    merged["settings"] = settings
    return merged


def save_profile(profile: dict, path: Path = PROFILE_PATH) -> dict:
    current = load_profile(path)
    current.update(profile)
    current["name"] = _clean_name(str(current.get("name", "")))
    write_json(path, current)
    return current


def logout_profile(path: Path = PROFILE_PATH) -> dict:
    profile = DEFAULT_PROFILE.copy()
    write_json(path, profile)
    return load_profile(path)
