"""Tests for scripts/make_codemap.py. Run: python -m unittest discover tests"""

import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import make_codemap  # noqa: E402


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def git(root, *args):
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


class CodemapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        write(self.root, "app/main.py", '"""Start the web app."""\n\ndef run():\n    pass\n\nclass Server:\n    pass\n')
        write(self.root, "app/util.js", "// Small helpers for dates\nexport const x = 1;\n")
        write(self.root, "README.md", "# Demo project\n")
        write(self.root, ".env", "API_KEY=sk-abcdefghijklmnopqrstuvwx\n")
        write(self.root, "config/credentials.json", '{"password": "hunter2"}\n')
        write(self.root, "scripts/measure_tokens.py", '"""Count tokens."""\n')
        write(self.root, "leaky.py", '"""password = hunter2"""\n')
        write(self.root, "node_modules/lib/index.js", "// should never appear\n")
        write(self.root, "ignored/thing.py", '"""Ignored by git."""\n')
        write(self.root, ".gitignore", "ignored/\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_summaries_and_symbols(self):
        text = make_codemap.build_map(self.root)
        self.assertIn("`main.py` - Start the web app. | run(), class Server", text)
        self.assertIn("`util.js` - Small helpers for dates", text)
        self.assertIn("`README.md` - Demo project", text)

    def test_frontmatter_description(self):
        write(self.root, "agents/a.md", "---\nname: a\ndescription: Finds code fast.\n---\nBody\n")
        write(self.root, "agents/b.md", "---\nname: b\ndescription: >\n  Folded line one\n  and two.\nmodel: haiku\n---\n")
        text = make_codemap.build_map(self.root)
        self.assertIn("`a.md` - Finds code fast.", text)
        self.assertIn("`b.md` - Folded line one and two.", text)

    def test_secrets_never_appear(self):
        text = make_codemap.build_map(self.root)
        self.assertNotIn(".env", text)
        self.assertNotIn("credentials", text)
        self.assertNotIn("sk-", text)
        self.assertNotIn("hunter2", text)
        # A file whose summary looks like a secret is listed, but with no summary.
        self.assertIn("- `leaky.py`\n", text)

    def test_whole_name_matching_keeps_normal_files(self):
        text = make_codemap.build_map(self.root)
        self.assertIn("measure_tokens.py", text)

    def test_skips_junk_dirs_without_git(self):
        text = make_codemap.build_map(self.root)
        self.assertNotIn("node_modules", text)

    def test_respects_gitignore_and_stamps_commit(self):
        git(self.root, "init", "-q")
        git(self.root, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
        git(self.root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x")
        text = make_codemap.build_map(self.root)
        self.assertNotIn("thing.py", text)
        self.assertRegex(text.splitlines()[0], r"commit=[0-9a-f]{7,}")

    def test_check_mode(self):
        out = os.path.join(self.root, "CODEMAP.md")
        self.assertEqual(make_codemap.main([self.root, "--check"]), 1)  # missing
        self.assertEqual(make_codemap.main([self.root]), 0)
        self.assertTrue(os.path.exists(out))
        self.assertEqual(make_codemap.main([self.root, "--check"]), 0)  # fresh
        write(self.root, "app/new.py", '"""New module."""\n')
        self.assertEqual(make_codemap.main([self.root, "--check"]), 1)  # stale


if __name__ == "__main__":
    unittest.main()
