import unittest

from algorithm import generate_sequence


class GenerateSequenceTests(unittest.TestCase):
    def setUp(self):
        self.mandatory = ["StandInit", "Sit", "Stand", "Crouch"]
        self.movements = [
            {"name": "right_arm", "start": "StandInit", "end": "PoseA",
             "duration": 8},
            {"name": "arms_opening", "start": "PoseA", "end": "Sit",
             "duration": 8},
            {"name": "move_forward", "start": "Sit", "end": "PoseB",
             "duration": 8},
            {"name": "diagonal_left", "start": "PoseB", "end": "Stand",
             "duration": 8},
            {"name": "union_arms", "start": "Stand", "end": "PoseC",
             "duration": 8},
            {"name": "move_backward", "start": "PoseC", "end": "Crouch",
             "duration": 8},
        ]

    def test_plans_across_mandatory_poses_with_global_move_minimum(self):
        plan = generate_sequence(self.mandatory, self.movements)

        self.assertEqual(
            plan["positions"],
            ["StandInit", "PoseA", "Sit", "PoseB", "Stand", "PoseC", "Crouch"])
        self.assertEqual(plan["intermediate_count"], 6)
        self.assertEqual(plan["duration_seconds"], 48)

    def test_rejects_missing_compatible_transition(self):
        with self.assertRaises(ValueError):
            generate_sequence(self.mandatory, self.movements[:2])

    def test_rejects_plan_over_time_limit(self):
        with self.assertRaises(ValueError):
            generate_sequence(self.mandatory, self.movements, time_limit=47)

    def test_cannot_relax_assignment_constraints(self):
        with self.assertRaises(ValueError):
            generate_sequence(
                self.mandatory, self.movements, min_intermediate=4)
        with self.assertRaises(ValueError):
            generate_sequence(
                self.mandatory, self.movements, time_limit=121)


if __name__ == "__main__":
    unittest.main()
