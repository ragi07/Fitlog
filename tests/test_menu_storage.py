"""Prüft das Menü mit echten Dateien in einem temporären Ordner."""

from contextlib import redirect_stdout
from copy import deepcopy
import csv
import datetime
from io import StringIO
import json
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


class MenuStorageTests(unittest.TestCase):
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

    def test_first_start_creates_file(self):
        self.run_menu(["0"])
        data = load_data()
        self.assertEqual(len(data["exercises"]), 6)
        self.assertEqual(data["workouts"], [])
        self.assertEqual(data["weekly_goal"], 3)

    def test_start_uses_saved_exercises(self):
        data = create_test_data()
        data["exercises"][0]["name"] = "Geladene Übung"
        save_data(data)
        output = self.run_menu(["1", "0"])
        self.assertIn("Geladene Übung", output)

    def test_saved_statistics_and_order_survive_restart(self):
        data = create_test_data()
        save_data(data)
        before = Path("data/fitlog.json").read_bytes()
        output = self.run_menu(["6", "0", "7", "2", "8", "0"])
        self.assertIn("2026-10-10 | Bench Press", output)
        self.assertIn("Progress: +7.5 kg", output)
        self.assertIn("Chest: 3310", output)
        self.assertEqual(Path("data/fitlog.json").read_bytes(), before)
        self.assertEqual(load_data(), data)

    def test_invalid_menu_repeats_question(self):
        output = self.run_menu(["abc", "", "-1", "11", "0"])
        self.assertEqual(output.count("Invalid input!"), 4)
        self.assertIn("Goodbye!", output)

    def test_corrupt_file_stops_without_overwriting(self):
        Path("data").mkdir()
        file = Path("data/fitlog.json")
        file.write_text("{broken", encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.run_menu([])
        self.assertEqual(file.read_text(encoding="utf-8"), "{broken")

    def test_load_error_is_reported_without_menu(self):
        with patch("main.load_data", side_effect=OSError("read error")):
            output = self.run_menu([])
        self.assertIn("Could not load the training data", output)
        self.assertNotIn("Choose an option", output)

    def test_goal_change_is_saved_and_loaded_again(self):
        self.run_menu(["9", "y", "4", "y", "0"])
        self.assertEqual(load_data()["weekly_goal"], 4)
        output = self.run_menu(["9", "n", "0"])
        self.assertIn("of 4", output)

    def test_cancel_goal_change_keeps_file(self):
        save_data(create_test_data())
        before = Path("data/fitlog.json").read_bytes()
        self.run_menu(["9", "y", "4", "n", "0"])
        self.assertEqual(Path("data/fitlog.json").read_bytes(), before)

    def test_failed_goal_save_restores_memory_and_file(self):
        data = create_test_data()
        before_data = deepcopy(data)
        save_data(data)
        before_file = Path("data/fitlog.json").read_bytes()
        with patch("goals.save_data", side_effect=OSError("write error")):
            output = self.run_menu(["9", "y", "4", "y", "0"], data)
        self.assertEqual(data, before_data)
        self.assertEqual(Path("data/fitlog.json").read_bytes(), before_file)
        self.assertIn("could not be saved", output)
        self.assertNotIn("Weekly goal saved.", output)

    def test_export_menu_uses_loaded_workouts(self):
        data = create_test_data()
        for workout in data["workouts"]:
            workout["date"] = datetime.date.today().isoformat()
        save_data(data)
        output = self.run_menu(["10", "0"])
        files = list(Path("reports").glob("*.csv"))
        self.assertEqual(len(files), 1)
        with files[0].open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.reader(stream, delimiter=";"))
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0][0], "date")
        self.assertIn("Training days: 1", output)
        self.assertIn("Total volume: 4030", output)

    def test_export_empty_week(self):
        self.run_menu(["10", "0"])
        file = next(Path("reports").glob("*.csv"))
        with file.open(encoding="utf-8-sig", newline="") as stream:
            self.assertEqual(len(list(csv.reader(stream, delimiter=";"))), 1)

    def test_export_failure_does_not_change_data(self):
        data = create_test_data()
        before = deepcopy(data)
        with patch("report.os.makedirs", side_effect=OSError("write error")):
            output = self.run_menu(["10", "0"], data)
        self.assertIn("Could not write the report", output)
        self.assertEqual(data, before)

    def test_real_program_restart(self):
        script = Path(__file__).resolve().parents[1] / "main.py"
        first = subprocess.run(
            [sys.executable, "-B", str(script)],
            input="0\n", text=True, capture_output=True, check=True,
        )
        self.assertIn("Goodbye!", first.stdout)
        save_data(create_test_data())
        second = subprocess.run(
            [sys.executable, "-B", str(script)],
            input="6\n0\n7\n2\n8\n0\n",
            text=True, capture_output=True, check=True,
        )
        self.assertIn("Progress: +7.5 kg", second.stdout)
        self.assertIn("Chest: 3310", second.stdout)

    def test_real_program_rejects_invalid_file(self):
        Path("data").mkdir()
        Path("data/fitlog.json").write_text("{}", encoding="utf-8")
        script = Path(__file__).resolve().parents[1] / "main.py"
        result = subprocess.run(
            [sys.executable, "-B", str(script)],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(
            json.loads(Path("data/fitlog.json").read_text()), {}
        )


if __name__ == "__main__":
    unittest.main()
