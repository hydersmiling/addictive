import unittest

from depot.core.money import apply_percent_off, format_cents, parse_cents, split_evenly


class MoneyTests(unittest.TestCase):
    def test_format(self):
        self.assertEqual(format_cents(1999), "$19.99")
        self.assertEqual(format_cents(-50), "-$0.50")

    def test_parse(self):
        self.assertEqual(parse_cents("$19.9"), 1990)

    def test_percent(self):
        self.assertEqual(apply_percent_off(1000, 10), 900)

    def test_split(self):
        self.assertEqual(split_evenly(10, 3), [4, 3, 3])
