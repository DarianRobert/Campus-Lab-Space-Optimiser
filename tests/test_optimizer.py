import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("optimizer", ROOT / "main.py")
optimizer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(optimizer)


class OptimizerTests(unittest.TestCase):
    def setUp(self):
        self.labs = optimizer.load_labs(ROOT / "Labs.txt")
        self.modules = optimizer.load_modules(ROOT / "Modules.txt")

    def test_supplied_data_remains_feasible_with_140_unused_seats(self):
        assignment = optimizer.greedy_assignment(self.modules, self.labs)
        self.assertEqual(set(assignment), set(self.modules))
        self.assertTrue(
            all(
                optimizer.is_feasible(module, lab, self.modules, self.labs)
                for module, lab in assignment.items()
            )
        )
        self.assertEqual(
            optimizer.total_unused_seats(assignment, self.modules, self.labs), 140
        )
        self.assertEqual(
            optimizer.local_search(assignment, self.modules, self.labs), assignment
        )

    def test_local_search_improves_a_poor_assignment_without_mutating_it(self):
        modules = {"M": {"students": 20, "software": "Python"}}
        initial = {"M": "L1"}
        improved = optimizer.local_search(initial, modules, self.labs)
        self.assertEqual(initial, {"M": "L1"})
        self.assertEqual(improved, {"M": "L3"})

    def test_infeasible_module_has_a_clear_error(self):
        self.modules["M1"]["students"] = 1000
        with self.assertRaisesRegex(ValueError, "No feasible lab found for M1"):
            optimizer.greedy_assignment(self.modules, self.labs)

    def test_csv_supports_blank_lines_bom_and_quoted_names(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "labs.txt"
            path.write_text(
                '\ufeff\nL1,"Lab, West",40,Python Java\n\n', encoding="utf-8"
            )
            self.assertEqual(optimizer.load_labs(path)["L1"]["name"], "Lab, West")

    def test_invalid_records_report_the_file_and_line(self):
        for data in (
            "L1,Lab,40\n",
            "L1,Lab,many,Python\n",
            "L1,Lab,-1,Python\n",
            "L1,,40,Python\n",
            "L1,Lab,40,Python\nL1,Other,50,Java\n",
        ):
            with self.subTest(data=data), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "labs.txt"
                path.write_text(data, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, r"labs.txt:\d+:"):
                    optimizer.load_labs(path)

    def test_empty_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty.txt"
            path.write_text("\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no records found"):
                optimizer.load_labs(path)

    def test_cli_finds_default_data_from_another_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                [sys.executable, str(ROOT / "main.py")],
                cwd=temp,
                capture_output=True,
                text=True,
                check=True,
            )
        self.assertEqual(result.stdout.count("TOTAL UNUSED SEATS: 140"), 2)

    def test_cli_reports_missing_input_without_a_traceback(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "main.py"),
                "--labs",
                str(ROOT / "missing.txt"),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
