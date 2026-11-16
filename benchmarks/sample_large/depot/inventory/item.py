"""Catalogue items."""

from dataclasses import dataclass

from depot.core.validation import require_positive, require_sku


@dataclass
class Item:
    sku: str
    name: str
    unit_cents: int
    weight_grams: int = 0

    def __post_init__(self):
        require_sku(self.sku)
        require_positive(self.unit_cents, "unit price")
