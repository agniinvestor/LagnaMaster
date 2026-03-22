"""
src/calculations/config_additions.py
Ayanamsha expansion (all 36 pyswisseph constants) + node mode toggle.
Session 124 (Phase 1).

Source: pyswisseph SE_SIDM_* constants; PVRNR recommends Lahiri/Chitrapaksha.
"""

from __future__ import annotations
from dataclasses import dataclass

# ─── Complete Ayanamsha map ──────────────────────────────────────────────────
# All 36 pyswisseph SE_SIDM_* constants
# Format: {name: (pyswisseph_constant, description, school)}

AYANAMSHA_MAP: dict[str, tuple[int, str, str]] = {
    # Primary — most commonly used
    "lahiri": (1, "Lahiri / Chitrapaksha — PVRNR, Govt of India standard", "parashari"),
    "raman": (3, "BV Raman — Bangalore tradition", "parashari"),
    "krishnamurti": (5, "KP / Krishnamurti — used in KP system", "kp"),
    "djwhal_khul": (6, "Djwhal Khul", "western"),
    "yukteshwar": (7, "Sri Yukteshwar — Autobiography of a Yogi", "parashari"),
    "jn_bhasin": (8, "JN Bhasin", "parashari"),
    "babyl_kugler1": (11, "Babylonian — Kugler 1", "historical"),
    "babyl_kugler2": (12, "Babylonian — Kugler 2", "historical"),
    "babyl_kugler3": (13, "Babylonian — Kugler 3", "historical"),
    "babyl_huber": (14, "Babylonian — Huber", "historical"),
    "babyl_etpsc": (15, "Babylonian — ET/PSC", "historical"),
    "aldebaran_15tau": (16, "Aldebaran at 15 Taurus", "historical"),
    "hipparchos": (17, "Hipparchos", "historical"),
    "sassanian": (18, "Sassanian", "historical"),
    "galcent_0sag": (19, "Galactic Centre at 0 Sagittarius", "galactic"),
    "j2000": (20, "J2000.0", "astronomical"),
    "j1900": (21, "J1900.0", "astronomical"),
    "b1950": (22, "B1950.0", "astronomical"),
    "suryasiddhanta": (23, "Suryasiddhanta", "classical"),
    "suryasiddhanta_mean": (24, "Suryasiddhanta (mean Sun)", "classical"),
    "aryabhata": (25, "Aryabhata", "classical"),
    "aryabhata_mean": (26, "Aryabhata (mean Sun)", "classical"),
    "ss_revati": (27, "SS Revati", "classical"),
    "ss_citra": (28, "SS Citra / True Chitrapaksha", "parashari"),
    "true_citra": (28, "True Citra — PVRNR preferred", "parashari"),  # alias
    "true_revati": (29, "True Revati", "classical"),
    "true_pushya": (30, "True Pushya — Sanjay Rath school", "jaimini"),
    "galcent_rgilbrand": (31, "Galactic Centre (R. Gilbrand)", "galactic"),
    "galequ_iau1958": (32, "Galactic Equator IAU 1958", "galactic"),
    "galequ_true": (33, "True Galactic Equator", "galactic"),
    "galequ_mula": (34, "Galactic Equator — Mula", "galactic"),
    "skydram": (35, "Skydram (Mardyks)", "western"),
    "true_mula": (36, "True Mula", "jaimini"),
    "dhruva_galcent": (36, "Dhruva Galactic Centre", "galactic"),  # alias
    "aryabhata_522": (40, "Aryabhata 522", "classical"),
    "babyl_britton": (41, "Babylonian — Britton", "historical"),
    "fagan_bradley": (0, "Fagan-Bradley — Western sidereal standard", "western"),
}

# Default for new charts — Lahiri is Govt of India standard, used by PVRNR
DEFAULT_AYANAMSHA = "lahiri"

# Ayanamshas where Lagna can differ by 1+ sign from Lahiri
# (warn user if switching between these)
LAGNA_SENSITIVE_AYANAMSHAS = {
    "fagan_bradley",
    "yukteshwar",
    "raman",
    "true_citra",
    "ss_revati",
    "true_revati",
    "galcent_0sag",
}


def ayanamsha_constant(name: str) -> int:
    """Return the pyswisseph SE_SIDM_* constant for a named ayanamsha."""
    entry = AYANAMSHA_MAP.get(name.lower())
    if entry is None:
        raise ValueError(
            f"Unknown ayanamsha: {name!r}. Valid names: {sorted(AYANAMSHA_MAP.keys())}"
        )
    return entry[0]


def is_lagna_sensitive(longitude: float, ayanamsha_name: str) -> bool:
    """
    Returns True if the Lagna is within 1° of a sign boundary,
    meaning ayanamsha choice could change the Lagna sign.
    Source: PLAN.md Session 124 note.
    """
    deg_in_sign = longitude % 30
    return deg_in_sign < 1.0 or deg_in_sign >= 29.0


# ─── Node mode ───────────────────────────────────────────────────────────────
# Source: PVRNR (BPHS) uses mean node (Parashari standard)
# KP and some modern practitioners use true node


class NodeMode:
    MEAN = "mean"  # Mean node — Parashari standard (default)
    TRUE = "true"  # True node — KP system, modern usage


DEFAULT_NODE_MODE = NodeMode.MEAN

# pyswisseph flags
NODE_MODE_FLAGS: dict[str, int] = {
    NodeMode.MEAN: 0,  # default — mean node
    NodeMode.TRUE: 2048,  # SEFLG_TRUEPOS equivalent for nodes
}

# Max longitude difference between mean and true node
NODE_MODE_MAX_DIFF_DEG = 1.5  # can reach 1.5° — enough to change sign at boundary


@dataclass
class AstronomicalConfig:
    """
    Astronomical foundation configuration.
    Stores ayanamsha + node mode for a calculation session.
    """

    ayanamsha: str = DEFAULT_AYANAMSHA
    node_mode: str = DEFAULT_NODE_MODE

    @property
    def ayanamsha_constant(self) -> int:
        return ayanamsha_constant(self.ayanamsha)

    @property
    def node_flag(self) -> int:
        return NODE_MODE_FLAGS.get(self.node_mode, 0)

    @property
    def description(self) -> str:
        entry = AYANAMSHA_MAP.get(self.ayanamsha.lower())
        desc = entry[1] if entry else self.ayanamsha
        return f"{desc} | Nodes: {self.node_mode}"


# Default singleton for backward compatibility
DEFAULT_CONFIG = AstronomicalConfig()
