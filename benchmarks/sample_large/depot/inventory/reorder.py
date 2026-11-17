"""Decide when to reorder stock."""

from depot.core import config


def reorder_point(daily_sales, lead_time_days):
    """Units on hand at which to reorder."""
    return daily_sales * (lead_time_days + config.get("reorder_buffer_days"))


def needs_reorder(stock, sku, daily_sales, lead_time_days):
    return stock.on_hand(sku) <= reorder_point(daily_sales, lead_time_days)
