"""Customer credit limits."""

from depot.core import config
from depot.core.errors import CreditLimitExceeded


def check_credit(balance_cents, order_cents):
    if balance_cents + order_cents > config.get("max_credit_cents"):
        raise CreditLimitExceeded("order would exceed the credit limit")
    return True
