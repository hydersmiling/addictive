"""Customer returns and refunds."""

from depot.orders.lines import calc_line_total


def refund_for(line, restocking_percent=10):
    """Refund in cents for a returned line, minus a restocking fee."""
    gross = calc_line_total(line)
    return gross - gross * restocking_percent // 100


def restock(stock, line):
    stock.receive(line["item"].sku, line["quantity"])
