"""Canonical derived house resolver. ALL bhavat-bhavam arithmetic goes here."""
from __future__ import annotations


def resolve_house(base: int, offset: int) -> int:
    """BPHS inclusive counting: '5th from 3rd' means count 3->4->5->6->7 = house 7.

    Args:
        base: starting house (1-12)
        offset: houses to count forward, inclusive (1-12)

    Returns:
        absolute house number (1-12)
    """
    return (base + offset - 2) % 12 + 1
