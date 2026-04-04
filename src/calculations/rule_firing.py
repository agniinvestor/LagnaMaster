"""src/calculations/rule_firing.py — Evaluate which corpus rules fire for a chart.

Bridges the corpus (6,500+ rules) to the scoring engine by evaluating each
rule's primary_condition against a computed chart.

Usage:
    from src.calculations.rule_firing import evaluate_chart
    result = evaluate_chart(chart)
    # result.fired_rules: list of FiredRule
    # result.house_summary: dict[int, HouseRuleSummary]
    # result.feature_vector(): dict of ML-ready features
"""
from __future__ import annotations

from dataclasses import dataclass, field

_MALEFICS = ("Sun", "Mars", "Saturn", "Rahu", "Ketu")
_BENEFICS = ("Jupiter", "Venus", "Mercury", "Moon")


@dataclass
class FiredRule:
    """A single corpus rule that fires for this chart."""
    rule_id: str
    source: str
    planet: str
    house: int  # 0 if not house-specific
    outcome_direction: str
    outcome_domains: list[str]
    confidence: float
    concordance_count: int  # how many texts agree
    # Tier 3 audit trail fields
    entity_target: str = "native"
    predictions: list[dict] = field(default_factory=list)
    signal_group: str = ""
    health_sensitive: bool = False
    context: dict | None = None


@dataclass
class SkippedRule:
    """A rule that was evaluated but did NOT fire, with the reason."""
    rule_id: str
    reason: str  # "condition_not_met" | "lagna_scope_mismatch" | "no_conditions" | "unsupported_type"


@dataclass
class HouseRuleSummary:
    """Aggregated rule-firing statistics for one house."""
    house: int
    total_fired: int = 0
    favorable_count: int = 0
    unfavorable_count: int = 0
    mixed_count: int = 0
    neutral_count: int = 0
    mean_confidence: float = 0.0
    source_count: int = 0  # unique sources that fired rules for this house
    concordance_score: float = 0.0  # fraction of rules with concordance
    dominant_direction: str = "neutral"


@dataclass
class RuleFiringResult:
    """Complete rule-firing evaluation for a chart."""
    fired_rules: list[FiredRule] = field(default_factory=list)
    skipped_rules: list[SkippedRule] = field(default_factory=list)  # Tier 3 audit trail
    house_summary: dict[int, HouseRuleSummary] = field(default_factory=dict)
    total_fired: int = 0
    total_evaluated: int = 0
    corpus_hash: str = ""  # Tier 3 Item 7: model-corpus version pinning

    def feature_vector(self) -> dict[str, float]:
        """Return ML-ready features from rule firing.

        Features per house (12 houses × 7 features = 84 features):
          h{N}_rules_fired: total rules that fired
          h{N}_favorable_ratio: fraction of fired rules that are favorable
          h{N}_unfavorable_ratio: fraction of fired rules that are unfavorable
          h{N}_mean_confidence: average confidence of fired rules
          h{N}_source_count: number of unique source texts
          h{N}_concordance_score: fraction with cross-text concordance
          h{N}_direction_score: +1 if dominant favorable, -1 if unfavorable, 0 mixed

        Global features (5):
          global_total_fired: total rules fired across all houses
          global_favorable_ratio: overall favorable ratio
          global_mean_confidence: overall mean confidence
          global_concordance_ratio: fraction of all fired rules with concordance
          global_source_diversity: unique sources across all fired rules
        """
        features: dict[str, float] = {}

        for h in range(1, 13):
            s = self.house_summary.get(h)
            prefix = f"h{h:02d}"
            if s and s.total_fired > 0:
                features[f"{prefix}_rules_fired"] = float(s.total_fired)
                features[f"{prefix}_favorable_ratio"] = s.favorable_count / s.total_fired
                features[f"{prefix}_unfavorable_ratio"] = s.unfavorable_count / s.total_fired
                features[f"{prefix}_mean_confidence"] = s.mean_confidence
                features[f"{prefix}_source_count"] = float(s.source_count)
                features[f"{prefix}_concordance_score"] = s.concordance_score
                dir_score = (s.favorable_count - s.unfavorable_count) / s.total_fired
                features[f"{prefix}_direction_score"] = dir_score
            else:
                features[f"{prefix}_rules_fired"] = 0.0
                features[f"{prefix}_favorable_ratio"] = 0.0
                features[f"{prefix}_unfavorable_ratio"] = 0.0
                features[f"{prefix}_mean_confidence"] = 0.0
                features[f"{prefix}_source_count"] = 0.0
                features[f"{prefix}_concordance_score"] = 0.0
                features[f"{prefix}_direction_score"] = 0.0

        # Global features
        if self.total_fired > 0:
            all_fav = sum(1 for r in self.fired_rules if r.outcome_direction == "favorable")
            all_conc = sum(1 for r in self.fired_rules if r.concordance_count > 0)
            all_sources = len({r.source for r in self.fired_rules})
            features["global_total_fired"] = float(self.total_fired)
            features["global_favorable_ratio"] = all_fav / self.total_fired
            features["global_mean_confidence"] = sum(r.confidence for r in self.fired_rules) / self.total_fired
            features["global_concordance_ratio"] = all_conc / self.total_fired
            features["global_source_diversity"] = float(all_sources)
        else:
            features["global_total_fired"] = 0.0
            features["global_favorable_ratio"] = 0.0
            features["global_mean_confidence"] = 0.0
            features["global_concordance_ratio"] = 0.0
            features["global_source_diversity"] = 0.0

        return features


def _find_planet(chart, planet_name: str):
    """Find a PlanetPosition by name (case-insensitive)."""
    p = chart.planets.get(planet_name)
    if p:
        return p
    for key in chart.planets:
        if key.lower() == planet_name.lower():
            return chart.planets[key]
    return None


def _planet_house(chart, planet_name: str) -> int:
    """Get house number (1-12) for a planet using sign-based system."""
    p = _find_planet(chart, planet_name)
    if not p:
        return 0
    return (p.sign_index - chart.lagna_sign_index) % 12 + 1


def _planet_sign(chart, planet_name: str) -> str:
    """Get sign name for a planet."""
    p = _find_planet(chart, planet_name)
    if not p:
        return ""
    return p.sign.lower()


def _normalize_planet_name(name: str) -> str:
    """Normalize planet name for lookup."""
    return name.lower().replace(" ", "")


# ── Sign lords (0=Aries → Mars, 1=Taurus → Venus, etc.) ──────────────────────
_SIGN_LORDS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
    4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
    8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

# ── Exaltation/debilitation/own signs (from dignity.py, duplicated for perf) ──
_EXALT_SIGN = {
    "Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5,
    "Jupiter": 3, "Venus": 11, "Saturn": 6, "Rahu": 1, "Ketu": 7,
}
_DEBIL_SIGN = {
    "Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11,
    "Jupiter": 9, "Venus": 5, "Saturn": 0, "Rahu": 7, "Ketu": 1,
}
_OWN_SIGNS = {
    "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
    "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10],
    "Rahu": [10], "Ketu": [7],
}
_MT_SIGNS = {
    "Sun": 4, "Moon": 1, "Mars": 0, "Mercury": 5,
    "Jupiter": 8, "Venus": 6, "Saturn": 10,
}

# ── Parashari graha drishti (7th always; Mars 4,8; Jupiter 5,9; Saturn 3,10) ──
_SPECIAL_ASPECTS = {
    "Mars": {3, 7},      # 4th and 8th (0-indexed diffs: 3, 7)
    "Jupiter": {4, 8},   # 5th and 9th
    "Saturn": {2, 9},    # 3rd and 10th
}


def _lord_of_house(chart, house_num: int) -> str:
    """Return the planet name that lords over a given house (1-12).

    Uses sign-based whole-sign house system:
      house 1 = lagna sign, house 2 = lagna sign + 1, etc.
    """
    sign_index = (chart.lagna_sign_index + house_num - 1) % 12
    return _SIGN_LORDS.get(sign_index, "")


def _planet_dignity_state(chart, planet_name: str) -> str:
    """Return the dignity state of a planet: exalted|debilitated|own_sign|moolatrikona|neutral.

    Simplified check using sign position. For full dignity with neecha bhanga,
    combustion etc., use dignity.compute_dignity().
    """
    p = _find_planet(chart, planet_name)
    if not p:
        return "unknown"
    name = p.name if hasattr(p, "name") else planet_name
    # Standardize name for table lookup
    for std_name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                     "Saturn", "Rahu", "Ketu"):
        if std_name.lower() == name.lower():
            name = std_name
            break
    si = p.sign_index
    if name in _EXALT_SIGN and si == _EXALT_SIGN[name]:
        return "exalted"
    if name in _DEBIL_SIGN and si == _DEBIL_SIGN[name]:
        return "debilitated"
    if name in _MT_SIGNS and si == _MT_SIGNS[name]:
        return "moolatrikona"
    if name in _OWN_SIGNS and si in _OWN_SIGNS[name]:
        return "own_sign"
    return "neutral"


def _planet_aspects_house(chart, planet_name: str, target_house: int) -> bool:
    """Check if a planet aspects a target house via Parashari graha drishti.

    Every planet aspects the 7th house from its position.
    Mars also aspects 4th and 8th; Jupiter 5th and 9th; Saturn 3rd and 10th.
    """
    p_house = _planet_house(chart, planet_name)
    if p_house == 0:
        return False
    diff = (target_house - p_house) % 12
    # All planets aspect 7th (diff=6 in 0-indexed)
    if diff == 6:
        return True
    # Special aspects
    name = planet_name.title()
    for std_name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                     "Saturn", "Rahu", "Ketu"):
        if std_name.lower() == name.lower():
            name = std_name
            break
    return diff in _SPECIAL_ASPECTS.get(name, set())


_DIGNITY_RANK = {"exalted": 5, "moolatrikona": 4, "own_sign": 3, "neutral": 2, "debilitated": 1, "unknown": 0}
MAX_BIND_ATTEMPTS = 10


def _check_with_bindings(conditions: list[dict], chart, context: dict | None = None) -> tuple[bool, int]:
    """Evaluate conditions with bind variables. Strongest valid binding wins."""
    # Find the bind-producing condition (first one with "bind" field)
    bind_idx = None
    bind_var = None
    for i, cond in enumerate(conditions):
        if cond.get("bind"):
            bind_idx = i
            bind_var = cond["bind"]
            break

    if bind_idx is None:
        return _check_compound_conditions(conditions, chart, context)

    bind_cond = conditions[bind_idx]
    planet_spec = bind_cond.get("planet", "")

    # Resolve candidate list
    if planet_spec == "any_benefic":
        candidates = list(_BENEFICS)
    elif planet_spec == "any_malefic":
        candidates = list(_MALEFICS)
    else:
        candidates = [planet_spec.title()]

    # Filter to planets that exist in chart
    candidates = [c for c in candidates if _find_planet(chart, c)]

    # Rank by dignity (strongest first)
    candidates.sort(key=lambda p: _DIGNITY_RANK.get(_planet_dignity_state(chart, p), 0), reverse=True)

    # Try each candidate
    for attempt, planet in enumerate(candidates[:MAX_BIND_ATTEMPTS]):
        # Substitute: replace bind var with specific planet in all conditions
        resolved = []
        for cond in conditions:
            c = dict(cond)
            if c.get("bind") == bind_var:
                c["planet"] = planet
                c.pop("bind", None)
            elif c.get("planet") == bind_var:
                c["planet"] = planet
            resolved.append(c)

        fires, house = _check_compound_conditions(resolved, chart, context)
        if fires:
            return True, house

    return False, 0


def _check_compound_conditions(conditions: list[dict], chart, context: dict | None = None) -> tuple[bool, int]:
    """Evaluate a list of computable primitive conditions (AND logic).

    Each condition dict has a "type" key. All must be true for the rule to fire.
    Returns (fires, house) where house is from the first house-specific condition.
    """
    if not conditions:
        return False, 0

    # Detect bind variables — if present, delegate to bind-aware evaluator
    has_binds = any(c.get("bind") for c in conditions)
    if has_binds:
        return _check_with_bindings(conditions, chart, context)

    matched_house = 0

    for idx, cond in enumerate(conditions):
        ctype = cond.get("type", "")

        if ctype == "planet_in_house":
            planet = cond.get("planet", "")
            target = cond.get("house", 0)
            actual = _planet_house(chart, planet.title())
            if isinstance(target, list):
                if actual not in target:
                    return False, 0
            elif actual != target:
                return False, 0
            matched_house = matched_house or actual

        elif ctype == "planet_in_sign":
            planet = cond.get("planet", "")
            raw_sign = cond.get("sign", "")
            if isinstance(raw_sign, list):
                target_signs = [s.lower() for s in raw_sign]
            else:
                target_signs = [raw_sign.lower()]
            actual_sign = _planet_sign(chart, planet.title())
            if actual_sign not in target_signs:
                return False, 0
            matched_house = matched_house or _planet_house(chart, planet.title())

        elif ctype == "lord_in_house":
            lord_of = cond.get("lord_of", 0)
            target = cond.get("house", 0)
            lord_planet = _lord_of_house(chart, lord_of)
            if not lord_planet:
                return False, 0
            actual = _planet_house(chart, lord_planet)
            if target == "any":
                pass  # lord exists, any house is fine
            elif isinstance(target, list):
                if actual not in target:
                    return False, 0
            elif actual != target:
                return False, 0
            matched_house = matched_house or actual

        elif ctype == "lord_in_sign":
            lord_of = cond.get("lord_of", 0)
            raw_sign = cond.get("sign", "")
            if isinstance(raw_sign, list):
                target_signs = [s.lower() for s in raw_sign]
            else:
                target_signs = [raw_sign.lower()]
            lord_planet = _lord_of_house(chart, lord_of)
            if not lord_planet:
                return False, 0
            actual_sign = _planet_sign(chart, lord_planet)
            if actual_sign not in target_signs:
                return False, 0
            matched_house = matched_house or _planet_house(chart, lord_planet)

        elif ctype == "planet_dignity":
            planet = cond.get("planet", "")
            target_dignity = cond.get("dignity", "")
            # Handle "lord_of_N" references
            if planet.startswith("lord_of_"):
                house_num = int(planet.split("_")[-1])
                planet = _lord_of_house(chart, house_num)
            if not planet:
                return False, 0
            actual_dignity = _planet_dignity_state(chart, planet)
            if target_dignity == "strong":
                # "strong" = exalted, own_sign, or moolatrikona
                if actual_dignity not in ("exalted", "own_sign", "moolatrikona"):
                    return False, 0
            elif target_dignity == "weak":
                # "weak" = debilitated or neutral (not strong)
                if actual_dignity in ("exalted", "own_sign", "moolatrikona"):
                    return False, 0
            elif actual_dignity != target_dignity:
                return False, 0

        elif ctype == "planet_aspecting":
            planet = cond.get("planet", "")
            target_house = cond.get("house", 0)
            if planet.startswith("lord_of_"):
                house_num = int(planet.split("_")[-1])
                planet = _lord_of_house(chart, house_num)
            if not planet:
                return False, 0
            if not _planet_aspects_house(chart, planet, target_house):
                return False, 0
            matched_house = matched_house or target_house

        elif ctype == "planets_conjunct":
            planets = cond.get("planets", [])
            if len(planets) < 2:
                return False, 0
            houses = [_planet_house(chart, p.title()) for p in planets]
            if any(h == 0 for h in houses) or len(set(houses)) != 1:
                return False, 0
            matched_house = matched_house or houses[0]

        elif ctype == "planets_conjunct_in_house":
            planets = cond.get("planets", [])
            target = cond.get("house", 0)
            houses = [_planet_house(chart, p.title()) for p in planets]
            if any(h == 0 for h in houses) or len(set(houses)) != 1:
                return False, 0
            if houses[0] != target:
                return False, 0
            matched_house = target

        elif ctype == "planet_in_house_from":
            planet_spec = cond.get("planet", "")
            ref_spec = cond.get("reference", "")
            offset = cond.get("offset", 0)

            # Resolve reference → must be exactly 1 planet
            resolved_ref = []
            if ref_spec.startswith("lord_of_"):
                h = int(ref_spec.split("_")[-1])
                p = _lord_of_house(chart, h)
                if p:
                    resolved_ref = [p]
            else:
                p = ref_spec.strip().title()
                if _find_planet(chart, p):
                    resolved_ref = [p]

            if len(resolved_ref) != 1:
                return False, 0

            ref_planet = resolved_ref[0]
            ref_house = _planet_house(chart, ref_planet)
            # BPHS inclusive counting: "5th from house 3" = house 7 (3,4,5,6,7)
            target_house = (ref_house + offset - 2) % 12 + 1

            # Resolve planet → may be multiple (any_malefic, etc.)
            if planet_spec == "any_malefic":
                candidates = list(_MALEFICS)
            elif planet_spec == "any_benefic":
                candidates = list(_BENEFICS)
            elif planet_spec.startswith("lord_of_"):
                lh = int(planet_spec.split("_")[-1])
                lord = _lord_of_house(chart, lh)
                candidates = [lord] if lord else []
            else:
                candidates = [planet_spec.strip().title()]

            valid_candidates = [c for c in candidates if _find_planet(chart, c)]
            if not valid_candidates:
                return False, 0

            hit = any(
                _planet_house(chart, c) == target_house
                for c in valid_candidates
            )
            if not hit:
                return False, 0
            matched_house = matched_house or target_house

        elif ctype == "planet_not_in_house":
            planet_spec = cond.get("planet", "")
            target_house = cond.get("house", 0)
            if isinstance(target_house, list):
                target_house = target_house[0]
            if planet_spec == "any_benefic":
                candidates = list(_BENEFICS)
            elif planet_spec == "any_malefic":
                candidates = list(_MALEFICS)
            else:
                candidates = [planet_spec.strip().title()]
            valid = [c for c in candidates if _find_planet(chart, c)]
            if any(_planet_house(chart, c) == target_house for c in valid):
                return False, 0
            matched_house = matched_house or target_house

        elif ctype == "planet_not_aspecting":
            planet_spec = cond.get("planet", "")
            target_house = cond.get("house", 0)
            if isinstance(target_house, list):
                target_house = target_house[0]
            if planet_spec == "any_benefic":
                candidates = list(_BENEFICS)
            elif planet_spec == "any_malefic":
                candidates = list(_MALEFICS)
            else:
                candidates = [planet_spec.strip().title()]
            valid = [c for c in candidates if _find_planet(chart, c)]
            if any(_planet_aspects_house(chart, c, target_house) for c in valid):
                return False, 0
            matched_house = matched_house or target_house

        elif ctype == "planet_in_navamsa_sign":
            planet_name = cond.get("planet", "")
            target_signs = cond.get("sign", [])
            if isinstance(target_signs, str):
                target_signs = [target_signs]
            target_signs_lower = [s.lower() for s in target_signs]

            if planet_name.startswith("lord_of_"):
                h = int(planet_name.split("_")[-1])
                planet_name = _lord_of_house(chart, h)
            if not planet_name:
                return False, 0

            pos = _find_planet(chart, planet_name.strip().title())
            if not pos:
                return False, 0

            # Compute navamsa sign
            # Standard navamsa: divide 30 degrees into 9 parts (3.333... each)
            # Starting sign depends on element of rasi sign
            FIRE_SIGNS = {0, 4, 8}      # Aries, Leo, Sagittarius
            EARTH_SIGNS = {1, 5, 9}     # Taurus, Virgo, Capricorn
            AIR_SIGNS = {2, 6, 10}      # Gemini, Libra, Aquarius
            # WATER_SIGNS = {3, 7, 11} — else branch handles Cancer/Scorpio/Pisces

            pada = int(pos.degree_in_sign / (30.0 / 9))
            if pada >= 9:
                pada = 8

            sign_idx = pos.sign_index
            if sign_idx in FIRE_SIGNS:
                start = 0       # Aries
            elif sign_idx in EARTH_SIGNS:
                start = 3       # Cancer
            elif sign_idx in AIR_SIGNS:
                start = 6       # Libra
            else:  # WATER
                start = 9       # Capricorn

            navamsa_sign_idx = (start + pada) % 12
            SIGN_NAMES = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                          "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
            navamsa_sign = SIGN_NAMES[navamsa_sign_idx]

            if navamsa_sign not in target_signs_lower:
                return False, 0

        elif ctype == "dispositor_condition":
            planet_name = cond.get("planet", "")
            state = cond.get("dispositor_state", "")

            if planet_name.startswith("lord_of_"):
                h = int(planet_name.split("_")[-1])
                planet_name = _lord_of_house(chart, h)
            if not planet_name:
                return False, 0

            pos = _find_planet(chart, planet_name.strip().title())
            if not pos:
                return False, 0

            # Dispositor = lord of the sign the planet occupies
            _SIGN_LORDS_LIST = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
                                "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
            dispositor = _SIGN_LORDS_LIST[pos.sign_index]

            if state == "in_house":
                target_house = cond.get("house", 0)
                if isinstance(target_house, list):
                    if _planet_house(chart, dispositor) not in target_house:
                        return False, 0
                else:
                    if _planet_house(chart, dispositor) != target_house:
                        return False, 0
                matched_house = matched_house or (target_house if isinstance(target_house, int) else target_house[0])
            elif state == "dignity":
                target_dignity = cond.get("dignity", "")
                actual_dignity = _planet_dignity_state(chart, dispositor)
                if target_dignity in ("strong", "weak"):
                    strong_states = {"exalted", "own_sign", "moolatrikona"}
                    if target_dignity == "strong" and actual_dignity not in strong_states:
                        return False, 0
                    if target_dignity == "weak" and actual_dignity in strong_states | {"neutral"}:
                        return False, 0
                else:
                    if actual_dignity != target_dignity:
                        return False, 0

        elif ctype == "argala_condition":
            from src.calculations.argala import compute_argala
            ref_house = cond.get("reference_house", 1)
            argala_type = cond.get("argala_type", "any")
            min_strength = cond.get("min_strength", "weak")
            obstruction_req = cond.get("obstruction", "any")

            result = compute_argala(chart, ref_house)

            # If no entries at all, argala doesn't apply
            if not result.entries:
                return False, 0

            # Normalize score: theoretical max = 12.0 (v1_linear)
            max_score = 12.0
            normalized = min(1.0, max(0.0, abs(result.net_argala_score) / max_score))

            # Filter by argala_type
            if argala_type == "benefic":
                matching = [e for e in result.entries if e.nature == "benefic_argala"]
                if not matching:
                    return False, 0
            elif argala_type == "malefic":
                matching = [e for e in result.entries if e.nature == "malefic_argala"]
                if not matching:
                    return False, 0

            # Filter by obstruction
            if obstruction_req == "unobstructed":
                active = [e for e in result.entries if not e.is_obstructed]
                if not active:
                    return False, 0
            elif obstruction_req == "partial":
                obstructed = [e for e in result.entries if e.is_obstructed]
                if not obstructed:
                    return False, 0

            # Check min_strength threshold
            strength_thresholds = {"weak": 0.01, "medium": 0.15, "strong": 0.35}
            if normalized < strength_thresholds.get(min_strength, 0.01):
                return False, 0

            # Determine actual type
            natures = {e.nature for e in result.entries if not e.is_obstructed}
            if natures == {"benefic_argala"}:
                actual_type = "benefic"
            elif natures == {"malefic_argala"}:
                actual_type = "malefic"
            else:
                actual_type = "mixed"

            # Obstruction level
            total = len(result.entries)
            obstructed_count = sum(1 for e in result.entries if e.is_obstructed)
            if total == 0:
                obs_level = "none"
            elif obstructed_count == 0:
                obs_level = "unobstructed"
            elif obstructed_count == total:
                obs_level = "full"
            else:
                obs_level = "partial"

            # Emit metadata to context
            if context is not None:
                context["conditions"][f"cond_{idx}"] = {
                    "type": "argala_condition",
                    "metadata": {
                        "argala_strength": round(normalized, 3),
                        "argala_type": actual_type,
                        "obstruction": obs_level,
                        "contributing_houses": [e.house_from_reference for e in result.entries if not e.is_obstructed],
                        "net_score": result.net_argala_score,
                        "normalization_version": "v1_linear",
                    },
                }
            matched_house = matched_house or ref_house

        elif ctype == "functional_benefic":
            from src.calculations.functional_dignity import compute_functional_classifications
            planet_spec = cond.get("planet", "")
            classification = cond.get("classification", "")
            if planet_spec.startswith("lord_of_"):
                h = int(planet_spec.split("_")[-1])
                planet_spec = _lord_of_house(chart, h)
            if not planet_spec or not _find_planet(chart, planet_spec.title()):
                return False, 0
            planet_name = planet_spec.title()
            fc = compute_functional_classifications(chart.lagna_sign_index)
            entry = fc.get(planet_name)
            if not entry:
                return False, 0
            if classification == "benefic" and not entry.is_functional_benefic:
                return False, 0
            elif classification == "malefic" and not entry.is_functional_malefic:
                return False, 0
            elif classification == "yogakaraka" and not entry.is_yogakaraka:
                return False, 0
            elif classification == "maraka" and not entry.is_maraka:
                return False, 0
            elif classification == "badhaka" and not entry.is_badhaka:
                return False, 0

        elif ctype == "dynamic_karaka":
            karaka = cond.get("karaka", "")
            state = cond.get("state", "")
            if karaka == "mother":
                candidates = ["Moon", "Mars"]
            elif karaka == "father":
                candidates = ["Sun", "Jupiter"]
            else:
                return False, 0
            ranked = sorted(candidates, key=lambda p: _DIGNITY_RANK.get(
                _planet_dignity_state(chart, p), 0), reverse=True)
            resolved = ranked[0]
            actual_dignity = _planet_dignity_state(chart, resolved)
            if state == "strong":
                if actual_dignity not in ("exalted", "own_sign", "moolatrikona"):
                    return False, 0
            elif state == "weak":
                if actual_dignity in ("exalted", "own_sign", "moolatrikona"):
                    return False, 0
            matched_house = matched_house or _planet_house(chart, resolved)

        elif ctype == "shadbala_strength":
            planet_spec = cond.get("planet", "")
            threshold = cond.get("threshold", "weak")
            if planet_spec.startswith("lord_of_"):
                h = int(planet_spec.split("_")[-1])
                planet_spec = _lord_of_house(chart, h)
            if not planet_spec or not _find_planet(chart, planet_spec.title()):
                return False, 0
            try:
                from src.calculations.shadbala import compute_shadbala
                sb = compute_shadbala(planet_spec.title(), chart)
                total = getattr(sb, "total", 0.0)
                normalized = min(1.0, max(0.0, total / 1.0)) if total else 0.0
            except Exception:
                # Shadbala may need birth_dt — if it fails, condition can't be evaluated
                return False, 0
            if threshold == "weak" and normalized >= 0.5:
                return False, 0
            elif threshold == "strong" and normalized < 0.5:
                return False, 0
            if context is not None:
                context["conditions"][f"cond_{idx}"] = {
                    "type": "shadbala_strength",
                    "metadata": {"shadbala_normalized": round(normalized, 3)},
                }

        elif ctype == "navamsa_lagna":
            target_signs = cond.get("sign", [])
            if isinstance(target_signs, str):
                target_signs = [target_signs]
            target_lower = [s.lower() for s in target_signs]
            lagna_degree = getattr(chart, "lagna_degree", None)
            if lagna_degree is None:
                return False, 0
            FIRE_SIGNS = {0, 4, 8}
            EARTH_SIGNS = {1, 5, 9}
            AIR_SIGNS = {2, 6, 10}
            lsi = chart.lagna_sign_index
            pada = int(lagna_degree / (30.0 / 9))
            if pada >= 9:
                pada = 8
            if lsi in FIRE_SIGNS:
                start = 0
            elif lsi in EARTH_SIGNS:
                start = 3
            elif lsi in AIR_SIGNS:
                start = 6
            else:
                start = 9
            nav_si = (start + pada) % 12
            SIGN_NAMES = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                          "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
            if SIGN_NAMES[nav_si] not in target_lower:
                return False, 0

        elif ctype == "derived_points_relationship":
            from src.calculations.argala import compute_arudha
            point_a = cond.get("point_a", {})
            point_b = cond.get("point_b", {})
            relationship = cond.get("relationship", "")

            # Compute both arudha points
            a_si = compute_arudha(chart, point_a.get("house", 1))
            b_si = compute_arudha(chart, point_b.get("house", 7))

            # Offset from A to B (1-based)
            offset = (b_si - a_si) % 12 + 1

            KENDRA = {1, 4, 7, 10}
            TRIKONA = {1, 5, 9}
            DUSTHANA = {6, 8, 12}
            UPACHAYA = {3, 6, 10, 11}

            if relationship == "kendra_trikona":
                if offset not in (KENDRA | TRIKONA):
                    return False, 0
            elif relationship == "dusthana":
                if offset not in DUSTHANA:
                    return False, 0
            elif relationship == "upachaya":
                if offset not in UPACHAYA:
                    return False, 0
            elif relationship == "kendra_trikona_upachaya":
                if offset not in (KENDRA | TRIKONA | UPACHAYA):
                    return False, 0

        elif ctype == "derived_house_sign":
            from src.calculations.argala import compute_arudha
            base_house = cond.get("base_house", 1)
            offset = cond.get("offset", 1)
            target_signs = cond.get("sign", [])
            if isinstance(target_signs, str):
                target_signs = [target_signs]
            target_lower = [s.lower() for s in target_signs]

            # Compute the derived point
            derived_si = compute_arudha(chart, base_house)
            # Apply offset (inclusive counting)
            target_si = (derived_si + offset - 1) % 12

            SIGN_NAMES = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                          "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
            if SIGN_NAMES[target_si] not in target_lower:
                return False, 0

        elif ctype == "lord_of_derived_house":
            from src.calculations.argala import compute_arudha
            base_house = cond.get("base_house", 1)
            offset = cond.get("offset", 1)
            lord_state = cond.get("lord_state", "")

            derived_si = compute_arudha(chart, base_house)
            target_si = (derived_si + offset - 1) % 12
            lord = _SIGN_LORDS.get(target_si, "")

            if not lord or not _find_planet(chart, lord):
                return False, 0

            if lord_state == "own_sign":
                dignity = _planet_dignity_state(chart, lord)
                if dignity != "own_sign":
                    return False, 0
            elif lord_state == "in_target":
                lord_pos = _find_planet(chart, lord)
                if lord_pos is None or lord_pos.sign_index != target_si:
                    return False, 0
            elif lord_state:
                dignity = _planet_dignity_state(chart, lord)
                if dignity != lord_state:
                    return False, 0

        else:
            # Unknown condition type — can't evaluate, rule doesn't fire
            return False, 0

    return True, matched_house


def _check_rule_fires(rule, chart) -> tuple[bool, int, dict | None]:
    """Check if a rule's primary_condition is satisfied by this chart.

    Returns (fires: bool, house: int, context: dict | None).
    House is 0 for non-house-specific rules.
    Context is populated only for V2 rules; legacy paths return None.
    """
    pc = rule.primary_condition
    if not pc:
        return False, 0, None

    # V2 computable primitives — use conditions list if present.
    # V2 conditions is a list of dicts with "type" keys.
    # Legacy "conditions" (pre-V2) is a single dict — skip those.
    conditions = pc.get("conditions", [])
    if isinstance(conditions, list) and conditions and isinstance(conditions[0], dict) and "type" in conditions[0]:
        context: dict = {"conditions": {}, "aggregates": {}, "gates": {}}
        fires, house = _check_compound_conditions(conditions, chart, context=context)
        return fires, house, context

    planet = pc.get("planet", "")
    ptype = pc.get("placement_type", "")
    pval = pc.get("placement_value", [])

    # Normalize planet name
    planet_norm = _normalize_planet_name(planet)

    # Skip compound/multi-planet rules that need conjunction detection
    # (we'll add conjunction checking later)
    if planet_norm in ("house_lord", "nodes", "general", "none", ""):
        return False, 0, None

    # Handle conjunction rules (e.g., "sun_moon", "mars_jupiter")
    if "_" in planet_norm and ptype in ("conjunction_in_house", "conjunction_condition",
                                         "multi_conjunction"):
        # Check if both/all planets are in the same house
        parts = planet_norm.split("_")
        if len(parts) == 2:
            h1 = _planet_house(chart, parts[0].title())
            h2 = _planet_house(chart, parts[1].title())
            if h1 > 0 and h2 > 0 and h1 == h2:
                if ptype == "conjunction_in_house":
                    # Check if they're in the specified house
                    target_house = pval[0] if pval else 0
                    if isinstance(target_house, int) and target_house == h1:
                        return True, h1, None
                    if not pval or not isinstance(pval[0] if pval else None, int):
                        return True, h1, None
                else:
                    return True, h1, None
        return False, 0, None

    # Sign placement rules
    if ptype == "sign_placement":
        target_sign = pval[0] if pval else ""
        if isinstance(target_sign, str):
            actual_sign = _planet_sign(chart, planet_norm.title())
            if actual_sign == target_sign.lower():
                # Determine house for this planet
                h = _planet_house(chart, planet_norm.title())
                return True, h, None
        return False, 0, None

    # House placement rules
    if ptype == "house_placement":
        target_house = pc.get("house", pval[0] if pval else 0)
        if isinstance(target_house, int) and target_house > 0:
            actual_house = _planet_house(chart, planet_norm.title())
            if actual_house == target_house:
                return True, target_house, None
        return False, 0, None

    # Sign condition / house condition (modifier rules)
    # These are supplementary/general rules — they modify base rules,
    # not standalone predictions. Skip for now; they'll be wired when
    # the modifier system is built.
    if ptype in ("sign_condition", "house_condition", "conjunction_condition"):
        return False, 0, None

    # Yoga rules — need dedicated yoga detection logic
    if ptype in ("yoga", "special"):
        return False, 0, None

    # Lagna-conditional rules (BVR)
    if ptype in ("house_placement",) and rule.lagna_scope:
        # Check if chart's lagna matches the rule's lagna_scope
        chart_lagna = chart.lagna_sign.lower()
        if chart_lagna not in rule.lagna_scope:
            return False, 0, None
        # Lagna matches — check house placement
        target_house = pc.get("house", pval[0] if pval else 0)
        if isinstance(target_house, int):
            actual_house = _planet_house(chart, planet_norm.title())
            if actual_house == target_house:
                return True, target_house, None
        return False, 0, None

    return False, 0, None


def _is_activated(rule, chart, dasha_context=None) -> bool:
    """Check if a rule is currently activated. Default: always active."""
    timing = getattr(rule, "timing_window", None)
    if not timing or timing.get("type") == "unspecified":
        return True
    return True


def evaluate_chart(chart) -> RuleFiringResult:
    """Evaluate all Phase 1B corpus rules against a chart.

    Returns a RuleFiringResult with fired rules, house summaries,
    and an ML-ready feature vector.
    """
    from src.corpus.combined_corpus import build_corpus

    corpus = build_corpus()
    phase1b_rules = [r for r in corpus.all() if r.phase.startswith("1B")]

    # Tier 3 Item 7: record corpus hash for model-corpus pinning
    try:
        from src.corpus.snapshot import corpus_hash
        c_hash = corpus_hash()
    except Exception:
        c_hash = ""

    result = RuleFiringResult(corpus_hash=c_hash)
    result.total_evaluated = len(phase1b_rules)

    for rule in phase1b_rules:
        if not _is_activated(rule, chart):
            result.skipped_rules.append(SkippedRule(rule_id=rule.rule_id, reason="not_activated"))
            continue
        fires, house, ctx = _check_rule_fires(rule, chart)
        if not fires:
            # Tier 3 Item 1: audit trail for skipped rules
            reason = "condition_not_met"
            pc = rule.primary_condition
            if not pc:
                reason = "no_conditions"
            elif not pc.get("conditions"):
                ptype = pc.get("placement_type", "")
                if ptype in ("yoga", "special", "sign_condition", "house_condition"):
                    reason = "unsupported_type"
            if hasattr(rule, "lagna_scope") and rule.lagna_scope:
                chart_lagna = getattr(chart, "lagna_sign", "").lower()
                if chart_lagna not in rule.lagna_scope:
                    reason = "lagna_scope_mismatch"
            result.skipped_rules.append(SkippedRule(
                rule_id=rule.rule_id, reason=reason,
            ))
            continue

        conc_count = len(rule.concordance_texts) if rule.concordance_texts else 0

        fired = FiredRule(
            rule_id=rule.rule_id,
            source=rule.source,
            planet=rule.primary_condition.get("planet", ""),
            house=house,
            outcome_direction=rule.outcome_direction,
            outcome_domains=rule.outcome_domains,
            confidence=rule.confidence,
            concordance_count=conc_count,
            # Tier 3 audit trail
            entity_target=getattr(rule, "entity_target", "native"),
            predictions=getattr(rule, "predictions", []),
            signal_group=getattr(rule, "signal_group", ""),
            health_sensitive=getattr(rule, "health_sensitive", False),
            context=ctx,
        )
        result.fired_rules.append(fired)

        # BB chain enrichment: derived_house_chains contribute to context
        if hasattr(rule, "derived_house_chains") and rule.derived_house_chains and ctx:
            from src.calculations.derived_house import resolve_house
            ctx.setdefault("aggregates", {})
            ctx["aggregates"].setdefault("bb_houses", [])
            ctx["aggregates"].setdefault("bb_strength", 0.0)
            for chain in rule.derived_house_chains:
                steps = chain if isinstance(chain, list) else [chain]
                current = steps[0].get("from", 1) if steps else 1
                for step in steps:
                    current = resolve_house(current, step.get("offset", 1))
                ctx["aggregates"]["bb_houses"].append(current)
                ctx["aggregates"]["bb_strength"] += 0.2

    result.total_fired = len(result.fired_rules)

    # Build house summaries
    for h in range(1, 13):
        house_rules = [r for r in result.fired_rules if r.house == h]
        if not house_rules:
            result.house_summary[h] = HouseRuleSummary(house=h)
            continue

        fav = sum(1 for r in house_rules if r.outcome_direction == "favorable")
        unfav = sum(1 for r in house_rules if r.outcome_direction == "unfavorable")
        mixed = sum(1 for r in house_rules if r.outcome_direction == "mixed")
        neutral = sum(1 for r in house_rules if r.outcome_direction == "neutral")
        mean_conf = sum(r.confidence for r in house_rules) / len(house_rules)
        sources = len({r.source for r in house_rules})
        conc_frac = sum(1 for r in house_rules if r.concordance_count > 0) / len(house_rules)

        if fav > unfav and fav > mixed:
            dominant = "favorable"
        elif unfav > fav and unfav > mixed:
            dominant = "unfavorable"
        elif mixed > 0:
            dominant = "mixed"
        else:
            dominant = "neutral"

        result.house_summary[h] = HouseRuleSummary(
            house=h,
            total_fired=len(house_rules),
            favorable_count=fav,
            unfavorable_count=unfav,
            mixed_count=mixed,
            neutral_count=neutral,
            mean_confidence=mean_conf,
            source_count=sources,
            concordance_score=conc_frac,
            dominant_direction=dominant,
        )

    return result
