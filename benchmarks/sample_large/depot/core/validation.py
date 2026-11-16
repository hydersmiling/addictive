"""Input validation helpers."""

import re

from depot.core.errors import ValidationError

SKU_PATTERN = re.compile(r"^[A-Z]{3}-\d{4}$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$")


def require_sku(sku):
    if not SKU_PATTERN.match(sku):
        raise ValidationError(f"bad SKU: {sku}")
    return sku


def require_positive(value, name):
    if value <= 0:
        raise ValidationError(f"{name} must be positive")
    return value


def require_email(email):
    if not EMAIL_PATTERN.match(email):
        raise ValidationError(f"bad email: {email}")
    return email
