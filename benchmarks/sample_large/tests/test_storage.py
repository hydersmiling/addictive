import os
import tempfile
import unittest

from depot.storage.json_store import JsonStore
from depot.storage.memory_store import MemoryStore
from depot.storage.migrations import migrate


class StorageTests(unittest.TestCase):
    def test_memory(self):
        m = MemoryStore()
        m.put("order:1", "x")
        self.assertEqual(m.keys("order:"), ["order:1"])

    def test_json_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JsonStore(os.path.join(tmp, "db.json"))
            store.save({"a": 1})
            self.assertEqual(store.load(), {"a": 1})

    def test_migrate(self):
        self.assertEqual(migrate({})["status"], "open")
