"""
src/calculations/school_rules.py
School-restriction declarations for LagnaMaster scoring rules.
Session 186 (Audit I-B).

Every scoring rule (R01-R22) is tagged with the school tradition it belongs to.
This resolves the school-mixing problem identified in Audit I-B:

  Sanjay Rath · Crux of Vedic Astrology, Preface:
  "One cannot mix systems. The moment you use a Jaimini concept in a
   Parashari context without declaring the school switch, you have
   left both traditions."

RULE SCHOOL ASSIGNMENTS:
  R01-R16, R19-R22 → "parashari"   (standard BPHS Parashari analysis)
  R17, R18         → "jaimini"     (Sthir Karak = Jaimini fixed significator concept)

Note on R17/R18: The Sthir Karak (fixed significator) is a Jaimini concept.
In strict Parashari mode, Sun = significator of Soul/father, Moon = mind/mother,
Mars = siblings, Mercury = friends/education, Jupiter = children/wisdom, Venus =
wife/desires, Saturn = longevity/sorrow — these are BPHS fixed significations
(naisargika karakatva), NOT Jaimini Sthir Karakas. The scoring rules R17/R18
as currently implemented use Jaimini-style assignments and should only fire in
Jaimini or mixed-school mode.

Source: PVRNR · BPHS Ch.32 (naisargika karakatva) vs Jaimini Sutras Adhyaya 1
        Pada 4 (Sthira Karakas). The distinction is systematically documented in
        Sanjay Rath · Crux of Vedic Astrology Ch.3.
"""

from __future__ import annotations

# Canonical school tags
PARASHARI = "parashari"
JAIMINI = "jaimini"
TAJIKA = "tajika"
KP = "kp"
ANY = "any"  # fires regardless of school

# Rule → school mapping
# R01-R22 are LagnaMaster's house scoring rules
SCHOOL_RULE_MAP: dict[str, str] = {
    "R01": PARASHARI,  # Gentle sign (trine/angle) in house
    "R02": PARASHARI,  # Functional benefic in house
    "R03": PARASHARI,  # Functional benefic aspects house
    "R04": PARASHARI,  # Bhavesh in Kendra/Trikona
    "R05": PARASHARI,  # Bhavesh with Kendra/Trikona lord
    "R06": PARASHARI,  # Bhavesh with functional benefic
    "R07": PARASHARI,  # Functional benefic aspects Bhavesh sign
    "R08": PARASHARI,  # Bhavesh in Shubh Kartari
    "R09": PARASHARI,  # Functional malefic in house
    "R10": PARASHARI,  # Functional malefic aspects house
    "R11": PARASHARI,  # Dusthana lord in house
    "R12": PARASHARI,  # House in Paap Kartari
    "R13": PARASHARI,  # Bhavesh with functional malefic
    "R14": PARASHARI,  # Functional malefic aspects Bhavesh
    "R15": PARASHARI,  # Bhavesh in Dusthana
    "R16": PARASHARI,  # Bhavesh with Dusthana lord
    "R17": JAIMINI,  # Sthir Karak in Kendra/Trikona (Jaimini fixed significator)
    "R18": JAIMINI,  # Sthir Karak in Dusthana (Jaimini fixed significator)
    "R19": PARASHARI,  # Bhavesh combust
    "R20": PARASHARI,  # Bhavesh in Dig Bala house
    "R21": PARASHARI,  # Bhavesh Pada in Pushkara Navamsha
    "R22": PARASHARI,  # Bhavesh retrograde
}

# School compatibility: which schools allow which rule traditions
# strict=True: only exact match passes
# strict=False: parashari mode allows "any"; jaimini mode allows parashari rules too
SCHOOL_ALLOWS: dict[str, set[str]] = {
    PARASHARI: {PARASHARI, ANY},
    JAIMINI: {PARASHARI, JAIMINI, ANY},  # Jaimini analysis includes Parashari base
    KP: {PARASHARI, ANY},  # KP is Parashari-derived
    TAJIKA: {PARASHARI, ANY},  # Tajika uses Parashari planetary base
}

SCHOOL_ALLOWS_STRICT: dict[str, set[str]] = {
    PARASHARI: {PARASHARI, ANY},
    JAIMINI: {JAIMINI, ANY},
    KP: {KP, ANY},
    TAJIKA: {TAJIKA, ANY},
}


def get_rule_school(rule_id: str) -> str:
    """Return the school tag for a given rule identifier (e.g. 'R17')."""
    return SCHOOL_RULE_MAP.get(rule_id, PARASHARI)


def is_rule_active(rule_id: str, school: str, strict: bool = False) -> bool:
    """
    Return True if the rule should fire given the declared school.

    Args:
        rule_id: e.g. "R17"
        school:  e.g. "parashari", "jaimini", "kp"
        strict:  if True, Jaimini rules never fire in Parashari mode and vice versa

    Examples:
        is_rule_active("R17", "parashari", strict=True)  → False
        is_rule_active("R17", "parashari", strict=False) → True (current default)
        is_rule_active("R17", "jaimini",   strict=True)  → True
        is_rule_active("R01", "jaimini",   strict=True)  → False (Parashari-only)
    """
    rule_school = get_rule_school(rule_id)
    if strict:
        allowed = SCHOOL_ALLOWS_STRICT.get(school, {PARASHARI, ANY})
    else:
        allowed = SCHOOL_ALLOWS.get(school, {PARASHARI, ANY})
    return rule_school in allowed


def filter_rules_by_school(
    rules: list,
    school: str,
    strict: bool = False,
) -> list:
    """
    Filter a list of RuleResult objects to those active in the given school.

    Args:
        rules:   list of RuleResult (must have .rule attribute, e.g. "R17")
        school:  "parashari" | "jaimini" | "kp" | "tajika"
        strict:  if True, enforce hard school boundaries

    Returns: filtered list of RuleResult

    Source: Sanjay Rath · Crux of Vedic Astrology, Preface
    """
    return [r for r in rules if is_rule_active(getattr(r, "rule", ""), school, strict)]


def get_jaimini_rules() -> list[str]:
    """Return list of rule IDs classified as Jaimini school."""
    return [rid for rid, school in SCHOOL_RULE_MAP.items() if school == JAIMINI]


def get_parashari_rules() -> list[str]:
    """Return list of rule IDs classified as Parashari school."""
    return [rid for rid, school in SCHOOL_RULE_MAP.items() if school == PARASHARI]


def school_score_adjustment(
    raw_score: float,
    rules: list,
    school: str,
    strict: bool = False,
) -> float:
    """
    Re-compute raw score excluding rules not active in the given school.

    This is the correction function to call when strict_school=True:
    it deducts contributions from rules that should not fire in this school.

    Args:
        raw_score: already-computed raw score (sum of all rule contributions)
        rules:     list of RuleResult with .rule and .score attributes
        school:    active school
        strict:    True to enforce hard school boundaries

    Returns: corrected score (same as raw_score when strict=False)
    """
    if not strict:
        return raw_score

    # Deduct contributions of rules that should not fire in this school
    deduction = sum(
        getattr(r, "score", 0.0)
        for r in rules
        if not is_rule_active(getattr(r, "rule", ""), school, strict=True)
    )
    return raw_score - deduction
