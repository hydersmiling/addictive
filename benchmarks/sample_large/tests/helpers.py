"""Shared test fixtures."""

from depot.customers.customer import Customer
from depot.inventory.item import Item
from depot.orders.order import Order


def make_item(sku="ABC-0001", cents=1000, weight=100, name="Widget"):
    return Item(sku, name, cents, weight)


def make_order(points=0, quantity=1, cents=1000):
    customer = Customer("C1", "Ada", "ada@example.com", loyalty_points=points)
    order = Order(customer)
    order.add(make_item(cents=cents), quantity)
    return order
