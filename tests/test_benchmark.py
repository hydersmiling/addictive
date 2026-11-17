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

    def test_rename_grader_accepts_a_correct_rename(self):
        import shutil
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            repo = os.path.join(tmp, "repo")
            shutil.copytree(run_benchmark.SAMPLE, repo)
            for rel in ("shop/cart.py", "tests/test_cart.py"):
                path = os.path.join(repo, rel)
                with open(path, encoding="utf-8") as fh:
                    text = fh.read().replace("calc_total", "cart_total")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)
            shutil.copy2(os.path.join(run_benchmark.HIDDEN, "check_rename.py"), repo)
            result = subprocess.run([sys.executable, "check_rename.py"], cwd=repo, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def _large_copy(self, tmp):
        import shutil
        repo = os.path.join(tmp, "repo")
        shutil.copytree(run_benchmark.SAMPLES["large"][0], repo)
        return repo

    def _run_check(self, repo, *names, cmd):
        import shutil
        import subprocess
        for name in names:
            shutil.copy2(os.path.join(run_benchmark.SAMPLES["large"][2], name), repo)
        return subprocess.run([sys.executable, *cmd], cwd=repo, capture_output=True, text=True)

    def test_large_graders_accept_correct_answers(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._large_copy(tmp)
            report = os.path.join(repo, "depot", "reports", "sales_report.py")
            with open(report, "a", encoding="utf-8") as fh:
                fh.write("\n\nfrom depot.core.money import format_cents\n\n\n"
                         "def order_summary(order):\n"
                         "    return f\"Order {order.order_id}: {order.item_count()} items, total {format_cents(total(order))}\"\n")
            r = self._run_check(repo, "test_order_summary.py", "check_reuse.py", cmd=["-m", "unittest", "test_order_summary"])
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(self._run_check(repo, cmd=["check_reuse.py"]).returncode, 0)
            for folder, _dirs, files in os.walk(repo):
                for name in files:
                    if name.endswith(".py"):
                        path = os.path.join(folder, name)
                        with open(path, encoding="utf-8") as fh:
                            text = fh.read()
                        with open(path, "w", encoding="utf-8") as fh:
                            fh.write(text.replace("calc_line_total", "line_total"))
            r = self._run_check(repo, "check_rename_large.py", cmd=["check_rename_large.py"])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_reuse_check_rejects_hand_rolled_formatting(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._large_copy(tmp)
            report = os.path.join(repo, "depot", "reports", "sales_report.py")
            with open(report, "a", encoding="utf-8") as fh:
                fh.write("\n\ndef order_summary(order):\n    return f\"${total(order) / 100:.2f}\"\n")
            self.assertNotEqual(self._run_check(repo, "check_reuse.py", cmd=["check_reuse.py"]).returncode, 0)

    def test_dry_run_runs_nothing(self):
        self.assertEqual(run_benchmark.main(["--claude-cmd", "does-not-exist"]), 0)


if __name__ == "__main__":
    unittest.main()
