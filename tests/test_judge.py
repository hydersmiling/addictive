"""Tests for benchmarks/judge.py with a fake reviewer (no real calls)."""

import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "benchmarks"))
import judge  # noqa: E402

FAKE = [sys.executable, os.path.join(ROOT, "tests", "fake_reviewer.py")]


class FixedRng:
    def __init__(self, value):
        self.value = value

    def random(self):
        return self.value


def row(mode, task="fix-bug", diff="+x"):
    return {"mode": mode, "task": task, "model": "sonnet", "sample": "large", "diff": diff}


class JudgeTests(unittest.TestCase):
    def test_pairs_need_both_modes_and_output(self):
        rows = [row("baseline"), row("kit"), row("baseline", "rename"), {"mode": "kit", "task": "x", "model": "m"}]
        pairs = judge.make_pairs(rows)
        self.assertEqual([(b["task"], k["mode"]) for b, k in pairs], [("fix-bug", "kit")])

    def test_blind_labels_map_back_correctly(self):
        base, kit = row("baseline", diff="-old"), row("kit", diff="+new")
        as_a = judge.judge_pair(base, kit, "fix it", FAKE, "opus", FixedRng(0.1))   # kit shown as A
        as_b = judge.judge_pair(base, kit, "fix it", FAKE, "opus", FixedRng(0.9))   # kit shown as B
        self.assertEqual((as_a["winner"], as_b["winner"]), ("kit", "baseline"))
        self.assertEqual(as_a["kit"]["correctness"], 9)
        self.assertEqual(as_b["kit"]["correctness"], 7)

    def test_prompts_are_per_sample(self):
        prompts = judge.load_prompts()
        self.assertIn("calc_line_total", prompts[("large", "rename")])
        self.assertIn("calc_total", prompts[("small", "rename")])
        self.assertNotEqual(prompts[("large", "rename")], prompts[("small", "rename")])

    def test_dry_run(self):
        import json
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as fh:
            fh.write(json.dumps(row("baseline")) + "\n" + json.dumps(row("kit")) + "\n")
        self.addCleanup(os.unlink, fh.name)
        self.assertEqual(judge.main([fh.name]), 0)


if __name__ == "__main__":
    unittest.main()
