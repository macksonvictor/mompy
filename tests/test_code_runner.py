import unittest

from backend.code_runner import run_user_code_safely


class CodeRunnerTests(unittest.TestCase):
    def test_captures_print_output(self):
        result = run_user_code_safely('name = "Mompy"\nprint(name)')
        self.assertTrue(result["ok"])
        self.assertEqual(result["output"], "Mompy")
        self.assertTrue(result["implemented"])

    def test_blocks_file_access(self):
        result = run_user_code_safely('open("x.txt", "w")')
        self.assertFalse(result["ok"])
        self.assertIn("open", result["error"])

    def test_blocks_imports(self):
        result = run_user_code_safely("import os\nprint(os.getcwd())")
        self.assertFalse(result["ok"])
        self.assertIn("nao e permitido", result["error"])

    def test_times_out_slow_code(self):
        result = run_user_code_safely("while True:\n    pass", timeout=0.2)
        self.assertFalse(result["ok"])
        self.assertTrue(result["timeout"])


if __name__ == "__main__":
    unittest.main()
