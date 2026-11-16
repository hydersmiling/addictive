"""Guards that keep the kit safe for users' codebases and free of personal data.

These fail the build if someone later adds network access to a script, a hook,
a permission bypass, or commits an email address or a personal folder path.
"""

import ast
import json
import os
import re
import subprocess
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

NETWORK_MODULES = {"socket", "urllib", "http", "requests", "httpx", "aiohttp",
                   "ftplib", "smtplib", "telnetlib", "xmlrpc", "websocket", "paramiko"}
OUR_SCRIPTS = ["scripts/make_codemap.py", "scripts/measure_tokens.py", "scripts/install.py",
               "scripts/check_agents.py", "benchmarks/run_benchmark.py"]


def tracked_text_files():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True,
                         text=True, encoding="utf-8", check=True).stdout
    for rel in filter(None, out.split("\0")):
        if rel.endswith((".png", ".jpg", ".gif", ".ico")) or not os.path.exists(os.path.join(ROOT, rel)):
            continue
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
            yield rel, fh.read()


class PrivacyGuardTests(unittest.TestCase):
    def test_scripts_have_no_network_access(self):
        for rel in OUR_SCRIPTS:
            with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                tree = ast.parse(fh.read())
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                for name in names:
                    self.assertNotIn(name.split(".")[0], NETWORK_MODULES, f"{rel} imports {name}")

    def test_no_hooks_or_permission_bypass(self):
        with open(os.path.join(ROOT, ".claude", "settings.json"), encoding="utf-8") as fh:
            settings = json.load(fh)
        self.assertNotIn("hooks", settings)
        self.assertNotIn("allow", settings.get("permissions", {}))
        for folder, _dirs, files in os.walk(os.path.join(ROOT, ".claude")):
            for name in files:
                with open(os.path.join(folder, name), encoding="utf-8") as fh:
                    text = fh.read()
                self.assertNotIn("bypassPermissions", text, name)
                self.assertNotRegex(text, r"(?m)^hooks:", name)

    def test_no_personal_data_committed(self):
        email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
        allowed_email = re.compile(r"@(users\.noreply\.github\.com|example\.(invalid|com|org)|t)$")
        user_path = re.compile(r"[A-Za-z]:\\+Users\\+(?!me\\|you\\|<)[A-Za-z0-9._-]+|/(home|Users)/(?!me/|you/|<)[a-z0-9._-]+/",
                               re.IGNORECASE)
        for rel, text in tracked_text_files():
            if rel.startswith("third_party/") or rel.startswith("optional/"):
                continue  # licence notices legitimately name their authors
            for m in email.finditer(text):
                self.assertRegex(m.group(), allowed_email, f"email in {rel}: {m.group()}")
            self.assertIsNone(user_path.search(text), f"personal path in {rel}")

    def test_no_real_secrets_committed(self):
        secret = re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}"
                            r"|-----BEGIN [A-Z ]*PRIVATE KEY-----")
        for rel, text in tracked_text_files():
            if rel == "scripts/make_codemap.py" or rel.startswith("tests/"):
                continue  # these hold the detection patterns and fake test values
            self.assertIsNone(secret.search(text), f"possible secret in {rel}")


if __name__ == "__main__":
    unittest.main()
