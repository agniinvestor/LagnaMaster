"""
src/calculations/friendship.py
================================
Natural (Naisargika) + Temporary (Tatkalik) + Five-fold (Panchadha) Maitri.
Source: REF_NaisargikaFriendship + CALC_TatkalikFriendship (Excel), BPHS Ch.15.
"""

from __future__ import annotations
from dataclasses import dataclass
from src.ephemeris import BirthChart


# ---------------------------------------------------------------------------
# Naisargika (Permanent) Friendship Matrix
# REF_NaisargikaFriendship rows 5-11 — row planet views column planet
# ---------------------------------------------------------------------------

_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# F=Friend, N=Neutral, E=Enemy
_NAISARGIKA_RAW: list[list[str]] = [
    # Sun   Moon  Mars  Merc  Jup   Ven   Sat    ← col (viewed)
    ["—",  "F",  "F",  "N",  "F",  "E",  "E"],   # Sun   ← row (viewer)
    ["F",  "—",  "N",  "F",  "N",  "N",  "N"],   # Moon
    ["F",  "F",  "—",  "E",  "F",  "N",  "N"],   # Mars
    ["F",  "E",  "N",  "—",  "N",  "F",  "N"],   # Mercury
    ["F",  "F",  "F",  "E",  "—",  "E",  "N"],   # Jupiter
    ["E",  "E",  "N",  "F",  "N",  "—",  "F"],   # Venus
    ["E",  "E",  "E",  "F",  "N",  "F",  "—"],   # Saturn
]

def _naisargika(viewer: str, viewed: str) -> str:
    """Return 'F', 'N', or 'E'. Rahu/Ketu always 'N' (no classical entry)."""
    if viewer == viewed:
        return "—"
    if viewer in ("Rahu", "Ketu") or viewed in ("Rahu", "Ketu"):
        return "N"
    i = _PLANETS.index(viewer)
    j = _PLANETS.index(viewed)
    return _NAISARGIKA_RAW[i][j]


# ---------------------------------------------------------------------------
# Tatkalik (Temporary) Friendship
# Rule: houses 2/3/4/10/11/12 from P1 = Friend; 1/5/6/7/8/9 = Enemy
# Symmetric by design.
# ---------------------------------------------------------------------------

_TATKALIK_FRIEND_HOUSES = {2, 3, 4, 10, 11, 12}

def _tatkalik(p1_sign_idx: int, p2_sign_idx: int) -> str:
    """Return 'F' or 'E'. Tatkalik is symmetric."""
    house = (p2_sign_idx - p1_sign_idx) % 12 + 1   # 1-12
    return "F" if house in _TATKALIK_FRIEND_HOUSES else "E"


# ---------------------------------------------------------------------------
# Panchadha Maitri (5-fold result)
# Naisargika × Tatkalik → Adhi Mitra / Mitra / Sama / Shatru / Adhi Shatru
# REF_NaisargikaFriendship rows 18-21
# ---------------------------------------------------------------------------

_PANCHADHA_TABLE = {
    ("F", "F"): "Adhi Mitra",
    ("F", "N"): "Mitra",       # Tatkalik N is impossible in practice
    ("F", "E"): "Sama",
    ("N", "F"): "Mitra",
    ("N", "N"): "Sama",
    ("N", "E"): "Shatru",
    ("E", "F"): "Sama",
    ("E", "N"): "Shatru",
    ("E", "E"): "Adhi Shatru",
}

# Scoring weights (REF_NaisargikaFriendship rows 27-30)
PANCHADHA_WEIGHT = {
    "Adhi Mitra":   +1.0,
    "Mitra":        +0.5,
    "Sama":          0.0,
    "Shatru":       -0.5,
    "Adhi Shatru":  -1.0,
}


@dataclass
class FriendshipResult:
    viewer: str
    viewed: str
    naisargika: str     # F / N / E
    tatkalik: str       # F / E
    panchadha: str      # Adhi Mitra … Adhi Shatru
    weight: float       # score modifier


def compute_friendship(
    viewer: str, viewer_sign_idx: int,
    viewed: str, viewed_sign_idx: int,
) -> FriendshipResult:
    """Compute 5-fold Panchadha Maitri between two planets."""
    nai = _naisargika(viewer, viewed)
    tat = _tatkalik(viewer_sign_idx, viewed_sign_idx)
    # Nodes have no tatkalik (they don't occupy independent signs in BPHS model)
    if viewer in ("Rahu", "Ketu") or viewed in ("Rahu", "Ketu"):
        tat = "N"
    key = (nai if nai in ("F", "N", "E") else "N", tat if tat in ("F", "N", "E") else "N")
    pancha = _PANCHADHA_TABLE.get(key, "Sama")
    return FriendshipResult(
        viewer=viewer,
        viewed=viewed,
        naisargika=nai,
        tatkalik=tat,
        panchadha=pancha,
        weight=PANCHADHA_WEIGHT[pancha],
    )


def compute_all_friendships(chart: BirthChart) -> dict[tuple[str, str], FriendshipResult]:
    """
    Compute all pairwise Panchadha relationships for a chart.
    Returns dict keyed by (viewer, viewed).
    """
    planets = list(chart.planets.keys())
    results = {}
    for p1 in planets:
        for p2 in planets:
            if p1 != p2:
                results[(p1, p2)] = compute_friendship(
                    p1, chart.planets[p1].sign_index,
                    p2, chart.planets[p2].sign_index,
                )
    return results
