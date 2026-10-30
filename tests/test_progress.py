"""US8: Gewichtsvergleich und Menüanschluss."""

from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import unittest
from unittest.mock import patch

from analytics import get_progress, show_progress
from main import main
from tests.sample_data import create_test_data


def capture(function, inputs, *args):
    output = StringIO()
    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(output):
            function(*args)
    return output.getvalue()


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.data = create_test_data()

    def test_first_last_best_and_difference(self):
        progress = get_progress(self.data["workouts"], 10)
        self.assertEqual(progress["first_weight"], 40.0)
        self.assertEqual(progress["last_weight"], 47.5)
        self.assertEqual(progress["best_weight"], 47.5)
        self.assertEqual(progress["progress"], 7.5)

    def test_best_weight_can_be_between_first_and_last(self):
        self.data["workouts"][0]["weight"] = 60.0
        progress = get_progress(self.data["workouts"], 10)
        self.assertEqual(progress["best_weight"], 60.0)
        self.assertEqual(progress["progress"], 7.5)

    def test_other_exercise_is_not_counted(self):
        self.data["workouts"][1]["weight"] = 999.0
        progress = get_progress(self.data["workouts"], 10)
        self.assertEqual(progress["best_weight"], 47.5)

    def test_zero_one_and_missing_entries(self):
        self.assertIsNone(get_progress([], 10))
        self.assertIsNone(get_progress(self.data["workouts"], 20))
        self.assertIsNone(get_progress(self.data["workouts"], 99))

    def test_same_day_entries_count_separately(self):
        workouts = [self.data["workouts"][0], self.data["workouts"][3]]
        progress = get_progress(workouts, 10)
        self.assertEqual(progress["first_weight"], 45.0)
        self.assertEqual(progress["last_weight"], 47.5)
        self.assertEqual(progress["progress"], 2.5)

    def test_zero_start_weight_is_allowed(self):
        self.data["workouts"][2]["weight"] = 0
        progress = get_progress(self.data["workouts"], 10)
        self.assertEqual(progress["progress"], 47.5)

    def test_progress_does_not_modify_data(self):
        before = deepcopy(self.data)
        get_progress(self.data["workouts"], 10)
        self.assertEqual(self.data, before)

    def test_positive_progress_has_plus_sign(self):
        output = capture(show_progress, ["2"], self.data)
        self.assertIn("First weight: 40 kg", output)
        self.assertIn("Last weight: 47.5 kg", output)
        self.assertIn("Best weight: 47.5 kg", output)
        self.assertIn("Progress: +7.5 kg", output)

    def test_negative_progress_has_minus_sign(self):
        self.data["workouts"][3]["weight"] = 35.0
        output = capture(show_progress, ["2"], self.data)
        self.assertIn("Progress: -5 kg", output)

    def test_unchanged_weight_has_zero_progress(self):
        for workout in self.data["workouts"]:
            workout["weight"] = 40.0
        output = capture(show_progress, ["2"], self.data)
        self.assertIn("Progress: +0 kg", output)

    def test_insufficient_entries_message(self):
        output = capture(show_progress, ["1"], self.data)
        self.assertIn("Not enough entries (at least 2 needed).", output)

    def test_cancel_does_not_show_a_result(self):
        output = capture(show_progress, ["0"], self.data)
        self.assertNotIn("First weight:", output)
        self.assertNotIn("Not enough entries", output)

    def test_no_exercises(self):
        self.data["exercises"] = []
        self.data["workouts"] = []
        output = capture(show_progress, [], self.data)
        self.assertIn("No exercises available.", output)

    def test_invalid_selection_retries(self):
        output = capture(show_progress, ["abc", "3", "2"], self.data)
        self.assertIn("Please enter a whole number.", output)
        self.assertIn("Please choose a number from 0 to 2.", output)
        self.assertIn("Progress: +7.5 kg", output)

    def test_menu_option_seven(self):
        before = deepcopy(self.data)
        output = capture(main, ["7", "2", "0"], self.data)
        self.assertIn("Progress: +7.5 kg", output)
        self.assertIn("Goodbye!", output)
        self.assertEqual(self.data, before)


if __name__ == "__main__":
    unittest.main()
