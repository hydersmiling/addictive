"""Moving stock between warehouses."""


def transfer(source, target, sku, quantity):
    """Move quantity of a SKU from one Stock to another."""
    source.take(sku, quantity)
    target.receive(sku, quantity)
    return {"sku": sku, "quantity": quantity}
