"""URL routing table."""

from depot.api import handlers

ROUTES = {("GET", "/orders/<id>"): handlers.get_order}


def resolve(method, pattern):
    return ROUTES.get((method, pattern))
