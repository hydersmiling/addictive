"""Message templates."""

TEMPLATES = {
    "shipped": "Hi {name}, order {order_id} has shipped.",
    "delayed": "Hi {name}, order {order_id} is delayed.",
}


def render(kind, **fields):
    return TEMPLATES[kind].format(**fields)
