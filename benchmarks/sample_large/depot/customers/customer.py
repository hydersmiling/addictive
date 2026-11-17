"""Customer records."""

from dataclasses import dataclass, field

from depot.core.validation import require_email


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    loyalty_points: int = 0
    addresses: list = field(default_factory=list)

    def __post_init__(self):
        require_email(self.email)
