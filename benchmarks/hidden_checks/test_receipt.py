"""Hidden check for the add-feature task (copied in only after Claude finishes)."""

import unittest

from shop.cart import receipt_line


class ReceiptTests(unittest.TestCase):
    def test_format(self):
        self.assertEqual(receipt_line("Apple", 150), "Apple: $1.50")
        self.assertEqual(receipt_line("Pear", 5), "Pear: $0.05")


if __name__ == "__main__":
    unittest.main()
