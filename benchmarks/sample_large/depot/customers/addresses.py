"""Postal addresses."""


def format_address(address):
    """One-line address from a dict with street, city and postcode."""
    return f"{address['street']}, {address['city']} {address['postcode']}"


def primary_address(customer):
    return customer.addresses[0] if customer.addresses else None
