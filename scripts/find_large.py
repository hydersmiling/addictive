"""Find files and functions that have grown too big to work with comfortably.

A large file costs tokens every time Claude has to read it, and a long function is
hard to change safely. This prints one line per candidate, biggest first, so Claude
can decide what to split without opening every file.

Usage (run from your project folder):
    python scripts/find_large.py                 # files over 400 lines, functions over 80
    python scripts/find_large.py --file-lines 300 --function-lines 60
    python scripts/find_large.py app/billing     # only this file or folder

Files are counted by lines of any text file the code map includes (gitignored files
and anything that looks like a secret are skipped). Functions and classes are
measured in Python files only. These are candidates, not orders: a long file of
data or generated code can be fine as it is.
"""

import argparse
import ast
import os
import sys

# Reuse the code map's file list so both tools agree on what the project is.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_codemap import list_files  # noqa: E402

SKIP_SUFFIXES = (".lock", ".min.js", ".min.css", ".map", ".svg", ".png", ".jpg", ".ico", ".pdf")


def count_lines(path):
    """Number of lines in a text file, or None for binary or unreadable files."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None  # binary
    return data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1)


def long_definitions(path, limit):
    """(name, start line, length) for Python functions and classes longer than limit."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            tree = ast.parse(fh.read())
    except (SyntaxError, ValueError, OSError):
        return []
    found = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            length = (node.end_lineno or node.lineno) - node.lineno + 1
            if length > limit:
                found.append((node.name, node.lineno, length))
    return found


def scan(root, only="", file_limit=400, function_limit=80):
    """Return (big files, long definitions) as sorted lists of tuples."""
    files, defs = [], []
    for rel in list_files(root):
        if only and not (rel == only or rel.startswith(only.rstrip("/") + "/")):
            continue
        if rel.lower().endswith(SKIP_SUFFIXES):
            continue
        path = os.path.join(root, rel)
        lines = count_lines(path)
        if lines and lines > file_limit:
            files.append((lines, rel))
        if rel.endswith(".py"):
            for name, start, length in long_definitions(path, function_limit):
                defs.append((length, f"{rel}:{start}", name))
    return sorted(files, reverse=True), sorted(defs, reverse=True)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="List files and functions that have grown too big.")
    parser.add_argument("only", nargs="?", default="", help="limit to this file or folder")
    parser.add_argument("--root", default=".", help="project folder (default: .)")
    parser.add_argument("--file-lines", type=int, default=400)
    parser.add_argument("--function-lines", type=int, default=80)
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    only = args.only.replace(os.sep, "/").strip("./") if args.only not in ("", ".") else ""
    files, defs = scan(root, only, args.file_lines, args.function_lines)
    for lines, rel in files:
        print(f"file  {lines:>5} lines  {rel}")
    for length, where, name in defs:
        print(f"def   {length:>5} lines  {where}  {name}")
    if not files and not defs:
        print(f"Nothing over {args.file_lines} lines per file or {args.function_lines} per function.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
