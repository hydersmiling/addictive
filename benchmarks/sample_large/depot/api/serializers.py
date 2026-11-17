"""Turn domain objects into plain dicts."""


def order_to_dict(order):
    return {"id": order.order_id, "status": order.status,
            "lines": [{"sku": l["item"].sku, "quantity": l["quantity"]} for l in order.lines]}


def customer_to_dict(customer):
    return {"id": customer.customer_id, "name": customer.name}
