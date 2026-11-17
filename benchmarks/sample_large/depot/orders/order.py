"""Orders and their lines."""

from dataclasses import dataclass, field

from depot.core.ids import next_id


@dataclass
class Order:
    customer: object
    lines: list = field(default_factory=list)
    order_id: str = ""
    status: str = "open"

    def __post_init__(self):
        if not self.order_id:
            self.order_id = next_id("ORD")

    def add(self, item, quantity):
        self.lines.append({"item": item, "quantity": quantity})

    def item_count(self):
        return sum(line["quantity"] for line in self.lines)
