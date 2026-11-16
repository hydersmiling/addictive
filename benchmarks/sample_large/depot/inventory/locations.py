"""Warehouse bin locations."""


class Locations:
    def __init__(self):
        self.bins = {}

    def assign(self, sku, bin_code):
        self.bins[sku] = bin_code

    def find(self, sku):
        return self.bins.get(sku, "UNASSIGNED")

    def skus_in_aisle(self, aisle):
        return sorted(s for s, b in self.bins.items() if b.startswith(aisle))
