"""Exception types raised by the package."""


class DepotError(Exception):
    """Base class for all depot errors."""


class OutOfStock(DepotError):
    pass


class NotFound(DepotError):
    pass


class ValidationError(DepotError):
    pass


class CreditLimitExceeded(DepotError):
    pass
