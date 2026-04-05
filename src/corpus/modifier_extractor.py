"""src/corpus/modifier_extractor.py — Extract modifiers from rule descriptions.

Applied at build time by combined_corpus.py.
Parses conditional language into structured modifier dicts.
"""
from __future__ import annotations
import re

# Patterns are matched against LOWERCASED description text.
# More specific patterns MUST come before general ones.
_MODIFIER_PATTERNS = [
    # ── Single-word dignity (missed by phrase patterns) ──────────────────
    (r"^exalted$", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "exalted"}], "effect": "amplifies", "target": "prediction", "strength": "strong"}),
    (r"^debilitated$", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "debilitated"}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"^in fall$|^in_fall$", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "debilitated"}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"^in moolatrikona$|^in_moolatrikona$", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "moolatrikona"}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),
    (r"in deep exaltation", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "exalted"}], "effect": "amplifies", "target": "prediction", "strength": "strong"}),

    # ── OR-dignity collapses ─────────────────────────────────────────────
    (r"with benefic or in own house or exalted", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "strong"}], "effect": "amplifies", "target": "prediction", "strength": "strong"}),
    (r"in own sign or exalted|own_sign_or_exalted", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "strong"}], "effect": "amplifies", "target": "prediction", "strength": "strong"}),
    (r"not in own or exaltation|not_in_own_or_exaltation", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "debilitated"}], "effect": "negates", "target": "prediction", "strength": "medium"}),
    (r"in fall or combustion|fall_or_combustion", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "debilitated"}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"debilitated or in enemy|debilitated_or_in_enemy", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "debilitated"}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"exalted or conjunct.*benefic|exalted_or_conjunct.*benefic", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "strong"}], "effect": "amplifies", "target": "prediction", "strength": "strong"}),

    # ── Moon phase ───────────────────────────────────────────────────────
    (r"waxing or bright|waxing_or_bright", lambda m: {"condition": [{"type": "moon_phase", "phase": "waxing"}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),
    (r"waning or afflicted|waning_or_afflicted", lambda m: {"condition": [{"type": "moon_phase", "phase": "waning"}], "effect": "negates", "target": "prediction", "strength": "medium"}),
    (r"waxing moon|full moon", lambda m: {"condition": [{"type": "moon_phase", "phase": "waxing"}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),
    (r"waning moon|new moon|dark moon", lambda m: {"condition": [{"type": "moon_phase", "phase": "waning"}], "effect": "negates", "target": "prediction", "strength": "medium"}),

    # ── Strength patterns ────────────────────────────────────────────────
    (r"planet with strength|with_strength|endowed with strength", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "strong"}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),
    (r"without strength|devoid of strength|bereft of strength", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "debilitated"}], "effect": "negates", "target": "prediction", "strength": "medium"}),

    # ── Affliction / benefic aspect patterns ─────────────────────────────
    (r"afflicted by natural malefic|afflicted_by_natural_malefics", lambda m: {"condition": [{"type": "planet_aspecting", "planet": "any_malefic", "house": "self"}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"no benefic aspect received|no_benefic_aspect_received", lambda m: {"condition": [{"type": "planet_not_aspecting", "planet": "any_benefic", "house": "self"}], "effect": "negates", "target": "prediction", "strength": "medium"}),

    # ── Conjunction OR aspect (pick aspect as superset) ──────────────────
    (r"conjunct or aspected by natural benefics", lambda m: {"condition": [{"type": "planet_aspecting", "planet": "any_benefic", "house": "self"}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),
    (r"conjunct or aspected by natural malefics", lambda m: {"condition": [{"type": "planet_aspecting", "planet": "any_malefic", "house": "self"}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"conjunct or aspected by (\w+)", lambda m: {"condition": [{"type": "planet_aspecting", "planet": m.group(1).title(), "house": "self"}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),

    # ── Aspect patterns (general — must come after conjunction-or-aspect) ─
    (r"aspected by natural benefic", lambda m: {"condition": [{"type": "planet_aspecting", "planet": "any_benefic", "house": "self"}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),
    (r"aspected by natural malefic", lambda m: {"condition": [{"type": "planet_aspecting", "planet": "any_malefic", "house": "self"}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"malefic aspect|aspected by malefic", lambda m: {"condition": [{"type": "planet_aspecting", "planet": "any_malefic", "house": "self"}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"benefic aspect|aspected by benefic", lambda m: {"condition": [{"type": "planet_aspecting", "planet": "any_benefic", "house": "self"}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),
    (r"aspected by (\w+)", lambda m: {"condition": [{"type": "planet_aspecting", "planet": m.group(1).title(), "house": "self"}], "effect": "qualifies", "target": "prediction", "strength": "strong"}),
    (r"aspect of (\w+)", lambda m: {"condition": [{"type": "planet_aspecting", "planet": m.group(1).title(), "house": "self"}], "effect": "qualifies", "target": "prediction", "strength": "strong"}),

    # ── Conjunction patterns (must come after conjunction-or-aspect) ──────
    (r"conjunct natural malefic|conjunct_natural_malefic", lambda m: {"condition": [{"type": "planets_conjunct", "planets": ["trigger", "any_malefic"]}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"conjunct natural benefic", lambda m: {"condition": [{"type": "planets_conjunct", "planets": ["trigger", "any_benefic"]}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),
    (r"conjunct malefic$|conjunct_malefic$", lambda m: {"condition": [{"type": "planets_conjunct", "planets": ["trigger", "any_malefic"]}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"conjunct (\w+)$", lambda m: {"condition": [{"type": "planets_conjunct", "planets": ["trigger", m.group(1).title()]}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),

    # ── Dignity phrases (existing, now with target) ──────────────────────
    (r"if exalted|when exalted", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "exalted"}], "effect": "amplifies", "target": "prediction", "strength": "strong"}),
    (r"if debilitated|when debilitated", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "debilitated"}], "effect": "negates", "target": "prediction", "strength": "strong"}),
    (r"in own sign|own house", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "own_sign"}], "effect": "amplifies", "target": "prediction", "strength": "medium"}),
    (r"combust|combustion", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "debilitated"}], "effect": "negates", "target": "prediction", "strength": "medium"}),
    (r"retrograde", lambda m: {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "retrograde"}], "effect": "qualifies", "target": "prediction", "strength": "medium"}),
]

_EXCEPTION_PATTERNS = [
    r"unless (\w[\w ]*)",
    r"except when",
    r"cancell?ation|cancelled if",
    r"negated by",
    r"neecha bhanga",
]


def extract_modifiers_from_description(description: str) -> tuple[list[dict], list[str]]:
    """Extract structured modifiers and exceptions from a rule description.

    Returns (modifiers: list[dict], exceptions: list[str]).
    """
    desc = description.lower()
    modifiers: list[dict] = []
    exceptions: list[str] = []

    for pattern, builder in _MODIFIER_PATTERNS:
        match = re.search(pattern, desc)
        if match:
            mod = builder(match)
            if mod not in modifiers:
                modifiers.append(mod)

    for pattern in _EXCEPTION_PATTERNS:
        match = re.search(pattern, desc)
        if match:
            exc = match.group(0).strip()
            if exc not in exceptions:
                exceptions.append(exc)

    return modifiers, exceptions
