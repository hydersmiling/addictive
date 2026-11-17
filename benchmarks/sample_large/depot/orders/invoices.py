"""Invoice text."""

from depot.core.money import format_cents
from depot.orders.lines import calc_line_total
from depot.orders.pricing import total


def invoice_lines(order):
    return [f"{l['item'].name} x{l['quantity']}: {format_cents(calc_line_total(l))}" for l in order.lines]


def invoice_text(order):
    body = "\n".join(invoice_lines(order))
    return f"Invoice {order.order_id}\n{body}\nTotal: {format_cents(total(order))}"
