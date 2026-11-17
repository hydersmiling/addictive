"""Stock levels per SKU."""

from depot.core.errors import OutOfStock


class Stock:
    def __init__(self):
        self.levels = {}

    def receive(self, sku, quantity):
        self.levels[sku] = self.levels.get(sku, 0) + quantity

    def take(self, sku, quantity):
        available = self.levels.get(sku, 0)
        if quantity > available:
            raise OutOfStock(f"{sku}: need {quantity}, have {available}")
        self.levels[sku] = available - quantity

    def on_hand(self, sku):
        return self.levels.get(sku, 0)
