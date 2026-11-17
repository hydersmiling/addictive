"""Supplier records."""

from dataclasses import dataclass


@dataclass
class Supplier:
    supplier_id: str
    name: str
    lead_time_days: int
