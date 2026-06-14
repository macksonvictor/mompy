import unittest

from backend.validator import validate_mission


class ValidatorTests(unittest.TestCase):
    def test_first_mission_accepts_exact_print(self):
        result = validate_mission("mission_001", 'print("Hello, Mompy!")')
        self.assertTrue(result["correct"])
        self.assertEqual(result["expected_output"], "Hello, Mompy!")

    def test_first_mission_rejects_wrong_message(self):
        result = validate_mission("mission_001", 'print("Hello")')
        self.assertFalse(result["correct"])
        self.assertTrue(result["hints"])

    def test_variable_mission_accepts_variable_print(self):
        result = validate_mission("mission_002", 'name = "Mompy"\nprint(name)')
        self.assertTrue(result["correct"])

    def test_syntax_error_returns_hint(self):
        result = validate_mission("mission_001", 'print("Hello, Mompy!"')
        self.assertFalse(result["correct"])
        self.assertIn("sintaxe", result["hints"][0])


if __name__ == "__main__":
    unittest.main()
