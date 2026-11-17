"""Order totals: subtotal, discounts, then tax."""

from depot.orders.discounts import apply_bulk_discount, apply_loyalty_discount
from depot.orders.lines import calc_line_total
from depot.orders.tax import with_tax


def subtotal(order):
    return sum(calc_line_total(line) for line in order.lines)


def total(order):
    """Final price in cents after loyalty and bulk discounts, including tax."""
    cents = apply_loyalty_discount(subtotal(order), order.customer)
    cents = apply_bulk_discount(cents, order.item_count())
    return with_tax(cents)
