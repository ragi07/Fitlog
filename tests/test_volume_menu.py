"""Ausgabe und Menüanschluss für das Gruppenvolumen."""

from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import unittest
from unittest.mock import patch

from analytics import show_volume
from main import main
from tests.sample_data import create_test_data


class VolumeMenuTests(unittest.TestCase):
    def test_sorted_totals_and_unchanged_data(self):
        data = create_test_data()
        before = deepcopy(data)
        output = StringIO()
        with redirect_stdout(output):
            show_volume(data)
        text = output.getvalue()
        self.assertIn("Chest: 3310", text)
        self.assertIn("Back: 720", text)
        self.assertLess(text.index("Chest:"), text.index("Back:"))
        self.assertEqual(data, before)

    def test_empty_data(self):
        output = StringIO()
        with redirect_stdout(output):
            show_volume({"exercises": [], "workouts": []})
        self.assertIn("No workouts available.", output.getvalue())

    def test_bodyweight_is_shown_with_zero(self):
        data = create_test_data()
        for workout in data["workouts"]:
            workout["weight"] = 0
        output = StringIO()
        with redirect_stdout(output):
            show_volume(data)
        self.assertIn("Chest: 0", output.getvalue())
        self.assertIn("Back: 0", output.getvalue())

    def test_menu_option_eight(self):
        output = StringIO()
        with patch("builtins.input", side_effect=["8", "0"]):
            with redirect_stdout(output):
                main(create_test_data())
        self.assertIn("Chest: 3310", output.getvalue())
        self.assertIn("Goodbye!", output.getvalue())


if __name__ == "__main__":
    unittest.main()
