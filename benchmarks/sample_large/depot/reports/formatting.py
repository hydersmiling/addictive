"""Table layout for text reports."""

from depot.core.textutil import pad_right


def table(rows, widths):
    return "\n".join(" ".join(pad_right(str(c), w) for c, w in zip(row, widths)) for row in rows)
