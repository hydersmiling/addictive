"""Write CODEMAP.md: a short map of a code project for Claude Code.

The map lists every file with a one-line summary, plus top-level function
and class names for Python files. Claude can read this one small file to find
code instead of opening many files, which saves tokens.

Usage (run from your project folder):
    python scripts/make_codemap.py            # write CODEMAP.md
    python scripts/make_codemap.py --check    # exit 1 if CODEMAP.md is out of date

Safety rules this script follows:
  * Files ignored by git (.gitignore) are left out.
  * Files that look like secrets (.env, keys, credentials) are listed by
    nothing at all: not their name, not their contents.
  * A summary line that looks like it holds a password or token is dropped.

Only the Python standard library is used, so there is nothing to install.
"""

import argparse
import ast
import fnmatch
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------------------
# Settings you might want to change
# ---------------------------------------------------------------------------

# Folders we never look inside, even when the project is not a git repo.
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".next", ".nuxt", "target", ".idea", ".vscode",
    ".pytest_cache", ".mypy_cache", "coverage",
}

# File name patterns that may hold secrets. Matching files are skipped completely.
SECRET_PATTERNS = [
    ".env", ".env.*", "*.env", "*.pem", "*.key", "*.p12", "*.pfx", "*.keystore",
    "id_rsa*", "id_ed25519*", "id_ecdsa*", "credentials*", "*.credentials",
    "secret.*", "secrets.*", "*.secret", "*.secrets", "token.json", "tokens.json",
    "*.token", ".netrc", ".npmrc", ".pypirc", "*.kdbx", "service-account*.json",
]
# Note: patterns are whole-name on purpose. "*token*" would also hide harmless
# files such as measure_tokens.py or tokenizer.py.

# Lock files and generated files: listed, but never opened (they are huge and boring).
NO_SUMMARY_PATTERNS = [
    "*.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock",
    "*.min.js", "*.min.css", "*.map",
]

# Text that suggests a line contains a real secret value.
SECRET_TEXT = re.compile(
    r"(sk-[A-Za-z0-9_-]{16,}"            # OpenAI / Anthropic style keys
    r"|gh[pousr]_[A-Za-z0-9]{20,}"       # GitHub tokens
    r"|AKIA[0-9A-Z]{16}"                 # AWS access key IDs
    r"|xox[abpr]-[A-Za-z0-9-]{10,}"      # Slack tokens
    r"|-----BEGIN [A-Z ]*PRIVATE KEY"    # private key blocks
    r"|sk_(live|test)_[A-Za-z0-9]{10,}"  # Stripe keys
    r"|AIza[0-9A-Za-z_-]{35}"            # Google API keys
    r"|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"  # JSON web tokens
    r"|(password|passwd|secret|api_?key|token)\s*[:=]\s*\S+)",
    re.IGNORECASE,
)

MAX_SUMMARY = 90         # characters per summary line
MAX_SYMBOLS = 12         # function/class names shown per Python file
READ_BYTES = 8192        # we only read the start of each file
HEADER_PREFIX = "<!-- codemap"


# ---------------------------------------------------------------------------
# Step 1: decide which files belong in the map
# ---------------------------------------------------------------------------

def run_git(root, *args):
    """Run a git command in `root`. Return its output, or None if git fails."""
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=True,
        )
        return result.stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def matches_any(name, patterns):
    """True if the file name matches any pattern (case-insensitive)."""
    lower = name.lower()
    return any(fnmatch.fnmatch(lower, p.lower()) for p in patterns)


def is_secret(path):
    """True if this file name looks like it may contain secrets."""
    return matches_any(os.path.basename(path), SECRET_PATTERNS)


def list_files(root, exclude=("CODEMAP.md",)):
    """Return the project's files as sorted forward-slash paths.

    In a git repo we ask git, which already respects .gitignore. Outside git
    we walk the folders ourselves and skip the usual junk folders.
    """
    out = run_git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    if out is not None:
        paths = [p for p in out.split("\0") if p]
        # `git ls-files` still lists deleted-but-not-committed files; drop them.
        paths = [p for p in paths if os.path.isfile(os.path.join(root, p))]
    else:
        paths = []
        for folder, dirs, files in os.walk(root):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for f in files:
                rel = os.path.relpath(os.path.join(folder, f), root)
                paths.append(rel.replace(os.sep, "/"))

    keep = []
    for p in paths:
        parts = p.split("/")
        if any(part in SKIP_DIRS for part in parts[:-1]):
            continue
        if is_secret(p):
            continue
        if os.path.islink(os.path.join(root, p)):
            continue  # a link could point outside the project (e.g. to ~/.ssh)
        if p in exclude:
            continue  # never list the map inside itself, or it changes every run
        keep.append(p)
    return sorted(keep)


# ---------------------------------------------------------------------------
# Step 2: describe each file in one line
# ---------------------------------------------------------------------------

def read_start(path):
    """Read the first few KB of a file as text. Return None for binary files."""
    try:
        with open(path, "rb") as fh:
            data = fh.read(READ_BYTES)
    except OSError:
        return None
    if b"\0" in data:
        return None  # a null byte means binary (image, zip, ...)
    return data.decode("utf-8", errors="replace")


def clean(line):
    """Shorten a summary line and drop it if it looks like a secret."""
    line = " ".join(line.split())
    if SECRET_TEXT.search(line):
        return ""
    if len(line) > MAX_SUMMARY:
        line = line[: MAX_SUMMARY - 3].rstrip() + "..."
    return line


def python_summary(text):
    """Return (docstring first line, list of top-level def/class names)."""
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return "", []
    doc = ast.get_docstring(tree) or ""
    first = doc.strip().splitlines()[0] if doc.strip() else ""
    names = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            names.append(f"class {node.name}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(f"{node.name}()")
    return first, names


COMMENT_STARTS = ("#", "//", "/*", "*", "--", "<!--", ";", "%", '"""', "'''")


def frontmatter_description(lines):
    """Read `description:` from a YAML header (--- ... ---), as used by skills and agents.

    Handles both `description: one line` and the folded form:
        description: >
          first line
          second line
    """
    for i, raw in enumerate(lines[1:60], start=1):
        if raw.strip() == "---":
            break  # end of the header
        if raw.startswith("description:"):
            value = raw.split(":", 1)[1].strip()
            if value in (">", "|", ">-", "|-", ""):
                folded = []
                for nxt in lines[i + 1:]:
                    if not nxt.startswith((" ", "\t")):
                        break
                    folded.append(nxt.strip())
                value = " ".join(folded)
            return value.strip("\"'")
    return ""


def generic_summary(text, name):
    """First heading or first comment line near the top of a file."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        return frontmatter_description(lines)
    for raw in lines[:40]:
        line = raw.strip()
        if not line or line.startswith("#!"):
            continue  # skip blank lines and shebangs like #!/usr/bin/env python
        if name.lower().endswith((".md", ".markdown", ".rst", ".txt")):
            return line.lstrip("#= ").strip()
        for start in COMMENT_STARTS:
            if line.startswith(start):
                body = line[len(start):].strip(" */-!>#")
                if body and not body.startswith(("eslint", "@ts-", "prettier", "type:")):
                    return body
                break
        else:
            return ""  # first real line is code, not a comment: no summary
    return ""


def describe(root, rel):
    """Return the map line(s) for one file."""
    name = os.path.basename(rel)
    if matches_any(name, NO_SUMMARY_PATTERNS):
        return ""
    text = read_start(os.path.join(root, rel))
    if text is None:
        return "(binary)"
    if rel.endswith(".py"):
        # Read the whole Python file so ast sees every top-level name.
        try:
            with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            return ""
        first, names = python_summary(text)
        summary = clean(first)
        if names:
            shown = ", ".join(names[:MAX_SYMBOLS])
            more = f" +{len(names) - MAX_SYMBOLS} more" if len(names) > MAX_SYMBOLS else ""
            summary = (summary + " | " if summary else "") + shown + more
        return summary
    return clean(generic_summary(text, name))


# ---------------------------------------------------------------------------
# Step 3: put it together
# ---------------------------------------------------------------------------

def build_map(root, out_name="CODEMAP.md"):
    """Return the full CODEMAP.md text for the project in `root`."""
    files = list_files(root, exclude=(out_name.replace(os.sep, "/"),))
    commit = (run_git(root, "rev-parse", "--short", "HEAD") or "").strip() or "none"

    lines = [
        f"{HEADER_PREFIX} commit={commit} files={len(files)} -->",
        "# Code map",
        "",
        "Generated by `scripts/make_codemap.py`. Do not edit by hand; re-run the script.",
        "Each line: path - what the file is for | top-level functions and classes.",
        "",
    ]
    current_dir = None
    for rel in files:
        folder = rel.rsplit("/", 1)[0] if "/" in rel else "."
        if folder != current_dir:
            lines.append("")
            lines.append(f"## {folder}/")
            current_dir = folder
        summary = describe(root, rel)
        name = rel.rsplit("/", 1)[-1]
        lines.append(f"- `{name}`" + (f" - {summary}" if summary else ""))
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    # Windows consoles default to an old encoding; force UTF-8 so printing never crashes.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Write a CODEMAP.md for Claude Code.")
    parser.add_argument("root", nargs="?", default=".", help="project folder (default: .)")
    parser.add_argument("--out", default="CODEMAP.md", help="output file, relative to root")
    parser.add_argument("--check", action="store_true",
                        help="do not write; exit 1 if the map is missing or out of date")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    out_path = os.path.join(root, args.out)
    fresh = build_map(root, args.out)

    if args.check:
        try:
            with open(out_path, encoding="utf-8") as fh:
                existing = fh.read()
        except OSError:
            print(f"STALE: {args.out} does not exist. Run: python scripts/make_codemap.py")
            return 1
        existing = existing.replace("\r\n", "\n")
        # Compare everything except the header line. The header holds the commit
        # hash, which changes every time CODEMAP.md itself is committed, so
        # comparing it would make the map look stale forever.
        if existing.split("\n", 1)[-1] != fresh.split("\n", 1)[-1]:
            print(f"STALE: {args.out} is out of date. Run: python scripts/make_codemap.py")
            return 1
        old_commit = existing.split("commit=", 1)[-1].split()[0] if "commit=" in existing else "?"
        new_commit = fresh.split("commit=", 1)[-1].split()[0]
        note = "" if old_commit == new_commit else f" (built at {old_commit}, now {new_commit}; files unchanged)"
        print(f"OK: {args.out} is up to date{note}.")
        return 0

    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(fresh)
    count = fresh.splitlines()[0].split("files=")[1].split()[0]
    print(f"Wrote {args.out} ({count} files, {len(fresh)} characters).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
