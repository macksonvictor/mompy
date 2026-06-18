import unittest
from unittest.mock import patch

from backend.missions import MISSIONS
from backend.validator import validate_mission


class ValidatorTests(unittest.TestCase):
    VALID_SOLUTIONS = {
        "mission_001": 'print("Hello, Mompy!")',
        "mission_002": 'print("Python")',
        "mission_003": 'print("Boot ready")',
        "mission_004": 'print("Mompy")',
        "mission_005": 'print("First")\nprint("Second")',
        "mission_006": 'name = "Mompy"\nprint(name)',
        "mission_007": "level = 1\nprint(level)",
        "mission_008": 'mode = "off"\nmode = "on"\nprint(mode)',
        "mission_009": "a = 2\nb = 3\nprint(a + b)",
        "mission_010": 'message = "Ready"\nprint(message)',
        "mission_011": 'power = True\nif power:\n    print("Ready")',
        "mission_012": 'temperature = 10\nif temperature > 5:\n    print("Warm")',
        "mission_013": 'code = "py"\nif code == "py":\n    print("Python")',
        "mission_014": 'score = 1\nif score >= 2:\n    print("Pass")\nelse:\n    print("Try again")',
        "mission_015": 'count = 3\nif count <= 3:\n    print("Inside")',
        "mission_016": "for i in range(3):\n    print(i)",
        "mission_017": 'for i in range(2):\n    print("Mompy")',
        "mission_018": "for number in range(1, 4):\n    print(number)",
        "mission_019": 'for letter in "py":\n    print(letter)',
        "mission_020": "total = 0\nfor number in range(3):\n    total = total + number\nprint(total)",
        "mission_021": 'items = ["onion", "terminal", "python"]\nprint(items)',
        "mission_022": 'items = ["onion", "terminal", "python"]\nprint(items[1])',
        "mission_023": "numbers = [1, 2, 3]\nnumbers.append(4)\nprint(numbers)",
        "mission_024": 'items = ["onion", "python"]\nfor item in items:\n    print(item)',
        "mission_025": "numbers = [1, 2, 3]\nprint(len(numbers))",
        "mission_026": 'def say_hello():\n    print("Hello")\nsay_hello()',
        "mission_027": 'def greet(user):\n    print("Hello, " + user)\ngreet("Mompy")',
        "mission_028": "def add(a, b):\n    return a + b\nprint(add(2, 3))",
        "mission_029": 'def make_message(user):\n    return "Hello, " + user\nprint(make_message("Mackson"))',
        "mission_030": "def double(n):\n    return n * 2\nprint(double(4))",
    }

    def test_first_mission_accepts_exact_print(self):
        result = validate_mission("mission_001", 'print("Hello, Mompy!")')
        self.assertTrue(result["correct"])
        self.assertEqual(result["expected_output"], "Hello, Mompy!")
        self.assertEqual(result["actual_output"], "Hello, Mompy!")

    def test_first_mission_does_not_block_on_empty_child_process_response(self):
        with patch(
            "backend.validator.run_user_code_safely",
            return_value={
                "ok": False,
                "output": "",
                "error": "Execucao finalizada sem resposta.",
                "timeout": False,
                "implemented": True,
            },
        ):
            result = validate_mission("mission_001", 'print("Hello, Mompy!")')

        self.assertTrue(result["correct"])
        self.assertEqual(result["expected_output"], "Hello, Mompy!")
        self.assertEqual(result["actual_output"], "Hello, Mompy!")

    def test_all_current_missions_accept_reference_solution(self):
        self.assertEqual(len(MISSIONS), 30)
        for mission_id, code in self.VALID_SOLUTIONS.items():
            with self.subTest(mission_id=mission_id):
                result = validate_mission(mission_id, code)
                self.assertTrue(result["correct"], result)

    def test_first_mission_rejects_wrong_message(self):
        result = validate_mission("mission_001", 'print("Hello")')
        self.assertFalse(result["correct"])
        self.assertTrue(result["hints"])

    def test_rejects_correct_shape_with_wrong_runtime_output(self):
        result = validate_mission(
            "mission_027",
            'def greet(user):\n    print("Hello, " + user)\ngreet("Python")',
        )
        self.assertFalse(result["correct"])
        self.assertNotEqual(result["actual_output"], result["expected_output"])

    def test_variable_block_starts_at_mission_six(self):
        result = validate_mission("mission_006", 'name = "Mompy"\nprint(name)')
        self.assertTrue(result["correct"])

    def test_syntax_error_returns_hint(self):
        result = validate_mission("mission_001", 'print("Hello, Mompy!"')
        self.assertFalse(result["correct"])
        self.assertIn("sintaxe", result["hints"][0])

    def test_concepts_are_ordered_for_beginners(self):
        block_concepts = {
            1: {"print", "string", "quotes", "parentheses", "multiple commands", "output"},
            2: {"variable", "assignment", "reassignment", "number", "addition", "print", "string"},
            3: {"if", "else", "boolean", "comparison", "greater than", "equality", "==", "<=", "colon", "indentation", "print", "string"},
            4: {"for", "range", "loop variable", "indentation", "print", "string sequence", "variable update", "addition"},
            5: {"list", "brackets", "items", "commas", "index", "zero based index", "append", "number", "for", "item", "indentation", "len", "print"},
            6: {"def", "function", "call", "indentation", "print", "parameter", "parameters", "string concatenation", "return", "addition", "multiplication"},
        }

        for mission in MISSIONS:
            allowed = block_concepts[mission.block]
            with self.subTest(mission=mission.id):
                self.assertTrue(set(mission.expected_concepts).issubset(allowed))


if __name__ == "__main__":
    unittest.main()
