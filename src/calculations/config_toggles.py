"""
src/calculations/config_toggles.py — Session 55

REF_Config §1 toggle implementation.
All calculation options from the workbook's configuration sheet.

Ayanamshas supported (CALC_PlanetLongitudes):
  lahiri       — standard Vedic/BPHS (SE_SIDM_LAHIRI = 1)
  raman        — B.V. Raman (SE_SIDM_RAMAN = 3)
  krishnamurti — KP system (SE_SIDM_KRISHNAMURTI = 5)
  fagan_bradley— Western sidereal (SE_SIDM_FAGAN_BRADLEY = 0)

Node types:
  mean  — mean node (default, smooth)
  true  — true node (oscillates)

Retrograde policies (R22 rule):
  apply    — ±0.1 modifier (current default)
  ignore   — no retrograde effect on scoring
  classical— full strength regardless of retrograde (traditional view)
"""
from __future__ import annotations

_AYANAMSHA_MAP = {
    "lahiri":        1,   # SE_SIDM_LAHIRI
    "raman":         3,   # SE_SIDM_RAMAN
    "krishnamurti":  5,   # SE_SIDM_KRISHNAMURTI
    "fagan_bradley": 0,   # SE_SIDM_FAGAN_BRADLEY
    "true_citra":    27,  # SE_SIDM_TRUE_CITRA (also used by some)
}

_RETROGRADE_POLICIES = {"apply", "ignore", "classical"}
_NODE_TYPES = {"mean", "true"}


def resolve_ayanamsha(name: str) -> int:
    """Return pyswisseph ayanamsha constant for a name string."""
    key = name.lower().replace("-","_").replace(" ","_")
    if key not in _AYANAMSHA_MAP:
        raise ValueError(f"Unknown ayanamsha '{name}'. "
                         f"Valid: {sorted(_AYANAMSHA_MAP)}")
    return _AYANAMSHA_MAP[key]


def r22_modifier(planet: str, is_retrograde: bool, policy: str = "apply") -> float:
    """
    R22 retrograde scoring modifier.
    policy: 'apply' → ±0.10 | 'ignore' → 0.0 | 'classical' → 0.0 (full strength)
    """
    if policy == "apply" and is_retrograde:
        # Outer planets (Mars,Jup,Sat,Rahu,Ketu): slightly positive retrograde
        # Inner planets (Mer,Ven): slightly negative
        _OUTER = {"Mars","Jupiter","Saturn","Rahu","Ketu"}
        return +0.10 if planet in _OUTER else -0.10
    return 0.0


def use_true_node(node_type: str = "mean") -> bool:
    """Return True if true node should be used (vs mean node)."""
    return node_type.lower() == "true"


class CalcConfig:
    """Live configuration object mirroring REF_Config toggles."""
    def __init__(
        self,
        school: str = "parashari",
        ayanamsha: str = "lahiri",
        retrograde_policy: str = "apply",
        yogakaraka_weight: float = 1.5,
        wc_aspect_weight: float = 0.75,
        dukshthan_penalty: float = -2.0,
        kartari_source: str = "saravali",
        combust_orbs: str = "standard",
        node_type: str = "mean",
    ):
        self.school            = school
        self.ayanamsha         = ayanamsha
        self.retrograde_policy = retrograde_policy
        self.yogakaraka_weight = yogakaraka_weight
        self.wc_aspect_weight  = wc_aspect_weight
        self.dukshthan_penalty = dukshthan_penalty
        self.kartari_source    = kartari_source
        self.combust_orbs      = combust_orbs
        self.node_type         = node_type

    @property
    def ayanamsha_id(self) -> int:
        return resolve_ayanamsha(self.ayanamsha)

    @property
    def use_true_node(self) -> bool:
        return self.node_type == "true"

    def to_dict(self) -> dict:
        return {k: v for k, v in vars(self).items()}

    @classmethod
    def from_dict(cls, d: dict) -> "CalcConfig":
        return cls(**{k: v for k, v in d.items() if k in cls.__init__.__code__.co_varnames})


# Default config singleton (Parashari, Lahiri, apply R22)
DEFAULT_CONFIG = CalcConfig()
