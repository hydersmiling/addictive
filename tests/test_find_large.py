"""Tests for scripts/find_large.py."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import find_large  # noqa: E402


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path) or root, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class FindLargeTests(unittest.TestCase):
    def test_reports_big_files_and_long_functions(self):
        with tempfile.TemporaryDirectory() as root:
            body = "\n".join(f"    x{i} = {i}" for i in range(30))
            write(root, "app/big.py", "def huge():\n" + body + "\n    return 1\n" + "\n" * 20)
            write(root, "app/small.py", "def tiny():\n    return 1\n")
            write(root, "notes.md", "line\n" * 50)
            files, defs = find_large.scan(root, file_limit=40, function_limit=10)
            self.assertEqual([rel for _n, rel in files], ["app/big.py", "notes.md"])  # 52 lines, then 50
            self.assertEqual([(where, name) for _n, where, name in defs], [("app/big.py:1", "huge")])

    def test_folder_filter_and_secret_files_skipped(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, "a/one.py", "x = 1\n" * 50)
            write(root, "b/two.py", "x = 1\n" * 50)
            write(root, ".env", "KEY=1\n" * 50)
            files, _ = find_large.scan(root, only="a", file_limit=10)
            self.assertEqual([rel for _n, rel in files], ["a/one.py"])
            all_files, _ = find_large.scan(root, file_limit=10)
            self.assertNotIn(".env", [rel for _n, rel in all_files])


if __name__ == "__main__":
    unittest.main()
