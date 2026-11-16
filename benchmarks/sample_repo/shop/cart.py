"""Shopping cart: add items and compute the total."""

from shop.money import apply_percent_off


class Cart:
    def __init__(self):
        self.items = []  # list of (name, cents, quantity)

    def add(self, name, cents, quantity=1):
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        self.items.append((name, cents, quantity))

    def count(self):
        return sum(q for _name, _cents, q in self.items)


def calc_total(cart, percent_off=0):
    """Total price of the cart in cents, after an optional percentage discount."""
    subtotal = sum(cents for _name, cents, _q in cart.items)
    return apply_percent_off(subtotal, percent_off)
