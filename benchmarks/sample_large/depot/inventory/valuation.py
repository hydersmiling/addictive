"""Value of stock on hand."""


def stock_value(stock, items_by_sku):
    """Total value in cents of everything on hand."""
    return sum(items_by_sku[sku].unit_cents * qty for sku, qty in stock.levels.items())
