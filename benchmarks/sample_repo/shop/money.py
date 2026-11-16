"""Money helpers. Prices are whole cents (int) to avoid rounding errors."""


def format_cents(cents):
    """Format cents as dollars, e.g. 150 -> '$1.50'."""
    return f"${cents // 100}.{cents % 100:02d}"


def apply_percent_off(cents, percent):
    """Reduce a price by a whole-number percentage, rounding down to a cent."""
    return cents - (cents * percent) // 100
