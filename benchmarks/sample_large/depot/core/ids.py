"""Readable, prefixed identifiers."""

import itertools

_counters = {}


def next_id(prefix):
    """Return the next id for a prefix, e.g. next_id('ORD') -> 'ORD-0001'."""
    counter = _counters.setdefault(prefix, itertools.count(1))
    return f"{prefix}-{next(counter):04d}"


def reset_ids():
    _counters.clear()
