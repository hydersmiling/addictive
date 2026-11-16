"""Tests for the cart. One of these fails because of a bug in shop/cart.py."""

import unittest

from shop.cart import Cart, calc_total


class CartTests(unittest.TestCase):
    def test_single_item(self):
        cart = Cart()
        cart.add("apple", 150)
        self.assertEqual(calc_total(cart), 150)

    def test_quantity_counts(self):
        cart = Cart()
        cart.add("apple", 150, quantity=3)
        self.assertEqual(calc_total(cart), 450)

    def test_discount(self):
        cart = Cart()
        cart.add("pear", 1000, quantity=2)
        self.assertEqual(calc_total(cart, percent_off=10), 1800)


if __name__ == "__main__":
    unittest.main()
