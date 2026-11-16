"""Request handlers."""

from depot.api.serializers import order_to_dict
from depot.core.errors import NotFound


def get_order(store, order_id):
    order = store.get(f"order:{order_id}")
    if order is None:
        raise NotFound(order_id)
    return order_to_dict(order)
