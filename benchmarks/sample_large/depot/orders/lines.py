"""Order line arithmetic."""


def calc_line_total(line):
    """Price of one order line in cents: unit price times quantity."""
    return line["item"].unit_cents * line["quantity"]


def heaviest_line(order):
    return max(order.lines, key=lambda l: l["item"].weight_grams * l["quantity"])
