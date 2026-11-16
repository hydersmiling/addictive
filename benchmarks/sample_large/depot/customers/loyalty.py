"""Loyalty tiers and points."""

from depot.core import config


def tier(points):
    """'gold', 'silver' or 'standard' for a points balance."""
    if points >= config.get("loyalty_gold_points"):
        return "gold"
    if points >= config.get("loyalty_silver_points"):
        return "silver"
    return "standard"


def points_for(total_cents):
    """One point per whole dollar spent."""
    return total_cents // 100
