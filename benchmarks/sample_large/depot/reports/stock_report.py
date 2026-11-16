"""Stock on hand report."""

from depot.reports.formatting import table


def stock_report(stock):
    rows = [(sku, qty) for sku, qty in sorted(stock.levels.items())]
    return table([("SKU", "QTY")] + rows, (10, 6))
