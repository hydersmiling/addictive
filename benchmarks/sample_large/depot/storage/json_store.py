"""JSON-file store."""

import json
import os


class JsonStore:
    def __init__(self, path):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, encoding="utf-8") as fh:
            return json.load(fh)

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, sort_keys=True)
