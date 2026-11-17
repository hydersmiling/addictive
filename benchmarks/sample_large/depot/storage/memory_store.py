"""In-memory key-value store (tests and demos)."""


class MemoryStore:
    def __init__(self):
        self.data = {}

    def put(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

    def keys(self, prefix=""):
        return sorted(k for k in self.data if k.startswith(prefix))
