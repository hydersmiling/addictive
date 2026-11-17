"""Tests for scripts/measure_tokens.py, using fake logs (never your real ones)."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import measure_tokens  # noqa: E402


def reply(msg_id, model, inp, out, cache_read=0, req="r"):
    return json.dumps({
        "type": "assistant", "requestId": req,
        "message": {"id": msg_id, "model": model, "usage": {
            "input_tokens": inp, "output_tokens": out,
            "cache_creation_input_tokens": 0, "cache_read_input_tokens": cache_read}},
    })


class MeasureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = os.path.join(self.tmp.name, "abc.jsonl")
        lines = [
            reply("m1", "claude-opus-5-5", 10, 100, 50, "r1"),
            reply("m1", "claude-opus-5-5", 10, 100, 50, "r1"),   # same reply, second content block
            reply("m2", "claude-opus-5-5", 5, 20, 0, "r2"),
            reply("s1", "<synthetic>", 999, 999),                 # not a real API call
            json.dumps({"type": "user", "message": {"content": "hi"}}),
            '{"half written',                                     # broken last line
        ]
        with open(self.log, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        sub_dir = os.path.join(self.tmp.name, "abc", "subagents")
        os.makedirs(sub_dir)
        with open(os.path.join(sub_dir, "agent-1.jsonl"), "w", encoding="utf-8") as fh:
            fh.write(reply("h1", "claude-haiku-5-5", 3, 30, 0, "r9"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_counts_each_reply_once(self):
        result = measure_tokens.measure(self.log)
        opus = result["main"]["claude-opus-5-5"]
        self.assertEqual(opus["replies"], 2)
        self.assertEqual(opus["input_tokens"], 15)
        self.assertEqual(opus["output_tokens"], 120)
        self.assertEqual(opus["cache_read_input_tokens"], 50)

    def test_skips_synthetic(self):
        self.assertNotIn("<synthetic>", measure_tokens.measure(self.log)["main"])

    def test_includes_subagents(self):
        result = measure_tokens.measure(self.log)
        self.assertEqual(result["subagent_logs"], 1)
        self.assertEqual(result["subagents"]["claude-haiku-5-5"]["output_tokens"], 30)

    def test_profile(self):
        p = measure_tokens.measure(self.log)["profile"]
        # two real replies: contexts 10+0+50=60 and 5+0+0=5
        self.assertEqual((p["replies"], p["floor"], p["peak"], p["reread"]), (2, 60, 60, 65))

    def test_project_folder_name(self):
        self.assertTrue(measure_tokens.project_folder_name("C:\\Users\\me\\my app").endswith("-me-my-app"))


if __name__ == "__main__":
    unittest.main()
