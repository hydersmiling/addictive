"""Package settings with safe defaults."""

DEFAULTS = {
    "tax_rate_percent": 8,
    "reorder_buffer_days": 3,
    "loyalty_gold_points": 1000,
    "loyalty_silver_points": 500,
    "max_credit_cents": 500_00,
}


def get(key):
    return DEFAULTS[key]
