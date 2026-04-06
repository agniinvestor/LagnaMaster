"""
src/calculations/panchadha_maitri.py — Session 50

5-fold Panchadha Maitri (BPHS Ch.15):
  Naisargika (permanent) + Tatkalik (temporal) → 5-category relationship

Tatkalik rule (CALC_TatkalikFriendship):
  Planet P2 in H2/3/4/10/11/12 from P1 → Tatkalik Friend
  Planet P2 in H1/5/6/7/8/9   from P1 → Tatkalik Enemy

Panchadha combination:
  Naisargika Friend  + Tatkalik Friend  = Adhi Mitra  (+1.0)
  Naisargika Friend  + Tatkalik Enemy   = Sama        ( 0.0)
  Naisargika Neutral + Tatkalik Friend  = Mitra       (+0.5)
  Naisargika Neutral + Tatkalik Enemy   = Shatru      (-0.5)
  Naisargika Enemy   + Tatkalik Friend  = Sama        ( 0.0)
  Naisargika Enemy   + Tatkalik Enemy   = Adhi Shatru (-1.0)

Scoring weights (CALC_PanchadhaMaitri §4):
  R06/R07: Adhi Mitra=+1.0, Mitra=+0.5, Sama=0, Shatru=−0.5, Adhi Shatru=−1.0
  R13/R14: Adhi Shatru=−1.0, Shatru=−0.5, Sama=0, Mitra=+0.5, Adhi Mitra=+1.0
"""

from __future__ import annotations
from dataclasses import dataclass

_NAT_FRIEND_DICT = {
    "Sun": {"Moon", "Mars", "Jupiter"},
    "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
    # BPHS Ch.3 notes (p.41, Santhanam Vol 1)
    "Rahu": {"Jupiter", "Venus", "Saturn"},
    "Ketu": {"Mars", "Venus", "Saturn"},
}
_NAT_ENEMY_DICT = {
    "Sun": {"Venus", "Saturn"},
    "Moon": set(),
    "Mars": {"Mercury"},
    "Mercury": {"Moon"},
    "Jupiter": {"Mercury", "Venus"},
    "Venus": {"Sun", "Moon"},
    "Saturn": {"Sun", "Moon", "Mars"},
    # BPHS Ch.3 notes (p.41, Santhanam Vol 1)
    "Rahu": {"Sun", "Moon", "Mars"},
    "Ketu": {"Sun", "Moon"},
}

_TATKALIK_FRIEND_HOUSES = {2, 3, 4, 10, 11, 12}  # from P1's house

_PANCHADHA_WEIGHTS = {
    "Adhi Mitra": +1.0,
    "Mitra": +0.5,
    "Sama": 0.0,
    "Shatru": -0.5,
    "Adhi Shatru": -1.0,
}


def naisargika_relation(p1: str, p2: str) -> str:
    """Return 'Friend', 'Neutral', or 'Enemy' (permanent Naisargika)."""
    if p2 in _NAT_FRIEND_DICT.get(p1, set()):
        return "Friend"
    if p2 in _NAT_ENEMY_DICT.get(p1, set()):
        return "Enemy"
    return "Neutral"


def tatkalik_relation(p1: str, p2: str, chart) -> str:
    """
    Tatkalik: if P2 is in H2/3/4/10/11/12 from P1's sign → Friend, else Enemy.
    Measured sign-to-sign (1-based house count from P1).
    """
    pos1 = chart.planets.get(p1)
    pos2 = chart.planets.get(p2)
    if not pos1 or not pos2:
        return "Neutral"
    # House of P2 counted from P1's sign (1 = same sign)
    diff = (pos2.sign_index - pos1.sign_index) % 12 + 1
    return "Friend" if diff in _TATKALIK_FRIEND_HOUSES else "Enemy"


def panchadha_relation(p1: str, p2: str, chart) -> str:
    """Return 5-fold Panchadha Maitri category."""
    nai = naisargika_relation(p1, p2)
    tat = tatkalik_relation(p1, p2, chart)
    if nai == "Friend" and tat == "Friend":
        return "Adhi Mitra"
    if nai == "Friend" and tat == "Enemy":
        return "Sama"
    if nai == "Neutral" and tat == "Friend":
        return "Mitra"
    if nai == "Neutral" and tat == "Enemy":
        return "Shatru"
    if nai == "Enemy" and tat == "Friend":
        return "Sama"
    if nai == "Enemy" and tat == "Enemy":
        return "Adhi Shatru"
    return "Sama"


def panchadha_score_weight(p1: str, p2: str, chart) -> float:
    """Numeric weight for scoring rules R06/R07/R13/R14."""
    return _PANCHADHA_WEIGHTS[panchadha_relation(p1, p2, chart)]


@dataclass
class PanchadhaMatrix:
    """Full 7×7 Panchadha Maitri matrix for a chart."""

    planets: list[str]
    relations: dict[tuple[str, str], str]
    weights: dict[tuple[str, str], float]

    def relation(self, p1: str, p2: str) -> str:
        return self.relations.get((p1, p2), "Sama")

    def weight(self, p1: str, p2: str) -> float:
        return self.weights.get((p1, p2), 0.0)


def compute_panchadha_matrix(chart) -> PanchadhaMatrix:
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]  # noqa: F841
    relations = {}
    weights = {}
    for p1 in planets:
        for p2 in planets:
            if p1 == p2:
                continue
            rel = panchadha_relation(p1, p2, chart)
            relations[(p1, p2)] = rel
            weights[(p1, p2)] = _PANCHADHA_WEIGHTS[rel]
    return PanchadhaMatrix(planets=planets, relations=relations, weights=weights)
