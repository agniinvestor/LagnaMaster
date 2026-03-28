"""
src/calculations/feature_decomp.py — Session 195

Feature decomposition: replaces 23 binary rule triggers with continuous
feature vectors suitable for ML analysis (Phase 6).

Each house yields a HouseFeatureVector of named float features.
ChartFeatureVector aggregates all 12 houses into a flat feature space.

S195: 4 extractors (gentle_sign, bhavesh_dignity, dig_bala, sav_bindus_norm)
      = 4 × 12 = 48 features

GUARDRAIL G22: No SHAP analysis or statistical inference without OSF
pre-registration (S201–S210). This module provides feature extraction
infrastructure only — analysis is deferred to Phase 6.

Public API
----------
  RuleFeature                                  — single named feature
  HouseFeatureVector                           — features for one house
  ChartFeatureVector                           — all 12 houses
  extract_features(chart, school) -> ChartFeatureVector

Classical sources
-----------------
  R01: BPHS Ch.11 — gentle/benefic signs for house placement
  R04: PVRNR BPHS Ch.47 — bhavesh dignity (exaltation, own, enemy, debilitation)
  R20: BPHS Ch.3 — Dig Bala (directional strength)
  R23: Brihat Parasara Hora Sastra Ch.66 — Ashtakavarga SAV bindus
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ── Sign-lord map (0=Aries … 11=Pisces) ──────────────────────────────────────
_SIGN_LORD: dict[int, str] = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun",
    5: "Mercury", 6: "Venus", 7: "Mars", 8: "Jupiter",
    9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

# R01 — gentle / benefic-natured signs (Cancer, Taurus, Libra, Pisces, Sag)
_GENTLE_SIGNS: frozenset[int] = frozenset({3, 1, 6, 11, 8})

# R20 — Dig Bala: planet → house of directional strength
_DIG_BALA: dict[str, int] = {
    "Sun": 10, "Mars": 10,
    "Moon": 4, "Venus": 4,
    "Mercury": 1, "Jupiter": 1,
    "Saturn": 7,
}

# Dignity score → normalised [-1, 1]
# Raw DIGNITY_SCORE max is 2.0 (DEEP_EXALT), min is -1.5 (DEBIL)
# Normalise: clamped to [-1.5, 2.0] then scaled to [-1, 1]
_DIG_RAW_MIN = -1.5
_DIG_RAW_MAX = 2.0


def _normalise_dignity(raw: float) -> float:
    """Map raw DIGNITY_SCORE value to [-1, 1]."""
    clipped = max(_DIG_RAW_MIN, min(_DIG_RAW_MAX, raw))
    span = _DIG_RAW_MAX - _DIG_RAW_MIN  # 3.5
    return round((clipped - _DIG_RAW_MIN) / span * 2.0 - 1.0, 4)


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass
class RuleFeature:
    """A single continuous feature derived from one scoring rule."""
    name: str         # short feature name, e.g. "gentle_sign"
    value: float      # continuous value, normalised to [-1,1] or [0,1]
    rule_id: str      # originating rule, e.g. "R01"
    house: int        # 1-12


@dataclass
class HouseFeatureVector:
    """
    Continuous feature vector for a single house.

    Features are stored in insertion order; to_dict() prefixes with
    "h{house:02d}_" to produce a unique flat namespace for the full chart.
    """
    house: int
    features: list[RuleFeature] = field(default_factory=list)

    def to_dict(self) -> dict[str, float]:
        """Return {h<house>_<name>: value} for each feature."""
        prefix = f"h{self.house:02d}_"
        return {prefix + rf.name: rf.value for rf in self.features}

    def to_array(self) -> list[float]:
        """Return feature values in insertion order."""
        return [float(rf.value) for rf in self.features]

    def feature_names(self) -> list[str]:
        prefix = f"h{self.house:02d}_"
        return [prefix + rf.name for rf in self.features]


@dataclass
class ChartFeatureVector:
    """
    Flat feature vector for a full chart (all 12 houses).

    Feature count = 12 × len(features per house).
    G22: Do not run SHAP or statistical analysis without OSF pre-registration.
    """
    lagna_sign: int   # 0-11
    school: str
    houses: dict[int, HouseFeatureVector] = field(default_factory=dict)

    def to_dict(self) -> dict[str, float]:
        """Flat dict: h01_gentle_sign … h12_sav_bindus_norm."""
        result: dict[str, float] = {}
        for hfv in self.houses.values():
            result.update(hfv.to_dict())
        return result

    def to_array(self) -> list[float]:
        """Values in house order (H1 first), then feature order within house."""
        result: list[float] = []
        for h in sorted(self.houses):
            result.extend(self.houses[h].to_array())
        return result

    def feature_names(self) -> list[str]:
        names: list[str] = []
        for h in sorted(self.houses):
            names.extend(self.houses[h].feature_names())
        return names

    def feature_count(self) -> int:
        return sum(len(hfv.features) for hfv in self.houses.values())


# ── Per-house extractors ──────────────────────────────────────────────────────

def _extract_gentle_sign(house: int, house_si: int) -> RuleFeature:
    """
    R01: Gentle/benefic sign for house.
    1.0 if house sign is Cancer/Taurus/Libra/Pisces/Sagittarius, else 0.0.
    Source: BPHS Ch.11 — Saumya (gentle) signs give benefic results.
    """
    val = 1.0 if house_si in _GENTLE_SIGNS else 0.0
    return RuleFeature("gentle_sign", val, "R01", house)


def _extract_bhavesh_dignity(house: int, house_si: int, chart) -> RuleFeature:
    """
    R04 (continuous): Dignity of the bhavesh (house lord) normalised to [-1, 1].
    1.0 = deep exaltation, -1.0 = deep debilitation.
    Source: PVRNR BPHS Ch.47 — bhavesh dignity determines house promise.
    """
    bhavesh = _SIGN_LORD[house_si]
    raw = 0.0  # neutral default

    if bhavesh in chart.planets:
        try:
            from src.calculations.dignity import compute_all_dignities, DIGNITY_SCORE
            digs = compute_all_dignities(chart)
            if bhavesh in digs:
                dl = digs[bhavesh].dignity
                raw = DIGNITY_SCORE.get(dl, 0.0)
        except Exception:
            raw = 0.0

    return RuleFeature("bhavesh_dignity", _normalise_dignity(raw), "R04", house)


def _extract_dig_bala(house: int, house_si: int, chart, frame_lagna_si: int) -> RuleFeature:
    """
    R20: Directional strength (Dig Bala) of bhavesh.
    1.0 if bhavesh occupies its Dig Bala house in this frame, else 0.0.
    Source: BPHS Ch.3 — planets gain full directional strength in specific houses.
    """
    bhavesh = _SIGN_LORD[house_si]
    bala_house = _DIG_BALA.get(bhavesh)
    if bala_house is None or bhavesh not in chart.planets:
        return RuleFeature("dig_bala", 0.0, "R20", house)

    bh_house = (chart.planets[bhavesh].sign_index - frame_lagna_si) % 12 + 1
    val = 1.0 if bh_house == bala_house else 0.0
    return RuleFeature("dig_bala", val, "R20", house)


def _extract_sav_bindus_norm(house: int, house_si: int, av_bindus: dict | None) -> RuleFeature:
    """
    R23 (continuous): Sarvashtakavarga bindu count normalised to [0, 1].
    Raw bindus range 0–8; 0 = weakest, 1.0 = maximum.
    Source: BPHS Ch.66 — ≥5 SAV bindus indicate strong house.
    """
    if av_bindus is None:
        return RuleFeature("sav_bindus_norm", 0.0, "R23", house)
    raw = float(av_bindus.get(house_si, 0))
    return RuleFeature("sav_bindus_norm", round(min(1.0, raw / 8.0), 4), "R23", house)


# ── Top-level extractor ───────────────────────────────────────────────────────

def extract_features(chart, school: str = "parashari") -> ChartFeatureVector:
    """
    Extract continuous feature vectors for all 12 houses of *chart*.

    S195: 4 features per house = 48 total features.
    Subsequent sessions (S196–S200) add more extractors.

    GUARDRAIL G22: Output is for infrastructure/ML pipeline use only.
    No SHAP or empirical analysis without OSF pre-registration.

    Args:
        chart:  BirthChart
        school: scoring school (stored in ChartFeatureVector; affects future extractors)

    Returns:
        ChartFeatureVector with HouseFeatureVector for each of houses 1–12.
    """
    lagna_si: int = chart.lagna_sign_index

    # Pre-compute Ashtakavarga for all houses
    av_bindus: dict | None = None
    try:
        from src.calculations.ashtakavarga import compute_ashtakavarga
        av = compute_ashtakavarga(chart)
        av_bindus = {si: av.sarva_ashtakavarga.get(si, 0) for si in range(12)}
    except Exception:
        av_bindus = None

    houses: dict[int, HouseFeatureVector] = {}
    for h in range(1, 13):
        house_si = (lagna_si + h - 1) % 12
        features = [
            _extract_gentle_sign(h, house_si),
            _extract_bhavesh_dignity(h, house_si, chart),
            _extract_dig_bala(h, house_si, chart, lagna_si),
            _extract_sav_bindus_norm(h, house_si, av_bindus),
        ]
        houses[h] = HouseFeatureVector(house=h, features=features)

    return ChartFeatureVector(lagna_sign=lagna_si, school=school, houses=houses)
