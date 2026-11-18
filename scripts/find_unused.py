"""Find Python code that nothing uses: functions, classes and imports.

Claude can run this once instead of reading every file to hunt for dead code.
It prints one line per candidate, so only the lines worth checking enter the
conversation.

Usage (run from your project folder):
    python scripts/find_unused.py              # report on the whole project
    python scripts/find_unused.py app/billing  # report only on this file or folder

How it decides:
  * A top-level function or class is a candidate when no Python file in the
    project mentions its name anywhere else (as code or as a string).
  * An import is a candidate when the file that imports it never uses it.
    Package `__init__.py` files are skipped, because their imports re-export.
  * Names that are often called from outside Python are left alone: anything
    with a decorator, `main`, `test*` names, `TestCase` classes and `__dunder__` names.

These are candidates, not verdicts. Code called by name from templates, config
files or other languages looks unused here; check each one before deleting it.
Only the Python standard library is used, and the same files are skipped as in
CODEMAP.md (gitignored files and anything that looks like a secret).
"""

import argparse
import ast
import os
import sys

# Reuse the code map's file list so both tools agree on what the project is.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_codemap import list_files  # noqa: E402


def is_exempt(node):
    """True for definitions that are usually called from outside Python code."""
    name = node.name
    if node.decorator_list:
        return True  # decorators often register a function (routes, fixtures, hooks)
    if name == "main" or name.startswith("test") or name.startswith("Test"):
        return True
    for base in getattr(node, "bases", []):
        # unittest finds TestCase subclasses itself, whatever they are called
        base_name = base.attr if isinstance(base, ast.Attribute) else getattr(base, "id", "")
        if base_name.endswith("TestCase"):
            return True
    return name.startswith("__") and name.endswith("__")


def mentioned_names(tree):
    """Every name this file mentions: variables, attributes, imports and strings."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.alias):
            names.add(node.name.split(".")[-1])
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            # getattr(obj, "name"), __all__ = ["name"], entry points written as text
            if node.value.isidentifier():
                names.add(node.value)
    return names


def used_in_file(tree):
    """Names actually used in this file's code (not counting import lines)."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value.isidentifier():
                names.add(node.value)  # covers names listed in __all__
    return names


def unused_imports(path, tree):
    """Imports in this file whose name the file never uses."""
    if os.path.basename(path) == "__init__.py":
        return []
    used = used_in_file(tree)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if alias.name == "*":
                    continue
                # "import a.b" binds "a"; "import a as b" and "from a import b" bind "b".
                bound = alias.asname or alias.name.split(".")[0]
                if bound not in used:
                    found.append({"path": path, "line": node.lineno, "kind": "import", "name": bound})
    return found


def find_unused(root, scope=""):
    """Return candidate findings as dicts: path, line, kind, name.

    The whole project is always searched for uses; `scope` only limits which
    files the findings are reported for.
    """
    trees, skipped = {}, []
    for rel in list_files(root):
        if not rel.endswith(".py"):
            continue
        try:
            with open(os.path.join(root, rel), encoding="utf-8-sig") as fh:
                trees[rel] = ast.parse(fh.read(), filename=rel)
        except (SyntaxError, UnicodeDecodeError, ValueError):
            skipped.append(rel)
    find_unused.skipped = skipped  # reported by main()
    find_unused.file_count = len(trees)

    # How many times each name is mentioned across the whole project.
    mentions = {}
    for tree in trees.values():
        for name in mentioned_names(tree):
            mentions[name] = mentions.get(name, 0) + 1

    scope = scope.replace(os.sep, "/").strip("/")
    findings = []
    for rel, tree in trees.items():
        if scope and rel != scope and not rel.startswith(scope + "/"):
            continue
        for node in tree.body:  # top-level definitions only; methods are often called dynamically
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if is_exempt(node):
                continue
            # A definition is not a mention of itself, so zero mentions means nobody uses it.
            if mentions.get(node.name, 0) == 0:
                kind = "class" if isinstance(node, ast.ClassDef) else "function"
                findings.append({"path": rel, "line": node.lineno, "kind": kind, "name": node.name})
        findings.extend(unused_imports(rel, tree))
    return sorted(findings, key=lambda f: (f["path"], f["line"], f["name"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description="List Python functions, classes and imports nothing uses.")
    parser.add_argument("scope", nargs="?", default="", help="only report on this file or folder")
    parser.add_argument("--root", default=".", help="project folder (default: current folder)")
    args = parser.parse_args(argv)

    findings = find_unused(args.root, args.scope)
    if find_unused.file_count == 0 and not find_unused.skipped:
        print("No Python files found; nothing to check.")
        return 1
    for f in findings:
        print(f"{f['path']}:{f['line']}  unused {f['kind']} {f['name']}")
    for rel in find_unused.skipped:
        print(f"could not parse: {rel}")
    print(f"{len(findings)} candidate(s) in {find_unused.file_count} Python file(s). "
          "Check each before deleting: code called by name from outside Python looks unused here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
