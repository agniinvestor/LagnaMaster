"""
src/calculations/calc_config.py
School-Declaration Architecture — CalcConfig.school gates which modules activate.
Session 156 (Audit OB-4, I-B).

Every classical rule belongs to a school. Mixing schools without declaration
produces results neither school would endorse.

Sources:
  Sanjay Rath · Crux of Vedic Astrology, Preface
  PVRNR · BPHS (Parashari school)
  Jaimini Sutras (Jaimini school)
  K.S. Krishnamurti · Reader Series (KP school)
  Neelakantha · Tajika Nilakanthi (Tajika school)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class School(str, Enum):
    """Jyotish calculation school declaration."""
    PARASHARI = "parashari"   # PVRNR BPHS — default
    JAIMINI   = "jaimini"     # Jaimini Sutras
    KP        = "kp"          # Krishnamurti Paddhati
    TAJIKA    = "tajika"       # Varshaphala / annual charts
    NADI      = "nadi"        # Nadi Jyotish (future)


class Authority(str, Enum):
    """Within Parashari, which authority resolves conflicts."""
    PVRNR    = "pvrnr"       # P.V.R. Narasimha Rao BPHS translation
    BV_RAMAN = "bv_raman"    # BV Raman tradition
    KN_RAO   = "kn_rao"      # K.N. Rao school
    SANJAY_RATH = "sanjay_rath"  # Sanjay Rath tradition


# Which modules are active per school
_SCHOOL_MODULES: dict[School, set[str]] = {
    School.PARASHARI: {
        "dignity", "shadbala", "nakshatra", "ashtakavarga",
        "scoring_v3", "scoring_patches", "yogas", "extended_yogas",
        "bhava_and_transit", "special_lagnas", "dasha", "vimshottari",
        "planetary_state", "bhava_bala", "panchanga",
    },
    School.JAIMINI: {
        "jaimini_rashi_drishti", "chara_karaka_config", "karakamsha_analysis",
        "argala", "jaimini_full", "chara_dasha", "shoola_dasha",
    },
    School.KP: {
        "kp_sublord", "vimshottari",
        # KP requires true node + KP ayanamsha
    },
    School.TAJIKA: {
        "varshaphala",
    },
}

# Authority-specific overrides (where PVRNR and BV Raman disagree)
_AUTHORITY_OVERRIDES: dict[Authority, dict[str, object]] = {
    Authority.PVRNR: {
        "rahu_exalt_sign": 1,        # Taurus
        "ketu_exalt_sign": 7,        # Scorpio
        "node_mode": "mean",
        "chara_karaka_schema": "7",  # 7-planet schema
    },
    Authority.BV_RAMAN: {
        "rahu_exalt_sign": 2,        # Gemini
        "ketu_exalt_sign": 8,        # Sagittarius
        "node_mode": "mean",
        "chara_karaka_schema": "7",
    },
    Authority.KN_RAO: {
        "rahu_exalt_sign": 1,        # Follows PVRNR
        "node_mode": "mean",
        "use_pratyantar": True,
    },
    Authority.SANJAY_RATH: {
        "rahu_exalt_sign": 2,        # Follows BV Raman
        "node_mode": "true",
        "chara_karaka_schema": "8",  # 8-planet schema
        "ayanamsha": "true_citra",
    },
}


@dataclass
class CalcConfig:
    """
    Calculation configuration — declares school and authority.

    Usage:
        cfg = CalcConfig(school=School.PARASHARI, authority=Authority.PVRNR)
        cfg = CalcConfig(school=School.KP)   # KP forces true node + KP ayanamsha
        cfg = CalcConfig(school=School.JAIMINI, authority=Authority.SANJAY_RATH)
    """
    school: School = School.PARASHARI
    authority: Authority = Authority.PVRNR
    ayanamsha: str = "lahiri"
    node_mode: str = "mean"      # "mean" | "true"

    # Rule-level declarations (each rule in scoring carries a school tag)
    strict_school: bool = False  # If True, refuse cross-school rules

    def __post_init__(self):
        """Apply authority overrides and school-specific defaults."""
        # Apply authority overrides
        overrides = _AUTHORITY_OVERRIDES.get(self.authority, {})

        if "node_mode" in overrides and self.node_mode == "mean":
            self.node_mode = overrides["node_mode"]
        if "ayanamsha" in overrides and self.ayanamsha == "lahiri":
            self.ayanamsha = overrides["ayanamsha"]

        # School-specific forced settings
        if self.school == School.KP:
            self.node_mode = "true"
            if self.ayanamsha == "lahiri":
                self.ayanamsha = "krishnamurti"

    @property
    def rahu_exalt_sign(self) -> int:
        """Rahu exaltation sign index per authority."""
        overrides = _AUTHORITY_OVERRIDES.get(self.authority, {})
        return overrides.get("rahu_exalt_sign", 1)  # Default PVRNR: Taurus

    @property
    def ketu_exalt_sign(self) -> int:
        """Ketu exaltation sign index."""
        return (self.rahu_exalt_sign + 6) % 12

    @property
    def chara_karaka_schema(self) -> str:
        """7 or 8 planet Chara Karaka schema."""
        overrides = _AUTHORITY_OVERRIDES.get(self.authority, {})
        return overrides.get("chara_karaka_schema", "7")

    def is_module_active(self, module_name: str) -> bool:
        """Returns True if a calculation module is active under this school."""
        active = _SCHOOL_MODULES.get(self.school, set())
        # Parashari always includes Jaimini inputs (Chara Karakas etc.)
        if self.school == School.PARASHARI:
            active = active | _SCHOOL_MODULES[School.JAIMINI]
        return module_name in active

    def validate_rule(self, rule_id: str, rule_school: str) -> bool:
        """
        Validate that a scoring rule belongs to the declared school.
        If strict_school=True, reject cross-school rules.
        """
        if not self.strict_school:
            return True
        return rule_school == self.school.value

    @property
    def description(self) -> str:
        return (f"School: {self.school.value} | Authority: {self.authority.value} | "
                f"Ayanamsha: {self.ayanamsha} | Nodes: {self.node_mode}")


# Default config for backward compatibility
DEFAULT_CONFIG = CalcConfig()

# Pre-built configs for common use cases
PARASHARI_PVRNR   = CalcConfig(school=School.PARASHARI, authority=Authority.PVRNR)
PARASHARI_RAMAN   = CalcConfig(school=School.PARASHARI, authority=Authority.BV_RAMAN,
                               ayanamsha="raman")
KP_CONFIG         = CalcConfig(school=School.KP, ayanamsha="krishnamurti",
                               node_mode="true")
JAIMINI_RATH      = CalcConfig(school=School.JAIMINI, authority=Authority.SANJAY_RATH,
                               node_mode="true", ayanamsha="true_citra")
TAJIKA_CONFIG     = CalcConfig(school=School.TAJIKA, authority=Authority.PVRNR)
