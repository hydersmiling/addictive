"""Tests for benchmarks/run_benchmark.py using a fake Claude (no real calls, no cost)."""

import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "benchmarks"))
import run_benchmark  # noqa: E402

FAKE = [sys.executable, os.path.join(ROOT, "tests", "fake_claude.py")]


def task(task_id):
    with open(os.path.join(ROOT, "benchmarks", "tasks.json"), encoding="utf-8") as fh:
        return next(t for t in json.load(fh)["tasks"] if t["id"] == task_id)


class BenchmarkTests(unittest.TestCase):
    def test_offline_guard(self):
        self.assertNotEqual(os.path.basename(FAKE[1]), "claude")

    def test_fix_bug_passes_in_both_modes(self):
        for mode in ("baseline", "kit"):
            row = run_benchmark.run_one(task("fix-bug"), mode, "haiku", FAKE)
            self.assertTrue(row["passed"], row["failures"])
            self.assertEqual((row["lines_added"], row["lines_removed"]), (1, 1))

    def test_unsolved_task_fails(self):
        row = run_benchmark.run_one(task("rename"), "baseline", "haiku", FAKE)
        self.assertFalse(row["passed"])

    def test_answer_check(self):
        row = run_benchmark.run_one(task("locate"), "baseline", "haiku", FAKE)
        self.assertTrue(row["passed"], row["failures"])

    def test_kit_mode_installs_kit_and_map(self):
        row = run_benchmark.run_one(task("locate"), "kit", "haiku", FAKE)
        self.assertTrue(row["passed"])
        self.assertEqual(row["lines_added"] + row["lines_removed"], 0)  # kit files are not counted

    def test_dry_run_runs_nothing(self):
        self.assertEqual(run_benchmark.main(["--claude-cmd", "does-not-exist"]), 0)


if __name__ == "__main__":
    unittest.main()
