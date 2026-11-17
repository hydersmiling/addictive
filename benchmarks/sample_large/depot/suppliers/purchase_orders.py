"""Purchase orders to suppliers."""

from depot.core.ids import next_id


def create_po(supplier, lines):
    """lines: list of (sku, quantity)."""
    return {"po_id": next_id("PO"), "supplier": supplier.supplier_id, "lines": list(lines)}


def po_units(po):
    return sum(q for _sku, q in po["lines"])
