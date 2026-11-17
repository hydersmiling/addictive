"""Expected arrival dates."""

from depot.core.dates import add_business_days


def expected_arrival(supplier, order_day):
    return add_business_days(order_day, supplier.lead_time_days)
