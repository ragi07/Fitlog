"""US9: Erste Tests für die Volumenberechnung."""

from copy import deepcopy
import unittest

from analytics import get_volume_by_muscle_group
from tests.sample_data import create_test_data


class VolumeTests(unittest.TestCase):
    def setUp(self):
        self.data = create_test_data()

    def test_empty_data(self):
        self.assertEqual(get_volume_by_muscle_group([], []), [])

    def test_no_workouts(self):
        result = get_volume_by_muscle_group(self.data["exercises"], [])
        self.assertEqual(result, [])

    def test_sets_times_repetitions_times_weight(self):
        workouts = [self.data["workouts"][0]]
        result = get_volume_by_muscle_group(self.data["exercises"], workouts)
        self.assertEqual(result, [{"muscle_group": "Chest", "volume": 1350}])

    def test_group_totals_match_hand_calculation(self):
        result = get_volume_by_muscle_group(
            self.data["exercises"], self.data["workouts"]
        )
        self.assertEqual(result, [
            {"muscle_group": "Chest", "volume": 3310},
            {"muscle_group": "Back", "volume": 720},
        ])

    def test_multiple_exercises_in_the_same_group(self):
        self.data["exercises"][1]["muscle_group"] = "Chest"
        result = get_volume_by_muscle_group(
            self.data["exercises"], self.data["workouts"]
        )
        self.assertEqual(result, [{"muscle_group": "Chest", "volume": 4030}])

    def test_largest_volume_is_first(self):
        self.data["workouts"][1]["weight"] = 200
        result = get_volume_by_muscle_group(
            self.data["exercises"], self.data["workouts"]
        )
        self.assertEqual(result[0], {"muscle_group": "Back", "volume": 4800})

    def test_bodyweight_counts_as_zero_volume(self):
        self.data["workouts"][1]["weight"] = 0
        result = get_volume_by_muscle_group(
            self.data["exercises"], self.data["workouts"]
        )
        self.assertEqual(result[1], {"muscle_group": "Back", "volume": 0})

    def test_decimal_weight(self):
        workouts = [{"exercise_id": 10, "sets": 2,
                     "reps": 3, "weight": 0.5}]
        result = get_volume_by_muscle_group(self.data["exercises"], workouts)
        self.assertEqual(result[0]["volume"], 3.0)

    def test_same_day_workouts_are_both_counted(self):
        workouts = [self.data["workouts"][0], self.data["workouts"][3]]
        result = get_volume_by_muscle_group(self.data["exercises"], workouts)
        self.assertEqual(result[0]["volume"], 2110)

    def test_source_data_is_not_changed(self):
        before = deepcopy(self.data)
        get_volume_by_muscle_group(
            self.data["exercises"], self.data["workouts"]
        )
        self.assertEqual(self.data, before)


if __name__ == "__main__":
    unittest.main()
