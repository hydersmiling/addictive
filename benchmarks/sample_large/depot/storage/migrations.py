"""Schema migrations for stored records."""

MIGRATIONS = []


def migration(func):
    MIGRATIONS.append(func)
    return func


@migration
def add_status_field(record):
    record.setdefault("status", "open")
    return record


def migrate(record):
    for step in MIGRATIONS:
        record = step(record)
    return record
