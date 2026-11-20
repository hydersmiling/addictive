# Splitting a Python module safely

## Turn a big module into a package (keeps every import working)
Before: `billing.py` (900 lines). After:
```
billing/
  __init__.py      # re-exports the public names
  invoices.py
  payments.py
  tax.py
```
`billing/__init__.py`:
```python
"""Billing: invoices, payments and tax. Public names are re-exported here."""
from .invoices import Invoice, make_invoice
from .payments import charge, refund
from .tax import tax_for

__all__ = ["Invoice", "make_invoice", "charge", "refund", "tax_for"]
```
Callers that wrote `from billing import charge` keep working unchanged.

## Or keep the old file as a thin shim
If the module must stay a single file name (for example it is run as a script), move the
code into new modules beside it and leave the old file importing from them:
```python
# report.py, kept so existing imports work
from report_layout import build_layout  # noqa: F401
from report_export import to_csv, to_pdf  # noqa: F401
```

## Watch out for
- **Circular imports:** if two new modules need each other, move the shared piece into a
  third module (often `common.py` or `types.py`) instead of importing in both directions.
- **Private helpers:** names starting with `_` move with the code that uses them; do not
  re-export them.
- **Monkeypatching in tests:** `mock.patch("billing.charge")` still patches the re-export,
  not the function the code now calls. Point patches at the new module (`billing.payments.charge`).
- **Module-level state** (caches, registries, settings): keep it in exactly one module and
  import it from there, or the split creates two copies.
- **`python -m` entry points and `if __name__ == "__main__":`** blocks stay in the file that
  is executed.
