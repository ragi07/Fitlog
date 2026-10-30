"""US7: Historie, Übungsfilter und Menüanschluss."""

from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import unittest
from unittest.mock import patch

from analytics import get_history, select_exercise, show_history
from main import main
from tests.sample_data import create_test_data


def capture(function, inputs, *args):
    output = StringIO()
    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(output):
            function(*args)
    return output.getvalue()


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.data = create_test_data()

    def test_history_is_chronological(self):
        entries = get_history(self.data["workouts"])
        self.assertEqual([entry["id"] for entry in entries], [3, 2, 1, 4])

    def test_filter_uses_stable_exercise_id(self):
        entries = get_history(self.data["workouts"], 10)
        self.assertEqual([entry["id"] for entry in entries], [3, 1, 4])

    def test_same_day_entries_remain_separate_and_stable(self):
        entries = get_history(self.data["workouts"], 10)
        same_day = []
        for entry in entries:
            if entry["date"] == "2026-10-20":
                same_day.append(entry["id"])
        self.assertEqual(same_day, [1, 4])

    def test_history_does_not_change_source_data(self):
        before = deepcopy(self.data)
        get_history(self.data["workouts"])
        self.assertEqual(self.data, before)

    def test_empty_and_unmatched_history(self):
        self.assertEqual(get_history([]), [])
        self.assertEqual(get_history(self.data["workouts"], 99), [])

    def test_all_filter_shows_all_rows_and_fields(self):
        output = capture(show_history, ["0"], self.data)
        self.assertIn("2026-10-10 | Bench Press | 3 | 10 | 40 kg", output)
        self.assertIn("2026-10-15 | Row | 2 | 12 | 30 kg", output)
        self.assertEqual(output.count("2026-10-20 | Bench Press"), 2)

    def test_numbered_filter_maps_to_id_not_list_position(self):
        # Back ist Auswahl 1, Chest Auswahl 2; die IDs sind 20 und 10.
        output = capture(show_history, ["2"], self.data)
        rows = [line for line in output.splitlines() if " | " in line]
        self.assertFalse(any(" | Row | " in line for line in rows))
        self.assertEqual(sum(" | Bench Press | " in row for row in rows), 3)

    def test_empty_history_prints_message_without_prompt(self):
        self.data["workouts"] = []
        output = capture(show_history, [], self.data)
        self.assertIn("No workouts available.", output)

    def test_filter_without_matches_prints_message(self):
        self.data["workouts"] = [self.data["workouts"][0]]
        output = capture(show_history, ["1"], self.data)
        self.assertIn("No workouts for this exercise.", output)

    def test_invalid_selection_retries_without_changing_data(self):
        before = deepcopy(self.data)
        output = capture(show_history, ["abc", "", "3", "2"], self.data)
        self.assertEqual(output.count("Please enter a whole number."), 2)
        self.assertIn("Please choose a number from 0 to 2.", output)
        self.assertEqual(self.data, before)

    def test_empty_exercise_selection(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertIsNone(select_exercise([]))
        self.assertIn("No exercises available.", output.getvalue())

    def test_menu_option_six_uses_supplied_data(self):
        before = deepcopy(self.data)
        output = capture(main, ["6", "0", "0"], self.data)
        self.assertIn("2026-10-10 | Bench Press", output)
        self.assertIn("Goodbye!", output)
        self.assertEqual(self.data, before)

    def test_default_menu_and_loaded_catalogue(self):
        self.assertIn("No workouts available.", capture(main, ["6", "0"]))
        self.data["exercises"][0]["name"] = "Loaded exercise"
        output = capture(main, ["1", "0"], self.data)
        self.assertIn("Loaded exercise", output)



if __name__ == "__main__":
    unittest.main()
