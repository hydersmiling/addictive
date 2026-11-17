import unittest

from depot.core.errors import OutOfStock
from depot.inventory.stock import Stock
from depot.inventory.transfers import transfer


class StockTests(unittest.TestCase):
    def test_take_and_receive(self):
        s = Stock()
        s.receive("ABC-0001", 5)
        s.take("ABC-0001", 2)
        self.assertEqual(s.on_hand("ABC-0001"), 3)

    def test_out_of_stock(self):
        with self.assertRaises(OutOfStock):
            Stock().take("ABC-0001", 1)

    def test_transfer(self):
        a, b = Stock(), Stock()
        a.receive("ABC-0001", 4)
        transfer(a, b, "ABC-0001", 3)
        self.assertEqual((a.on_hand("ABC-0001"), b.on_hand("ABC-0001")), (1, 3))
