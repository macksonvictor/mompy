"""Guided lesson metadata for Mompy blocks."""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Lesson:
    id: str
    title: str
    block: int
    missions_range: str
    intro_title: str
    goals: tuple[str, ...]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["goals"] = list(self.goals)
        return data


LESSONS: tuple[Lesson, ...] = (
    Lesson(
        id="lesson_001",
        title="First Python Commands",
        block=1,
        missions_range="1-5",
        intro_title="First Python Commands",
        goals=(
            "Understand Python as a language of instructions",
            "Display text with print()",
            "Use quotes and parentheses without errors",
        ),
    ),
    Lesson(
        id="lesson_002",
        title="Variables and Values",
        block=2,
        missions_range="6-10",
        intro_title="Variables and Values",
        goals=(
            "Store values in names using =",
            "Tell apart a variable from a quoted string",
            "Use variables, numbers, and simple addition in print()",
        ),
    ),
    Lesson(
        id="lesson_003",
        title="Decisions",
        block=3,
        missions_range="11-15",
        intro_title="Decisions",
        goals=(
            "Understand true or false conditions",
            "Use if, else, colons, and indentation",
            "Compare values with ==, >, >= and <=",
        ),
    ),
    Lesson(
        id="lesson_004",
        title="Loops",
        block=4,
        missions_range="16-20",
        intro_title="Loops",
        goals=(
            "Repeat tasks with for",
            "Use range and a loop variable",
            "Update a variable inside a loop",
        ),
    ),
    Lesson(
        id="lesson_005",
        title="Lists",
        block=5,
        missions_range="21-25",
        intro_title="Lists",
        goals=(
            "Create lists with brackets, items, and commas",
            "Read items by index",
            "Add, count, and iterate over items",
        ),
    ),
    Lesson(
        id="lesson_006",
        title="Functions",
        block=6,
        missions_range="26-30",
        intro_title="Functions",
        goals=(
            "Create functions with def",
            "Call functions and receive parameters",
            "Return values with return",
        ),
    ),
)


def get_lessons() -> list[dict]:
    return [lesson.to_dict() for lesson in LESSONS]


def lesson_for_mission_number(mission_number: int) -> Lesson | None:
    for lesson in LESSONS:
        start, end = [int(part) for part in lesson.missions_range.split("-")]
        if start <= mission_number <= end:
            return lesson
    return None
