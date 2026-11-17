"""Date helpers for business days and periods."""

from datetime import date, timedelta


def add_business_days(start, days):
    """Return the date `days` business days after `start` (Mon-Fri)."""
    current = start
    while days > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:
            days -= 1
    return current


def month_bounds(day):
    """First and last day of the month containing `day`."""
    first = day.replace(day=1)
    next_month = (first + timedelta(days=32)).replace(day=1)
    return first, next_month - timedelta(days=1)


def is_weekend(day):
    return day.weekday() >= 5


def today():
    return date.today()
