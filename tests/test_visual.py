"""Tests for the screenshot script and the blind visual judge (no browser, no real calls)."""

import os
import random
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "benchmarks"))
import screenshot  # noqa: E402
import visual_bench  # noqa: E402

FAKE = [sys.executable, os.path.join(ROOT, "tests", "fake_visual_judge.py")]


class VisualTests(unittest.TestCase):
    def test_screenshot_command_uses_a_throwaway_profile_and_local_file(self):
        cmd = screenshot.screenshot_command("browser", "index.html", "out.png", 800, 600, "PROFILE")
        self.assertIn("--headless=new", cmd)
        self.assertIn("--user-data-dir=PROFILE", cmd)
        self.assertTrue(cmd[-1].startswith("file:"))

    def test_missing_browser_is_reported_not_crashed(self):
        old = os.environ.get("BROWSER")
        os.environ["BROWSER"] = os.path.join(ROOT, "does-not-exist.exe")
        try:
            path = screenshot.find_browser()
            self.assertNotEqual(path, os.environ["BROWSER"])
        finally:
            if old is None:
                del os.environ["BROWSER"]
            else:
                os.environ["BROWSER"] = old

    def test_blind_labels_map_back_to_setups(self):
        shots = {"opus-plain": "o.png", "sonnet-plain": "s.png", "sonnet-mainseat": "m.png"}
        rng = random.Random(3)
        order = list(shots)
        random.Random(3).shuffle(order)  # the order the judge will see as A, B, C
        verdict = visual_bench.judge(shots, "brief", FAKE, rng=rng)
        self.assertEqual(verdict["ranking"], order)  # the fake always ranks A, B, C
        self.assertEqual(verdict["scores"][order[0]]["polish"], 9)

    def test_dry_run_runs_nothing(self):
        self.assertEqual(visual_bench.main([]), 0)


if __name__ == "__main__":
    unittest.main()
