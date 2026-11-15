"""Gesamtablauf und Speicherfehler der schreibenden Menüpunkte."""

from contextlib import redirect_stdout
from copy import deepcopy
import csv
import datetime
from io import StringIO
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from main import main
from storage import load_data, save_data
from tests.sample_data import create_test_data


class CompleteMenuTests(unittest.TestCase):
    def setUp(self):
        self.previous_folder = Path.cwd()
        self.temporary_folder = tempfile.TemporaryDirectory()
        os.chdir(self.temporary_folder.name)

    def tearDown(self):
        os.chdir(self.previous_folder)
        self.temporary_folder.cleanup()

    def run_menu(self, answers, data=None):
        output = StringIO()
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                main(data)
        return output.getvalue()

    def test_added_exercise_is_saved_immediately(self):
        self.run_menu(["2", "  Neue   Übung  ", "9", "3", "0"])
        data = load_data()
        self.assertEqual(data["exercises"][-1], {
            "id": 7, "name": "Neue Übung", "muscle_group": "Legs"
        })

    def test_search_uses_saved_catalogue_without_saving(self):
        data = create_test_data()
        save_data(data)
        before = Path("data/fitlog.json").read_bytes()
        with patch("main.save_data") as save:
            output = self.run_menu(["3", "PRESS", "0"])
        save.assert_not_called()
        self.assertIn("Chest: Bench Press", output)
        self.assertEqual(Path("data/fitlog.json").read_bytes(), before)

    def test_workout_is_saved_with_numeric_id(self):
        self.run_menu(["4", "", "1", "3", "10", "52,5", "0"])
        data = load_data()
        self.assertEqual(data["workouts"], [{
            "id": 1, "exercise_id": 1,
            "date": datetime.date.today().isoformat(),
            "sets": 3, "reps": 10, "weight": 52.5
        }])

    def test_invalid_field_keeps_previous_values(self):
        answers = [
            "4", "2026-11-15", "99", "abc", "1",
            "0", "3", "101", "10", "-1", "nan", "40", "0"
        ]
        output = StringIO()
        with patch("builtins.input", side_effect=answers) as question:
            with redirect_stdout(output):
                main()
        date_questions = [
            call for call in question.call_args_list
            if call.args[0].startswith("Date (")
        ]
        self.assertEqual(len(date_questions), 1)
        data = load_data()
        self.assertEqual(len(data["workouts"]), 1)
        self.assertEqual(data["workouts"][0]["date"], "2026-11-15")
        self.assertEqual(data["workouts"][0]["weight"], 40)

    def test_no_exercises_prevents_logging(self):
        data = {
            "format": "fitlog-v1", "exercises": [],
            "workouts": [], "weekly_goal": 3
        }
        with patch("main.save_data") as save:
            output = self.run_menu(["4", "0"], data)
        save.assert_not_called()
        self.assertIn("Please add an exercise first", output)
        self.assertEqual(data["workouts"], [])

    def test_confirmed_deletion_is_saved(self):
        data = create_test_data()
        before = deepcopy(data)
        save_data(data)
        self.run_menu(["5", "2", "y", "0"])
        loaded = load_data()
        self.assertEqual(
            loaded["workouts"],
            before["workouts"][:1] + before["workouts"][2:]
        )
        self.assertEqual(loaded["exercises"], before["exercises"])

    def test_cancelled_deletion_keeps_memory_and_file(self):
        for answers in [["5", "0", "0"], ["5", "2", "n", "0"]]:
            data = create_test_data()
            before = deepcopy(data)
            save_data(data)
            before_file = Path("data/fitlog.json").read_bytes()
            with patch("main.save_data") as save:
                self.run_menu(answers, data)
            save.assert_not_called()
            self.assertEqual(data, before)
            self.assertEqual(Path("data/fitlog.json").read_bytes(), before_file)

    def test_failed_addition_restores_previous_data(self):
        data = deepcopy(load_data())
        self.check_failed_change(["2", "Neue Übung", "1", "0"], data)

    def test_failed_logging_restores_previous_data(self):
        data = deepcopy(load_data())
        self.check_failed_change(["4", "", "1", "3", "10", "40", "0"], data)

    def test_failed_deletion_restores_previous_data(self):
        data = create_test_data()
        self.check_failed_change(["5", "1", "y", "0"], data)

    def test_deleting_last_workout_updates_all_views(self):
        data = create_test_data()
        data["workouts"] = [data["workouts"][0]]
        data["workouts"][0]["date"] = datetime.date.today().isoformat()
        save_data(data)
        output = self.run_menu([
            "5", "1", "y", "5", "6", "7", "2", "8",
            "9", "n", "10", "0"
        ])
        self.assertEqual(load_data()["workouts"], [])
        self.assertIn("No workouts to delete.", output)
        self.assertIn("No workouts available.", output)
        self.assertIn("Not enough entries", output)
        self.assertIn("0 of 3", output)
        report = next(Path("reports").glob("*.csv"))
        with report.open(encoding="utf-8-sig", newline="") as stream:
            self.assertEqual(len(list(csv.reader(stream, delimiter=";"))), 1)

    def check_failed_change(self, answers, data):
        before = deepcopy(data)
        save_data(data)
        before_file = Path("data/fitlog.json").read_bytes()
        with patch("main.save_data", side_effect=OSError("write error")):
            output = self.run_menu(answers, data)
        self.assertEqual(data, before)
        self.assertEqual(Path("data/fitlog.json").read_bytes(), before_file)
        self.assertIn("Previous data restored.", output)
        self.assertNotIn("Changes saved.", output)

    def test_complete_console_workflow_and_restart(self):
        script = Path(__file__).resolve().parents[1] / "main.py"
        answers = [
            "2", "New Exercise", "3",
            "3", "new",
            "4", "", "7", "3", "10", "50",
            "4", "", "7", "2", "8", "55",
            "6", "0", "7", "5", "8",
            "9", "y", "1", "y", "10",
            "5", "1", "y", "6", "0", "10", "0"
        ]
        result = subprocess.run(
            [sys.executable, "-B", str(script)],
            input="\n".join(answers) + "\n",
            text=True, capture_output=True, check=True,
        )
        self.assertNotIn("not implemented yet", result.stdout)
        self.assertIn("Progress: +5 kg", result.stdout)
        self.assertIn("Legs: 2380", result.stdout)
        self.assertIn("Workout deleted.", result.stdout)
        data = load_data()
        self.assertEqual(len(data["exercises"]), 7)
        self.assertEqual([entry["id"] for entry in data["workouts"]], [2])
        self.assertEqual(data["weekly_goal"], 1)
        report = next(Path("reports").glob("*.csv"))
        with report.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.reader(stream, delimiter=";"))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][1], "New Exercise")
        self.assertEqual(float(rows[1][-1]), 880)

        restarted = subprocess.run(
            [sys.executable, "-B", str(script)],
            input="6\n0\n7\n5\n8\n9\nn\n10\n0\n",
            text=True, capture_output=True, check=True,
        )
        self.assertIn("Legs: 880", restarted.stdout)
        self.assertIn("Not enough entries", restarted.stdout)
        self.assertIn("1 of 1", restarted.stdout)
        self.assertEqual(load_data(), data)


if __name__ == "__main__":
    unittest.main()
