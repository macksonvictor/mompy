"""XP and level rules for Mompy."""

from __future__ import annotations


MAX_LEVEL = 100


def xp_required_for_level(level: int) -> int:
    """Return total XP required to reach a level.

    This mirrors the frontend curve: level 1 starts at 0 XP and later levels
    grow non-linearly, so level 100 remains a long-term achievement.
    """

    if level <= 1:
        return 0
    return int(100 * ((level - 1) ** 1.6))


def get_level_title(level: int) -> str:
    if level >= 100:
        return "Legend"
    if level >= 30:
        return "Expert"
    if level >= 15:
        return "Builder"
    if level >= 6:
        return "Apprentice"
    if level >= 2:
        return "Rookie"
    return "Beginner"


def calculate_level(total_xp: int) -> dict:
    safe_xp = max(0, int(total_xp))
    level = 1

    while level < MAX_LEVEL and safe_xp >= xp_required_for_level(level + 1):
        level += 1

    current_level_xp = xp_required_for_level(level)
    next_level_xp = xp_required_for_level(level + 1)
    span = max(1, next_level_xp - current_level_xp)
    progress = ((safe_xp - current_level_xp) / span) * 100
    title = get_level_title(level)

    return {
        "level": level,
        "title": title,
        "label": f"{level:02d} · {title}",
        "total_xp": safe_xp,
        "current_level_xp": current_level_xp,
        "next_level_xp": next_level_xp,
        "xp_into_level": max(0, safe_xp - current_level_xp),
        "xp_to_next_level": max(0, next_level_xp - safe_xp),
        "progress": min(100, max(0, progress)),
    }
