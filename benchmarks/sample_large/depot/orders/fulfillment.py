"""Picking and shipping orders."""

from depot.core.dates import add_business_days


def pick(order, stock):
    """Take every line from stock and mark the order picked."""
    for line in order.lines:
        stock.take(line["item"].sku, line["quantity"])
    order.status = "picked"


def ship_date(order_day, express=False):
    return add_business_days(order_day, 1 if express else 3)
