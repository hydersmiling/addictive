"""Sales tax."""

from depot.core import config


def tax_for(cents):
    """Tax in cents, rounded down."""
    return cents * config.get("tax_rate_percent") // 100


def with_tax(cents):
    return cents + tax_for(cents)
