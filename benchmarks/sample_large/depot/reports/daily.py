"""End-of-day summary."""

from depot.core.money import format_cents
from depot.core.textutil import plural
from depot.reports.sales_report import revenue


def daily_summary(orders):
    return f"{plural(len(orders), 'order')}, revenue {format_cents(revenue(orders))}"
