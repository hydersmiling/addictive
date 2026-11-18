"""Tests for scripts/find_unused.py. Run: python -m unittest discover tests"""

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import find_unused  # noqa: E402


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class FindUnusedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        write(self.root, "app/money.py", (
            "import os\n"
            "import json\n"
            "from math import floor, ceil\n"
            "\n"
            "def fmt(x):\n"
            "    return json.dumps(floor(x))\n"
            "\n"
            "def old_fmt(x):\n"
            "    return str(x)\n"
            "\n"
            "class Unused:\n"
            "    pass\n"
            "\n"
            "@register\n"
            "def plugin_hook():\n"
            "    pass\n"
            "\n"
            "def by_name():\n"
            "    pass\n"
            "\n"
            "def main():\n"
            "    pass\n"
        ))
        write(self.root, "app/run.py", (
            "from app.money import fmt\n"
            "HANDLER = 'by_name'\n"
            "print(fmt(2))\n"
        ))
        write(self.root, "app/__init__.py", "from app.money import fmt\n")
        write(self.root, "tests/test_money.py", (
            "import unittest\n"
            "def test_fmt():\n    pass\n"
            "class MoneyChecks(unittest.TestCase):\n    pass\n"
        ))
        write(self.root, "broken.py", "def (:\n")

    def tearDown(self):
        self.tmp.cleanup()

    def names(self, scope=""):
        return {(f["path"], f["kind"], f["name"]) for f in find_unused.find_unused(self.root, scope)}

    def test_reports_unused_function_class_and_imports(self):
        found = self.names()
        self.assertIn(("app/money.py", "function", "old_fmt"), found)
        self.assertIn(("app/money.py", "class", "Unused"), found)
        self.assertIn(("app/money.py", "import", "os"), found)
        self.assertIn(("app/money.py", "import", "ceil"), found)

    def test_keeps_used_and_likely_dynamic_code(self):
        found = {name for _, _, name in self.names()}
        for kept in ("fmt", "json", "floor", "plugin_hook", "by_name", "main", "test_fmt", "MoneyChecks"):
            self.assertNotIn(kept, found)

    def test_init_reexports_are_not_unused_imports(self):
        self.assertFalse(any(p == "app/__init__.py" for p, _, _ in self.names()))

    def test_scope_limits_the_report_but_not_the_search(self):
        found = self.names("app/run.py")
        self.assertEqual(found, set())  # fmt is used; HANDLER is a variable, not reported

    def test_report_lists_lines_and_skipped_files(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = find_unused.main(["--root", self.root])
        text = out.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("app/money.py:8  unused function old_fmt", text)
        self.assertIn("could not parse: broken.py", text)

    def test_no_python_files_is_said_plainly(self):
        with tempfile.TemporaryDirectory() as empty:
            write(empty, "notes.md", "# hi\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = find_unused.main(["--root", empty])
        self.assertEqual(code, 1)
        self.assertIn("No Python files", out.getvalue())


if __name__ == "__main__":
    unittest.main()
