"""Tests for the Claude Code plugin manifests and the rules-only install used by /mainseat:setup."""

import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import install  # noqa: E402


def load(name):
    with open(os.path.join(ROOT, ".claude-plugin", name), encoding="utf-8") as fh:
        return json.load(fh)


class PluginTests(unittest.TestCase):
    def test_manifest_lists_every_core_agent(self):
        listed = sorted(os.path.basename(p) for p in load("plugin.json")["agents"])
        on_disk = sorted(f for f in os.listdir(os.path.join(ROOT, ".claude", "agents")) if f.endswith(".md"))
        self.assertEqual(listed, on_disk)

    def test_manifest_paths_exist_and_stay_inside(self):
        data = load("plugin.json")
        for path in data["agents"] + data["skills"]:
            self.assertTrue(path.startswith("./") and ".." not in path, path)
            self.assertTrue(os.path.exists(os.path.join(ROOT, path)), path)

    def test_marketplace_points_at_this_plugin(self):
        market, plugin = load("marketplace.json"), load("plugin.json")
        self.assertEqual(market["plugins"][0]["name"], plugin["name"])
        self.assertEqual(market["plugins"][0]["source"], "./")

    def test_version_matches_changelog(self):
        with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as fh:
            heading = next(line for line in fh if line.startswith("## "))
        self.assertIn(load("plugin.json")["version"], heading)

    def test_rules_only_install_skips_agents_and_skills(self):
        with tempfile.TemporaryDirectory() as target:
            copied, _ = install.install(target, dry_run=True, rules_only=True)
            norm = [c.replace(os.sep, "/") for c in copied]
            self.assertIn("CLAUDE.md", norm)
            self.assertIn("scripts/make_codemap.py", norm)
            self.assertFalse(any(c.startswith(".claude/agents") or c.startswith(".claude/skills") for c in norm))


if __name__ == "__main__":
    unittest.main()
