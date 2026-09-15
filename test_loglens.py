import unittest

from loglens import analyze, health


class LogLensTests(unittest.TestCase):
    def test_counts_levels_and_errors(self):
        lines = [
            "2026-09-15 10:00:00 INFO started",
            "2026-09-15 10:01:00 WARN slow response",
            "2026-09-15 10:02:00 ERROR ConnectionTimeout upstream",
            "2026-09-15 10:03:00 ERROR ConnectionTimeout upstream",
        ]
        levels, errors, hours = analyze(lines)
        self.assertEqual(levels["INFO"], 1)
        self.assertEqual(levels["WARN"], 1)
        self.assertEqual(levels["ERROR"], 2)
        self.assertEqual(errors["ConnectionTimeout"], 2)
        self.assertEqual(hours[10], 4)

    def test_health(self):
        self.assertEqual(health({"ERROR": 0, "WARN": 0}), "HEALTHY")
        self.assertEqual(health({"ERROR": 1, "WARN": 0}), "WATCH")
        self.assertEqual(health({"ERROR": 10, "WARN": 0}), "NEEDS ATTENTION")


if __name__ == "__main__":
    unittest.main()
