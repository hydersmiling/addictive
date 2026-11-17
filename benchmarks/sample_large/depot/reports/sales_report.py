"""Sales reports."""

from depot.orders.pricing import total


def revenue(orders):
    """Total revenue in cents across orders."""
    return sum(total(o) for o in orders)


def best_customer(orders):
    spend = {}
    for o in orders:
        spend[o.customer.name] = spend.get(o.customer.name, 0) + total(o)
    return max(spend, key=spend.get) if spend else None
