"""
src/calculations/feature_decomp.py — Sessions 195–197

Feature decomposition: replaces 23 binary rule triggers with continuous
feature vectors suitable for ML analysis (Phase 6).

Each house yields a HouseFeatureVector of named float features.
ChartFeatureVector aggregates all 12 houses into a flat feature space.

S195: 4 extractors (gentle_sign, bhavesh_dignity, dig_bala, sav_bindus_norm)
S196: +4 extractors (kartari_score, combust_score, retrograde_score, bhavesh_house_type)
S197: +3 extractors (benefic_net_score, malefic_net_score, karak_score)
      = 11 × 12 = 132 features

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
  R04: PVRNR BPHS Ch.47 — bhavesh dignity and house placement
  R08/R12: Phaladeepika Ch.6 — Shubha / Paapa Kartari Yoga
  R19: BPHS Ch.3 v.51-59 — combustion (near Sun) diminishes planet's power
  R20: BPHS Ch.3 — Dig Bala (directional strength)
  R22: Phaladeepika Ch.2 v.9 — retrograde planets have altered significations
  R23: BPHS Ch.66 — Ashtakavarga SAV bindus
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

# House-type placement scores for bhavesh (R04 house placement aspect)
_HOUSE_TYPE_SCORE: dict[int, float] = {
    1: 1.0,   # kendra + trikona
    5: 0.9, 9: 0.9,          # trikona
    4: 0.75, 7: 0.75, 10: 0.75,  # kendra
    11: 0.5,                  # upachaya (gains)
    3: 0.4,                   # upachaya (growth)
    2: 0.3,                   # neutral (wealth)
    6: 0.1, 8: 0.1, 12: 0.1, # dusthana
}

# R22 retrograde scores by planet category
_OUTER_PLANETS = {"Jupiter", "Saturn"}
_INNER_PLANETS = {"Mercury", "Venus", "Mars"}

# Natural benefics / malefics for kartari (natural, not functional)
_NAT_BENEFIC_SET = frozenset({"Jupiter", "Venus", "Mercury", "Moon"})
_NAT_MALEFIC_SET = frozenset({"Sun", "Mars", "Saturn", "Rahu", "Ketu"})

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


# ── S196 extractors ──────────────────────────────────────────────────────────

def _build_sign_planets(chart, frame_lagna_si: int) -> dict[int, list[str]]:
    """Map sign_index → list of planet names in that sign."""
    sp: dict[int, list[str]] = {}
    for p, pos in chart.planets.items():
        sp.setdefault(pos.sign_index, []).append(p)
    return sp


def _extract_kartari_score(
    house: int, house_si: int, sign_planets: dict[int, list[str]]
) -> RuleFeature:
    """
    R08 + R12: Kartari Yoga score.
    +1.0 = Shubha Kartari (benefics flank house on both sides).
    -1.0 = Paapa Kartari (malefics flank house on both sides).
     0.0 = no kartari.
    Source: Phaladeepika Ch.6 — flanking planets have strong influence on bhava.
    """
    prev_si = (house_si - 1) % 12
    next_si = (house_si + 1) % 12
    prev_pl = sign_planets.get(prev_si, [])
    next_pl = sign_planets.get(next_si, [])
    shubh = (
        any(p in _NAT_BENEFIC_SET for p in prev_pl)
        and any(p in _NAT_BENEFIC_SET for p in next_pl)
    )
    paap = (
        any(p in _NAT_MALEFIC_SET for p in prev_pl)
        and any(p in _NAT_MALEFIC_SET for p in next_pl)
    )
    if shubh:
        val = 1.0
    elif paap:
        val = -1.0
    else:
        val = 0.0
    return RuleFeature("kartari_score", val, "R08/R12", house)


def _extract_combust_score(house: int, house_si: int, chart) -> RuleFeature:
    """
    R19: Combustion score for the bhavesh.
    +0.5 = cazimi (within 1° of Sun — actually strengthened).
     0.0 = not combust.
    -0.5 = combust.
    -1.0 = combust AND retrograde (worst).
    Source: BPHS Ch.3 v.51-59; Phaladeepika Ch.2 — combustion reduces planet significations.
    """
    bhavesh = _SIGN_LORD[house_si]
    if bhavesh not in chart.planets:
        return RuleFeature("combust_score", 0.0, "R19", house)

    try:
        from src.calculations.dignity import compute_all_dignities
        digs = compute_all_dignities(chart)
        dig = digs.get(bhavesh)
        if dig is None:
            return RuleFeature("combust_score", 0.0, "R19", house)
        if dig.cazimi:
            val = 0.5
        elif dig.combust and chart.planets[bhavesh].is_retrograde:
            val = -1.0
        elif dig.combust:
            val = -0.5
        else:
            val = 0.0
    except Exception:
        val = 0.0

    return RuleFeature("combust_score", val, "R19", house)


def _extract_retrograde_score(house: int, house_si: int, chart) -> RuleFeature:
    """
    R22: Retrograde score for the bhavesh.
    Outer planets (Jupiter/Saturn) rx → +0.25 (inner strength, slower but potent).
    Inner planets (Mercury/Venus/Mars) rx → -0.5 (disrupted significations).
    Sun/Moon never retrograde → 0.0.
    Source: Phaladeepika Ch.2 v.9; BPHS Ch.3 — vakra (retrograde) planets behave unusually.
    """
    bhavesh = _SIGN_LORD[house_si]
    if bhavesh not in chart.planets:
        return RuleFeature("retrograde_score", 0.0, "R22", house)

    is_rx = chart.planets[bhavesh].is_retrograde
    if not is_rx:
        return RuleFeature("retrograde_score", 0.0, "R22", house)

    if bhavesh in _OUTER_PLANETS:
        val = 0.25
    elif bhavesh in _INNER_PLANETS:
        val = -0.5
    else:
        val = 0.0

    return RuleFeature("retrograde_score", val, "R22", house)


def _extract_bhavesh_house_type(
    house: int, house_si: int, chart, frame_lagna_si: int
) -> RuleFeature:
    """
    R04 (house placement): Where is the bhavesh placed? [0, 1].
    1.0 = H1 (kendra + trikona), 0.75 = kendra, 0.9 = trikona, 0.1 = dusthana.
    Source: BPHS Ch.11 — house of bhavesh placement determines house promise.
    """
    bhavesh = _SIGN_LORD[house_si]
    if bhavesh not in chart.planets:
        return RuleFeature("bhavesh_house_type", 0.3, "R04", house)  # neutral default

    bh_house = (chart.planets[bhavesh].sign_index - frame_lagna_si) % 12 + 1
    val = _HOUSE_TYPE_SCORE.get(bh_house, 0.3)
    return RuleFeature("bhavesh_house_type", val, "R04", house)


# ── S197 extractors ──────────────────────────────────────────────────────────

def _aspects(planet: str, p_house: int, t_house: int) -> bool:
    """Basic aspect check (mirrors multi_axis_scoring)."""
    diff = (t_house - p_house) % 12
    if diff == 6:
        return True
    extras = {"Mars": {3, 9}, "Jupiter": {4, 8}, "Saturn": {2, 9}}
    return diff in extras.get(planet, set())


def _extract_benefic_net_score(
    house: int, house_si: int, chart, frame_lagna_si: int,
    is_fb, sign_planets: dict[int, list[str]]
) -> RuleFeature:
    """
    R02 + R03 + R06 + R07 combined: net functional-benefic strength for house.
    Score = (benefics_in_house + 0.5*fb_aspects_house + fb_with_bhavesh
             + 0.5*fb_aspects_bhavesh) / 5.0  → [0, 1]
    Source: PVRNR BPHS — benefic placement, aspect, and association all count.
    """
    bhavesh = _SIGN_LORD[house_si]
    p_house = {p: (pos.sign_index - frame_lagna_si) % 12 + 1
               for p, pos in chart.planets.items()}
    bh_house = p_house.get(bhavesh, house)
    in_house = sign_planets.get(house_si, [])

    score = 0.0
    for p in in_house:
        if is_fb(p):
            score += 1.0
    for p, pos in chart.planets.items():
        ph = p_house.get(p, 1)
        if is_fb(p) and p not in in_house and _aspects(p, ph, house):
            score += 0.5
    bh_si = chart.planets[bhavesh].sign_index if bhavesh in chart.planets else house_si
    bh_cotenants = [p for p in sign_planets.get(bh_si, []) if p != bhavesh]
    for p in bh_cotenants:
        if is_fb(p):
            score += 1.0
    for p, pos in chart.planets.items():
        ph = p_house.get(p, 1)
        if is_fb(p) and _aspects(p, ph, bh_house):
            score += 0.5

    return RuleFeature("benefic_net_score", round(min(1.0, score / 5.0), 4), "R02-R07", house)


def _extract_malefic_net_score(
    house: int, house_si: int, chart, frame_lagna_si: int,
    is_fm, sign_planets: dict[int, list[str]]
) -> RuleFeature:
    """
    R09 + R10 + R13 + R14 combined: net functional-malefic affliction for house.
    Score = (malefics_in_house + 0.5*fm_aspects_house + fm_with_bhavesh
             + 0.5*fm_aspects_bhavesh) / 5.0  → [0, 1]
    Source: PVRNR BPHS — malefic association and aspect reduce house promise.
    """
    bhavesh = _SIGN_LORD[house_si]
    p_house = {p: (pos.sign_index - frame_lagna_si) % 12 + 1
               for p, pos in chart.planets.items()}
    bh_house = p_house.get(bhavesh, house)
    in_house = sign_planets.get(house_si, [])

    score = 0.0
    for p in in_house:
        if is_fm(p):
            score += 1.0
    for p, pos in chart.planets.items():
        ph = p_house.get(p, 1)
        if is_fm(p) and p not in in_house and _aspects(p, ph, house):
            score += 0.5
    bh_si = chart.planets[bhavesh].sign_index if bhavesh in chart.planets else house_si
    bh_cotenants = [p for p in sign_planets.get(bh_si, []) if p != bhavesh]
    for p in bh_cotenants:
        if is_fm(p):
            score += 1.0
    for p, pos in chart.planets.items():
        ph = p_house.get(p, 1)
        if is_fm(p) and _aspects(p, ph, bh_house):
            score += 0.5

    return RuleFeature("malefic_net_score", round(min(1.0, score / 5.0), 4), "R09-R14", house)


_STHIR_KARAK: dict[int, set[str]] = {
    1: {"Sun"}, 2: {"Jupiter"}, 3: {"Mars"}, 4: {"Moon", "Venus"},
    5: {"Jupiter"}, 6: {"Mars", "Saturn"}, 7: {"Venus"}, 8: {"Saturn"},
    9: {"Sun", "Jupiter"}, 10: {"Sun", "Mercury", "Saturn"},
    11: {"Jupiter"}, 12: {"Saturn"},
}


def _extract_karak_score(
    house: int, house_si: int, chart, frame_lagna_si: int
) -> RuleFeature:
    """
    R17 + R18: Sthira Karak score for this house.
    +1.0 = all karakas for this house are in/aspecting it.
    -1.0 = all karakas are in dusthana from this house.
     0.0 = balanced / no karakas.
    Source: BPHS Ch.32 — Naisargika Karakatva (natural significators).
    """
    _DUSTHANA_SET = {6, 8, 12}
    karakas = _STHIR_KARAK.get(house, set())
    if not karakas:
        return RuleFeature("karak_score", 0.0, "R17/R18", house)

    pos_count = 0
    neg_count = 0
    total = 0

    for karak in karakas:
        if karak not in chart.planets:
            continue
        total += 1
        ksi = chart.planets[karak].sign_index
        kh = (ksi - frame_lagna_si) % 12 + 1
        if kh == house or _aspects(karak, kh, house):
            pos_count += 1
        else:
            dist = (house - kh) % 12 + 1
            if dist in _DUSTHANA_SET:
                neg_count += 1

    if total == 0:
        return RuleFeature("karak_score", 0.0, "R17/R18", house)

    val = round((pos_count - neg_count) / total, 4)
    return RuleFeature("karak_score", max(-1.0, min(1.0, val)), "R17/R18", house)


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

    sign_planets = _build_sign_planets(chart, lagna_si)

    # S197: functional benefic/malefic callables for this lagna
    try:
        import types
        from src.calculations.functional_roles import compute_functional_roles
        _SIGN_NAMES = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
        ]
        _fake = types.SimpleNamespace(
            lagna_sign_index=lagna_si,
            lagna_sign=_SIGN_NAMES[lagna_si],
            planets=chart.planets,
        )
        _roles = compute_functional_roles(_fake)
        is_fb = _roles.is_functional_benefic
        is_fm = _roles.is_functional_malefic
    except Exception:
        is_fb = lambda p: False  # noqa: E731
        is_fm = lambda p: False  # noqa: E731

    houses: dict[int, HouseFeatureVector] = {}
    for h in range(1, 13):
        house_si = (lagna_si + h - 1) % 12
        features = [
            # S195
            _extract_gentle_sign(h, house_si),
            _extract_bhavesh_dignity(h, house_si, chart),
            _extract_dig_bala(h, house_si, chart, lagna_si),
            _extract_sav_bindus_norm(h, house_si, av_bindus),
            # S196
            _extract_kartari_score(h, house_si, sign_planets),
            _extract_combust_score(h, house_si, chart),
            _extract_retrograde_score(h, house_si, chart),
            _extract_bhavesh_house_type(h, house_si, chart, lagna_si),
            # S197
            _extract_benefic_net_score(h, house_si, chart, lagna_si, is_fb, sign_planets),
            _extract_malefic_net_score(h, house_si, chart, lagna_si, is_fm, sign_planets),
            _extract_karak_score(h, house_si, chart, lagna_si),
        ]
        houses[h] = HouseFeatureVector(house=h, features=features)

    return ChartFeatureVector(lagna_sign=lagna_si, school=school, houses=houses)
