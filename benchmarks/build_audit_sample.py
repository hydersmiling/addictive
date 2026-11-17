"""Build the 'audit' benchmark sample: the large sample plus 150 legacy modules.

The legacy modules make broad searches expensive, which is where delegating
reading to a cheaper subagent should pay off. A few modules hide problems the
audit tasks must find; similar-looking "decoy" modules are correct and must
not be reported. Generation is seeded, so every build is identical.

Usage: python benchmarks/build_audit_sample.py OUTPUT_FOLDER
"""

import os
import random
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "sample_large")
MODULES = 150

# Planted problems (module number -> code). The tasks must find exactly these.
MONEY_BUGS = {   # formats dollars by hand instead of using format_cents
    17: 'def price_label(cents):\n    return f"${cents / 100:.2f}"\n',
    48: 'def fee_text(cents):\n    return "$%d.%02d" % divmod(cents, 100)\n',
    93: 'def refund_text(cents):\n    return "$" + str(cents // 100) + "." + str(cents % 100).zfill(2)\n',
    131: 'def credit_line(cents):\n    dollars = round(cents / 100, 2)\n    return "credit: $" + str(dollars)\n',
}
SQL_BUGS = {     # builds SQL from values with string formatting (injection risk)
    29: 'def find_customer(cur, customer_id):\n    cur.execute(f"SELECT * FROM customers WHERE id = {customer_id}")\n    return cur.fetchone()\n',
    76: 'def delete_note(cur, title):\n    cur.execute("DELETE FROM notes WHERE title = \'%s\'" % title)\n',
    118: 'def rename_sku(cur, sku, name):\n    cur.execute("UPDATE items SET name = \'" + name + "\' WHERE sku = \'" + sku + "\'")\n',
}
DECOYS = {       # look similar but are correct
    35: 'from depot.core.money import format_cents\n\n\ndef price_label(cents):\n    return format_cents(cents)\n',
    61: 'def find_customer(cur, customer_id):\n    cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))\n    return cur.fetchone()\n',
    104: 'def percent_text(ratio):\n    return f"{ratio * 100:.2f}%"\n',
    142: 'def delete_note(cur, title):\n    cur.execute("DELETE FROM notes WHERE title = ?", (title,))\n',
}

NOUNS = ["pallet", "shipment", "bin", "carrier", "manifest", "route", "zone", "dock", "crate", "label",
         "invoice", "ledger", "quota", "forecast", "batch", "tote", "rack", "lane", "slot", "audit"]
VERBS = ["load", "count", "merge", "split", "score", "rank", "check", "group", "trim", "sort"]


def filler_function(rng, n):
    """A small, plausible helper function with a docstring and some logic."""
    noun, verb = rng.choice(NOUNS), rng.choice(VERBS)
    other = rng.choice(NOUNS)
    limit = rng.randint(3, 40)
    return (
        f"def {verb}_{noun}s_{n}(records, limit={limit}):\n"
        f'    """{verb.capitalize()} {noun} records and keep at most `limit` per {other}."""\n'
        f"    groups = {{}}\n"
        f"    for record in records:\n"
        f"        key = record.get('{other}', 'none')\n"
        f"        groups.setdefault(key, []).append(record)\n"
        f"    result = []\n"
        f"    for key in sorted(groups):\n"
        f"        items = sorted(groups[key], key=lambda r: r.get('weight', 0), reverse=True)\n"
        f"        result.extend(items[:limit])\n"
        f"    return result\n"
    )


def module_text(rng, number):
    noun = rng.choice(NOUNS)
    parts = [f'"""Legacy {noun} utilities (module {number:03d}), kept for old integrations."""\n']
    funcs = [filler_function(rng, i) for i in range(rng.randint(4, 7))]
    special = MONEY_BUGS.get(number) or SQL_BUGS.get(number) or DECOYS.get(number)
    if special:
        funcs.insert(rng.randint(1, len(funcs)), special)
    parts.extend(funcs)
    return "\n\n".join(parts)


def build(dest):
    """Copy the large sample into dest and add the legacy package."""
    shutil.copytree(BASE, dest)
    rng = random.Random(20261117)
    legacy = os.path.join(dest, "depot", "legacy")
    os.makedirs(legacy)
    with open(os.path.join(legacy, "__init__.py"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write('"""Old modules kept for backward compatibility."""\n')
    for number in range(1, MODULES + 1):
        with open(os.path.join(legacy, f"mod_{number:03d}.py"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(module_text(rng, number))


if __name__ == "__main__":
    build(sys.argv[1])
    print(f"Built audit sample in {sys.argv[1]}")
