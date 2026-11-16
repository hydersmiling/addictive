"""Tests for scripts/install.py and scripts/check_agents.py."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import check_agents  # noqa: E402
import install  # noqa: E402


class InstallTests(unittest.TestCase):
    def test_never_overwrites(self):
        with tempfile.TemporaryDirectory() as target:
            mine = os.path.join(target, "CLAUDE.md")
            with open(mine, "w", encoding="utf-8") as fh:
                fh.write("my rules")
            copied, skipped = install.install(target)
            self.assertIn("CLAUDE.md", skipped)
            with open(mine, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "my rules")
            self.assertTrue(os.path.exists(os.path.join(target, "scripts", "make_codemap.py")))
            self.assertTrue(any("big-decision.md" in c for c in copied))
            again, _ = install.install(target)
            self.assertEqual(again, [])  # second run copies nothing

    def test_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as target:
            copied, _ = install.install(target, dry_run=True)
            self.assertTrue(copied)
            self.assertEqual(os.listdir(target), [])


class CheckAgentsTests(unittest.TestCase):
    def _agent(self, text):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(text)
        tmp.close()
        self.addCleanup(os.unlink, tmp.name)
        return check_agents.check(tmp.name, check_agents.AGENT_FIELDS, need_model=True)

    def test_good_agent(self):
        self.assertEqual(self._agent("---\nname: a\ndescription: d\nmodel: haiku\n---\n"), [])

    def test_typo_and_missing_model(self):
        problems = " ".join(self._agent("---\nname: a\ndescription: d\nmodle: haiku\n---\n"))
        self.assertIn("unknown field 'modle'", problems)
        self.assertIn("no 'model' set", problems)

    def test_repo_agents_are_valid(self):
        self.assertEqual(check_agents.main(), 0)


if __name__ == "__main__":
    unittest.main()
