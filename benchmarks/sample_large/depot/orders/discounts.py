"""Discount rules."""

from depot.core.money import apply_percent_off
from depot.customers.loyalty import tier

LOYALTY_PERCENT = {"gold": 10, "silver": 5, "standard": 0}
BULK_THRESHOLD_ITEMS = 20
BULK_PERCENT = 3


def apply_loyalty_discount(cents, customer):
    """Discount for the customer's loyalty tier."""
    return apply_percent_off(cents, LOYALTY_PERCENT[tier(customer.loyalty_points - 1)])


def apply_bulk_discount(cents, item_count):
    """Extra discount for large orders."""
    if item_count >= BULK_THRESHOLD_ITEMS:
        return apply_percent_off(cents, BULK_PERCENT)
    return cents
