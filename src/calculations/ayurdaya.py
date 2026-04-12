"""
src/calculations/ayurdaya.py
Ayurdaya (longevity) — composite result combining three BPHS Ch.44 methods.

Delegates to longevity.py for the individual calculations (Pindayu, Nisargayu,
Amsayu). This module provides the unified AyurdayaResult dataclass and the
compute_ayurdaya() composite function.

Source: BPHS Ch.44; PVRNR commentaries
"""

from __future__ import annotations
from dataclasses import dataclass

from src.calculations.longevity import (
    compute_pindayu,
    compute_nisargayu,
    compute_amsayu,
)


@dataclass
class AyurdayaResult:
    pindayu: float  # years from planetary arc method
    amsayu: float  # years from navamsha positions
    nisargayu: float  # natural/fixed longevity
    combined: float  # (pindayu + amsayu + nisargayu) / 3
    category: str  # "Short" (<32) / "Middle" (32-64) / "Long" (>64)


def compute_ayurdaya(chart) -> AyurdayaResult:
    """
    Full Ayurdaya calculation combining all three methods.
    Source: BPHS Ch.44
    """
    pindayu = compute_pindayu(chart)
    amsayu = compute_amsayu(chart)
    nisargayu = compute_nisargayu(chart)
    combined = round((pindayu + amsayu + nisargayu) / 3.0, 2)

    if combined < 32:
        category = "Short"
    elif combined < 64:
        category = "Middle"
    else:
        category = "Long"

    return AyurdayaResult(
        pindayu=pindayu,
        amsayu=amsayu,
        nisargayu=nisargayu,
        combined=combined,
        category=category,
    )
