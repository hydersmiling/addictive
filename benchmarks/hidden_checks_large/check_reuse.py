"""Hidden check: order_summary must reuse existing helpers, not re-implement them."""

import pathlib
import re
import sys

text = pathlib.Path("depot/reports/sales_report.py").read_text(encoding="utf-8")
if re.search(r"/\s*100|%\s*100|:\.2f|divmod\(", text):
    sys.exit("sales_report.py re-implements money formatting instead of using format_cents")
if "format_cents" not in text:
    sys.exit("sales_report.py does not use depot.core.money.format_cents")
