"""Guided briefings shown before mission blocks."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BriefingStep:
    type: str
    title: str | None = None
    text: str | None = None
    retry_text: str | None = None
    question: str | None = None
    options: tuple[dict, ...] = ()
    success_text: str | None = None
    fail_text: str | None = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["options"] = [dict(option) for option in self.options]
        return {key: value for key, value in data.items() if value not in (None, (), [])}


@dataclass(frozen=True)
class Briefing:
    id: str
    title: str
    subtitle: str
    before_mission_index: int
    missions_range: str
    steps: tuple[BriefingStep, ...]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "before_mission_index": self.before_mission_index,
            "missions_range": self.missions_range,
            "steps": [step.to_dict() for step in self.steps],
        }


def check(question: str, correct: str, wrong_a: str, wrong_b: str, success: str, fail: str) -> BriefingStep:
    return BriefingStep(
        type="check",
        question=question,
        options=(
            {"label": "A", "text": wrong_a, "correct": False},
            {"label": "B", "text": correct, "correct": True},
            {"label": "C", "text": wrong_b, "correct": False},
        ),
        success_text=success,
        fail_text=fail,
    )


BRIEFINGS: tuple[Briefing, ...] = (
    Briefing(
        id="briefing_001",
        title="Mompy",
        subtitle="First Python Commands",
        before_mission_index=0,
        missions_range="1-5",
        steps=(
            BriefingStep(
                type="lesson",
                title="Python",
                text="Python is a language created by Guido van Rossum. It became known for being readable: the code tries to look clear to people.",
                retry_text="Think of Python as a clear way to write instructions for a computer. The idea is to read the code without struggling.",
            ),
            BriefingStep(
                type="lesson",
                title="Commands",
                text="A program is made of commands. Running code means asking Python to follow those commands in order.",
                retry_text="Each important line is an instruction. Python reads and tries to execute exactly what is written.",
            ),
            BriefingStep(
                type="lesson",
                title="Text",
                text="When we want to write a message, we use text. In Python, text normally goes inside quotes.",
                retry_text='Without quotes, Python thinks the word is a code name. With quotes, it understands it as a message, like "Hello".',
            ),
            BriefingStep(
                type="lesson",
                title="print",
                text="print is the basic command to show something in the console output. It uses parentheses to receive what will be shown.",
                retry_text='The form is print("message"). The command is print; the text goes in quotes; everything goes inside the parentheses.',
            ),
            check(
                "To show text on screen, we use:",
                "print with text in quotes",
                "if with comparison",
                "for with range",
                "Correct. print shows messages and results in the console.",
                "Not yet. In this block, the main tool is print with text in quotes.",
            ),
            check(
                "If you forget the quotes around text, Python may:",
                "try to read the word as a code name",
                "turn it into a number automatically",
                "repeat the message",
                "Correct. Quotes tell Python that it is text.",
                "Almost. Quotes are the signal that the content is a message.",
            ),
        ),
    ),
    Briefing(
        id="briefing_002",
        title="Mompy",
        subtitle="Variables and Values",
        before_mission_index=5,
        missions_range="6-10",
        steps=(
            BriefingStep(
                type="lesson",
                title="Variable",
                text="A variable is a name that stores a value. You use the name later to retrieve that value.",
                retry_text="Imagine a label on a box. The label is the variable name; what is inside is the value.",
            ),
            BriefingStep(
                type="lesson",
                title="Assignment",
                text="In Python, = stores a value in a name. This is called assignment.",
                retry_text='When you write name = "Mompy", you are storing the text "Mompy" in the name name.',
            ),
            BriefingStep(
                type="lesson",
                title="Name or text",
                text='name without quotes is a variable. "name" with quotes is literal text. That difference changes everything.',
                retry_text='print(name) shows the stored value. print("name") shows the word name.',
            ),
            BriefingStep(
                type="lesson",
                title="Numbers and addition",
                text="Variables can also store numbers. You can add values and show the result with print.",
                retry_text="If a = 2 and b = 3, print(a + b) shows 5.",
            ),
            check(
                "The = sign in a variable means:",
                "store a value in a name",
                "compare two values",
                "show a message",
                "Correct. = assigns a value.",
                "Not yet. Comparison comes later; here = stores a value.",
            ),
            check(
                "Which difference matters?",
                'name is a variable; "name" is text',
                "name is always text",
                "quotes erase variables",
                "Correct. Without quotes, Python looks for the variable.",
                "Almost. Quotes turn content into literal text.",
            ),
        ),
    ),
    Briefing(
        id="briefing_003",
        title="Mompy",
        subtitle="Decisions",
        before_mission_index=10,
        missions_range="11-15",
        steps=(
            BriefingStep(
                type="lesson",
                title="Condition",
                text="A condition is a question that results in true or false. Programs use this to choose paths.",
                retry_text='Questions like 10 > 3 or code == "py" become True or False.',
            ),
            BriefingStep(
                type="lesson",
                title="if",
                text="An if runs a block only if the condition is true. In Python, the if line ends with a colon.",
                retry_text="if means if. If the question is true, the indented block runs.",
            ),
            BriefingStep(
                type="lesson",
                title="Indentation",
                text="Indented means shifted to the right. The indented lines belong to the if or the else.",
                retry_text="Without indentation, Python does not know which lines are part of the decision.",
            ),
            BriefingStep(
                type="lesson",
                title="Comparison",
                text="Use == to compare equality. Use >, <, >= and <= to compare size or order.",
                retry_text="= stores a value. == asks if two values are equal.",
            ),
            BriefingStep(
                type="lesson",
                title="else",
                text="else is the other path. It runs when the if condition is not true.",
                retry_text="If the if does not run, the else can handle the opposite case.",
            ),
            check(
                "What does if do?",
                "runs a block if a condition is true",
                "repeats an action forever",
                "stores text in a variable",
                "Correct. if is a choice based on a condition.",
                "Not yet. if decides; repetition comes in the next block.",
            ),
            check(
                "In Python, the block that belongs to if must be:",
                "indented",
                "without quotes",
                "outside the file",
                "Correct. Indentation shows belonging.",
                "Almost. The if block is shifted to the right.",
            ),
            check(
                "Which operator compares equality?",
                "==",
                "=",
                ">=",
                "Correct. == compares; = assigns.",
                "Not yet. = stores a value. To ask if equal, use ==.",
            ),
        ),
    ),
    Briefing(
        id="briefing_004",
        title="Mompy",
        subtitle="Loops",
        before_mission_index=15,
        missions_range="16-20",
        steps=(
            BriefingStep(
                type="lesson",
                title="Repeat",
                text="Loops exist to avoid copying and pasting identical commands. The program runs the same block multiple times.",
                retry_text="If something needs to happen many times, a loop organizes that.",
            ),
            BriefingStep(
                type="lesson",
                title="for",
                text="for goes through a sequence. On each iteration, a variable receives the current value.",
                retry_text="In for i in range(3), i is 0, then 1, then 2.",
            ),
            BriefingStep(
                type="lesson",
                title="range",
                text="range creates a sequence of numbers. range(3) generates 0, 1 and 2. range(1, 4) generates 1, 2 and 3.",
                retry_text="The end of range is not included. range(1, 4) stops before 4.",
            ),
            BriefingStep(
                type="lesson",
                title="Loop block",
                text="What is indented inside the for runs on each iteration.",
                retry_text="If print is inside the for, it can show something multiple times.",
            ),
            BriefingStep(
                type="lesson",
                title="Update value",
                text="A loop can update a variable. total = total + number adds a new value to the old total.",
                retry_text="This is common when we collect results across multiple iterations.",
            ),
            check(
                "A loop mainly helps to:",
                "repeat actions without copying code",
                "compare equality",
                "create a function",
                "Correct. A loop is organized repetition.",
                "Not yet. In this block, the focus is repeating actions.",
            ),
            check(
                "In for i in range(3), the values of i are:",
                "0, 1 and 2",
                "1, 2 and 3",
                "3, 2 and 1",
                "Correct. range(3) starts at 0 and stops before 3.",
                "Almost. range(3) generates 0, 1 and 2.",
            ),
        ),
    ),
    Briefing(
        id="briefing_005",
        title="Mompy",
        subtitle="Lists",
        before_mission_index=20,
        missions_range="21-25",
        steps=(
            BriefingStep(
                type="lesson",
                title="List",
                text="A list stores multiple values in a single variable. It uses brackets.",
                retry_text='Example: items = ["onion", "python"]. Strings go in quotes and are separated by commas.',
            ),
            BriefingStep(
                type="lesson",
                title="Items",
                text="Each value inside the list is an item. Commas separate the items.",
                retry_text="If you forget a comma, Python may not understand where one item ends and the next begins.",
            ),
            BriefingStep(
                type="lesson",
                title="Index",
                text="Lists have positions. In Python, the first position is 0, so the second item is at index 1.",
                retry_text="items[0] gets the first item. items[1] gets the second.",
            ),
            BriefingStep(
                type="lesson",
                title="append and len",
                text="append adds an item to the end. len counts how many items exist.",
                retry_text="numbers.append(4) adds 4. len(numbers) counts the items.",
            ),
            BriefingStep(
                type="lesson",
                title="Iterating a list",
                text="You can also use for to go through each item in a list.",
                retry_text="for item in items: makes item receive one list value at a time.",
            ),
            check(
                "In Python, the first index of a list is:",
                "0",
                "1",
                "-1 always",
                "Correct. Lists start at index 0.",
                "Not yet. The first item is at index 0.",
            ),
            check(
                "To add an item to the end of a list, we use:",
                "append",
                "if",
                "def",
                "Correct. append adds to the end.",
                "Almost. if decides and def creates a function; append works on lists.",
            ),
        ),
    ),
    Briefing(
        id="briefing_006",
        title="Mompy",
        subtitle="Functions",
        before_mission_index=25,
        missions_range="26-30",
        steps=(
            BriefingStep(
                type="lesson",
                title="Function",
                text="A function is a block of code with a name. It helps organize a task.",
                retry_text="Think of a function as a small machine: you call it by name and it does the job.",
            ),
            BriefingStep(
                type="lesson",
                title="def",
                text="In Python, we create a function with def, a name, parentheses, and a colon. The function block is indented.",
                retry_text="def say_hello(): creates the function. The line inside must be shifted to the right.",
            ),
            BriefingStep(
                type="lesson",
                title="Calling",
                text="Creating a function does not run it automatically. You need to call the function by name with parentheses.",
                retry_text="After def say_hello():, write say_hello() to run it.",
            ),
            BriefingStep(
                type="lesson",
                title="Parameters",
                text="Parameters are information that enters the function. In greet(user), user receives the value passed in the call.",
                retry_text='greet("Mompy") makes user equal "Mompy" inside the function.',
            ),
            BriefingStep(
                type="lesson",
                title="return",
                text="return sends a value back. You can then show that value with print.",
                retry_text="return a + b sends the sum back to whoever called add(a, b).",
            ),
            check(
                "Creating a function with def:",
                "does not run the function by itself",
                "always runs it twice",
                "deletes the parameters",
                "Correct. After creating, you still need to call it.",
                "Not yet. def creates the function; the call runs it.",
            ),
            check(
                "return is used to:",
                "send a value back from the function",
                "always show text directly on screen",
                "create a list",
                "Correct. return delivers a result.",
                "Almost. print shows; return sends back.",
            ),
        ),
    ),
)


BRIEFINGS_BY_ID: dict[str, Briefing] = {briefing.id: briefing for briefing in BRIEFINGS}


def get_briefings() -> list[dict]:
    return [briefing.to_dict() for briefing in BRIEFINGS]


def get_briefing(briefing_id: str) -> dict | None:
    briefing = BRIEFINGS_BY_ID.get(briefing_id)
    return briefing.to_dict() if briefing else None


def briefing_for_mission_index(mission_index: int) -> dict | None:
    for briefing in BRIEFINGS:
        if briefing.before_mission_index == mission_index:
            return briefing.to_dict()
    return None
