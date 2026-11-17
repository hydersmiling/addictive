"""Small text helpers for labels and reports."""


def pad_right(text, width):
    return text[:width].ljust(width)


def plural(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


def slug(text):
    return "-".join(text.lower().split())
