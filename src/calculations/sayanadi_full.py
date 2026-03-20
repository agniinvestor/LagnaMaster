"""
src/calculations/sayanadi_full.py — Session 49

Complete 12-state Sayanadi Avastha system (BPHS Ch.45–47).
Replaces the 7-state approximation in avastha_v2.py.

State priority (highest wins):
  Kopa     — combust (Sun's orb)
  Deena    — defeated in Graha Yuddha
  Sthira   — own/exaltation sign
  Mudita   — friendly sign + benefic aspect
  Kshuditha— enemy sign
  Trashita — watery sign + malefic aspect
  Sayana   — odd sign, 0°–10° (decanate 1)
  Upavesh  — odd sign, 10°–20° (decanate 2)
  Netrapani— odd sign, 20°–30° (decanate 3)
  Kautuka  — even sign, 0°–10° (decanate 1)
  Nishcheshta — even sign, 10°–20° (decanate 2)
  Prakrita — all other

Modifiers (from REF_AvasthaRules §3):
  Mudita / Sthira           ×1.25
  Deena / Kopa              ×0.50
  Kshuditha                 ×0.75
  Trashita                  ×0.75
  Sayana / Nishcheshta      ×0.60  (strongly weakening)
  Upavesh                   ×0.75
  Netrapani / Kautuka       ×0.85  (mildly weakening)
  Prakrita                  ×1.00
"""
from __future__ import annotations
from dataclasses import dataclass

_NAT_FRIEND = {
    "Sun":   {"Moon","Mars","Jupiter"},
    "Moon":  {"Sun","Mercury"},
    "Mars":  {"Sun","Moon","Jupiter"},
    "Mercury":{"Sun","Venus"},
    "Jupiter":{"Sun","Moon","Mars"},
    "Venus": {"Mercury","Saturn"},
    "Saturn":{"Mercury","Venus"},
}
_NAT_ENEMY = {
    "Sun":   {"Venus","Saturn"},
    "Moon":  set(),
    "Mars":  {"Mercury"},
    "Mercury":{"Moon"},
    "Jupiter":{"Mercury","Venus"},
    "Venus": {"Sun","Moon"},
    "Saturn":{"Sun","Moon","Mars"},
}
_EXALT_SI  = {"Sun":0,"Moon":1,"Mars":9,"Mercury":5,"Jupiter":3,"Venus":11,"Saturn":6}
_OWN       = {"Sun":{4},"Moon":{3},"Mars":{0,7},"Mercury":{2,5},
              "Jupiter":{8,11},"Venus":{1,6},"Saturn":{9,10}}
_WATERY_SI = {3, 7, 11}   # Cancer, Scorpio, Pisces
_NAT_BENEF = {"Jupiter","Venus","Mercury","Moon"}
_NAT_MALEF = {"Sun","Mars","Saturn","Rahu","Ketu"}

# BPHS combust orbs (degrees from Sun)
_COMBUST_ORB = {"Moon":12,"Mars":17,"Mercury":14,"Jupiter":11,"Venus":10,"Saturn":15}

_MODIFIERS = {
    "Sthira":     1.25,
    "Mudita":     1.25,
    "Prakrita":   1.00,
    "Netrapani":  0.85,
    "Kautuka":    0.85,
    "Upavesh":    0.75,
    "Kshuditha":  0.75,
    "Trashita":   0.75,
    "Nishcheshta":0.60,
    "Sayana":     0.60,
    "Deena":      0.50,
    "Kopa":       0.50,
}


@dataclass
class SayanadiResult:
    planet: str
    state: str
    modifier: float
    reason: str


def compute_sayanadi_full(planet: str, chart,
                          yuddha_losers: set[str] | None = None) -> SayanadiResult:
    """
    Compute the full 12-state Sayanadi for a planet.
    yuddha_losers: set of planet names that lost a Graha Yuddha.
    """
    pos = chart.planets.get(planet)
    if not pos:
        return SayanadiResult(planet, "Prakrita", 1.0, "Not in chart")

    si  = pos.sign_index      # 0-based sign index
    deg = pos.degree_in_sign  # 0.0–30.0
    lon = pos.longitude

    # ── Priority 1: Kopa (combust) ────────────────────────────────────────────
    if planet not in ("Sun", "Moon", "Rahu", "Ketu"):
        sun_lon = chart.planets["Sun"].longitude
        orb = abs(lon - sun_lon) % 360
        if orb > 180:
            orb = 360 - orb
        if orb <= _COMBUST_ORB.get(planet, 15):
            return SayanadiResult(planet, "Kopa", 0.50,
                                  f"Combust — {orb:.1f}° from Sun (orb {_COMBUST_ORB.get(planet,15)}°)")

    # ── Priority 2: Deena (defeated in Graha Yuddha) ─────────────────────────
    if yuddha_losers and planet in yuddha_losers:
        return SayanadiResult(planet, "Deena", 0.50,
                              "Defeated in Graha Yuddha")

    # ── Priority 3: Sthira (own/exaltation sign) ──────────────────────────────
    if si in _OWN.get(planet, set()) or _EXALT_SI.get(planet) == si:
        return SayanadiResult(planet, "Sthira", 1.25,
                              "In own or exaltation sign")

    # ── Priority 4: Mudita (friendly sign + benefic aspect) ──────────────────
    lord_name = _sign_lord(si)
    is_friendly = lord_name in _NAT_FRIEND.get(planet, set())
    if is_friendly and _has_benefic_aspect(planet, si, chart):
        return SayanadiResult(planet, "Mudita", 1.25,
                              f"Friendly sign ({lord_name}) + benefic aspect")

    # ── Priority 5: Kshuditha (enemy sign) ────────────────────────────────────
    is_enemy = lord_name in _NAT_ENEMY.get(planet, set())
    if is_enemy:
        return SayanadiResult(planet, "Kshuditha", 0.75,
                              f"Enemy sign (lord {lord_name})")

    # ── Priority 6: Trashita (watery sign + malefic aspect) ──────────────────
    if si in _WATERY_SI and _has_malefic_aspect(planet, si, chart):
        return SayanadiResult(planet, "Trashita", 0.75,
                              "Watery sign + malefic 7th aspect")

    # ── Priority 7–11: Decanate-based states ─────────────────────────────────
    is_odd = (si % 2 == 0)   # sign_index 0=Aries (odd), 1=Taurus (even) ...
    decan = int(deg / 10)    # 0,1,2

    if is_odd:
        if decan == 0:
            return SayanadiResult(planet, "Sayana", 0.60,
                                  "Odd sign, 1st decanate (0°–10°) — sleeping")
        elif decan == 1:
            return SayanadiResult(planet, "Upavesh", 0.75,
                                  "Odd sign, 2nd decanate (10°–20°) — stirring")
        else:
            return SayanadiResult(planet, "Netrapani", 0.85,
                                  "Odd sign, 3rd decanate (20°–30°) — introspective")
    else:
        if decan == 0:
            return SayanadiResult(planet, "Kautuka", 0.85,
                                  "Even sign, 1st decanate (0°–10°) — playful")
        elif decan == 1:
            return SayanadiResult(planet, "Nishcheshta", 0.60,
                                  "Even sign, 2nd decanate (10°–20°) — powerless")

    return SayanadiResult(planet, "Prakrita", 1.00, "Normal state")


def compute_all_sayanadi(chart, yuddha_losers: set[str] | None = None
                         ) -> dict[str, SayanadiResult]:
    planets_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
    if yuddha_losers is None:
        try:
            from src.calculations.graha_yuddha import compute_graha_yuddha
            wars = compute_graha_yuddha(chart)
            yuddha_losers = {w.loser for w in wars}
        except Exception:
            yuddha_losers = set()
    return {p: compute_sayanadi_full(p, chart, yuddha_losers) for p in planets_7}


# ── Helpers ───────────────────────────────────────────────────────────────────
_SIGN_LORDS = {0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
               6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter"}

def _sign_lord(si: int) -> str:
    return _SIGN_LORDS[si % 12]

def _has_benefic_aspect(planet: str, si: int, chart) -> bool:
    """Check if any natural benefic casts 7th aspect on planet's sign."""
    for p2, pos2 in chart.planets.items():
        if p2 == planet or p2 not in _NAT_BENEF:
            continue
        if (pos2.sign_index + 6) % 12 == si:
            return True
    return False

def _has_malefic_aspect(planet: str, si: int, chart) -> bool:
    """Check if any natural malefic casts 7th aspect on planet's sign."""
    for p2, pos2 in chart.planets.items():
        if p2 == planet or p2 not in _NAT_MALEF:
            continue
        if (pos2.sign_index + 6) % 12 == si:
            return True
    return False
