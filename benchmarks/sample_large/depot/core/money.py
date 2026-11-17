"""Money helpers. All amounts are whole cents (int)."""


def format_cents(cents):
    """Format cents as dollars: 1999 -> '$19.99', -50 -> '-$0.50'."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"


def parse_cents(text):
    """Parse '$19.99' or '19.99' into cents."""
    text = text.strip().replace("$", "")
    dollars, _, frac = text.partition(".")
    return int(dollars or 0) * 100 + int((frac + "00")[:2])


def apply_percent_off(cents, percent):
    """Reduce an amount by a whole-number percentage, rounding down to a cent."""
    return cents - (cents * percent) // 100


def split_evenly(cents, parts):
    """Split an amount into `parts` near-equal integers that sum to the total."""
    base, extra = divmod(cents, parts)
    return [base + (1 if i < extra else 0) for i in range(parts)]
