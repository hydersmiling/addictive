"""Batch and expiry tracking."""


def expiring_before(batches, day):
    """Batches (dicts with 'expires') that expire before `day`."""
    return [b for b in batches if b["expires"] < day]


def oldest_first(batches):
    return sorted(batches, key=lambda b: b["expires"])
