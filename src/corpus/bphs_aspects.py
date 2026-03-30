"""
src/corpus/bphs_aspects.py — BPHS Aspect Rules (S226)

Encodes planetary aspect rules from BPHS Ch.48-50.
Includes special aspects of Mars/Saturn/Jupiter and aspect effects.

Sources:
  BPHS Ch.48 — Graha Drishti (planetary aspects)
  BPHS Ch.49 — Special aspect effects
  BPHS Ch.50 — Rashi aspects (sign aspects)

20 rules. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_ASPECTS_REGISTRY = CorpusRegistry()

_RULES = [
    RuleRecord(
        rule_id="ASP001",
        source="BPHS",
        chapter="Ch.48",
        school="parashari",
        category="aspect",
        description=(
            "All planets aspect 7th house from their position (full 7th aspect). "
            "This is the universal full-strength aspect. Two planets 180° apart "
            "fully aspect each other."
        ),
        confidence=0.95,
        verse="Ch.48 v.1-3",
        tags=["aspect", "7th_aspect", "full_aspect", "universal"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP002",
        source="BPHS",
        chapter="Ch.48",
        school="parashari",
        category="aspect",
        description=(
            "Jupiter special aspects: Jupiter aspects 5th and 9th from its "
            "position (in addition to 7th). These are ¾ strength aspects. "
            "Jupiter's 5th/9th aspects are highly auspicious."
        ),
        confidence=0.95,
        verse="Ch.48 v.4-6",
        tags=["aspect", "jupiter", "5th_aspect", "9th_aspect", "special_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP003",
        source="BPHS",
        chapter="Ch.48",
        school="parashari",
        category="aspect",
        description=(
            "Saturn special aspects: Saturn aspects 3rd and 10th from its "
            "position (in addition to 7th). ¾ strength aspects. Saturn's "
            "3rd/10th aspects add discipline or obstruction."
        ),
        confidence=0.95,
        verse="Ch.48 v.7-9",
        tags=["aspect", "saturn", "3rd_aspect", "10th_aspect", "special_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP004",
        source="BPHS",
        chapter="Ch.48",
        school="parashari",
        category="aspect",
        description=(
            "Mars special aspects: Mars aspects 4th and 8th from its position "
            "(in addition to 7th). ¾ strength aspects. Mars' 4th/8th aspects "
            "bring energy, conflict, or accidents to those houses."
        ),
        confidence=0.95,
        verse="Ch.48 v.10-12",
        tags=["aspect", "mars", "4th_aspect", "8th_aspect", "special_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP005",
        source="BPHS",
        chapter="Ch.48",
        school="parashari",
        category="aspect",
        description=(
            "Benefic aspect on dusthana: Jupiter or Venus aspecting H6, H8, "
            "or H12 reduces the negative effects of those houses. Illness, "
            "longevity, and loss are moderated."
        ),
        confidence=0.85,
        verse="Ch.48 v.13-15",
        tags=["aspect", "benefic", "dusthana", "protection"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP006",
        source="BPHS",
        chapter="Ch.48",
        school="parashari",
        category="aspect",
        description=(
            "Malefic aspect on trikona: Saturn or Mars aspecting H1, H5, or "
            "H9 restricts positive outcomes of those houses. Fortune, "
            "intelligence, or self may be burdened."
        ),
        confidence=0.85,
        verse="Ch.48 v.16-18",
        tags=["aspect", "malefic", "trikona", "restriction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP007",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="aspect",
        description=(
            "Jupiter aspect on Moon: Jupiter aspecting Moon gives emotional "
            "stability, wisdom, and protection from mental distress. "
            "Counteracts Kemadruma and afflictions."
        ),
        confidence=0.9,
        verse="Ch.49 v.1-3",
        tags=["aspect", "jupiter", "moon", "emotional_stability"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP008",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="aspect",
        description=(
            "Jupiter aspect on lagna: Jupiter aspecting H1 protects health, "
            "gives wisdom, and brings good fortune to the personality. "
            "One of the most protective single aspects."
        ),
        confidence=0.9,
        verse="Ch.49 v.4-6",
        tags=["aspect", "jupiter", "lagna", "protection"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP009",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="aspect",
        description=(
            "Saturn aspect on H4: Saturn aspecting the 4th house restricts "
            "domestic happiness, may separate native from mother. Property "
            "gained late or with difficulty."
        ),
        confidence=0.85,
        verse="Ch.49 v.7-9",
        tags=["aspect", "saturn", "4th_house", "domestic_restriction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP010",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="aspect",
        description=(
            "Mars aspect on H7: Mars aspecting the 7th house can indicate "
            "marital tension, aggressive partner, or separation. Mangal dosha "
            "principle: Mars in H1/4/7/8/12 aspects H7."
        ),
        confidence=0.85,
        verse="Ch.49 v.10-12",
        tags=["aspect", "mars", "7th_house", "mangal_dosha", "marriage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP011",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="aspect",
        description=(
            "Venus aspect on lagna: Venus aspecting H1 gives beauty, charm, "
            "artistic ability, and comfort-seeking personality. "
            "Enhances social attractiveness."
        ),
        confidence=0.85,
        verse="Ch.49 v.13-15",
        tags=["aspect", "venus", "lagna", "beauty", "charm"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP012",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="aspect",
        description=(
            "Sun aspect on H10: Sun aspecting the 10th house (3rd aspect or "
            "7th aspect from H4) enhances career authority and government "
            "connections. Professional ambition energized."
        ),
        confidence=0.8,
        verse="Ch.49 v.16-18",
        tags=["aspect", "sun", "10th_house", "career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP013",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="aspect",
        description=(
            "Rahu/Ketu shadow aspects: Rahu and Ketu have no formal special "
            "aspects but their conjunction with a planet amplifies that "
            "planet's effects — both positive and disruptive."
        ),
        confidence=0.8,
        verse="Ch.49 v.19-21",
        tags=["aspect", "rahu", "ketu", "conjunction_effect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP014",
        source="BPHS",
        chapter="Ch.50",
        school="parashari",
        category="aspect",
        description=(
            "Rashi (sign) aspects: Cardinal signs (Aries, Cancer, Libra, "
            "Capricorn) aspect each other fully. Fixed signs aspect each "
            "other. Dual signs aspect each other (Jaimini principle)."
        ),
        confidence=0.8,
        verse="Ch.50 v.1-4",
        tags=["aspect", "rashi_aspect", "sign_aspect", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP015",
        source="BPHS",
        chapter="Ch.50",
        school="parashari",
        category="aspect",
        description=(
            "Aspect strength by distance: the 7th house aspect is full "
            "strength (100%). 5th/9th aspects of Jupiter are ¾ strength (75%). "
            "3rd/10th aspects of Saturn and 4th/8th of Mars are ¾ strength."
        ),
        confidence=0.85,
        verse="Ch.50 v.5-8",
        tags=["aspect", "aspect_strength", "grading"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP016",
        source="BPHS",
        chapter="Ch.50",
        school="parashari",
        category="aspect",
        description=(
            "Aspect modification by dignity: exalted planet's aspect is more "
            "beneficial; debilitated planet's aspect is weaker. Aspects carry "
            "the planet's current dignity into the aspected house."
        ),
        confidence=0.85,
        verse="Ch.50 v.9-11",
        tags=["aspect", "dignity_modification", "exaltation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP017",
        source="BPHS",
        chapter="Ch.50",
        school="parashari",
        category="aspect",
        description=(
            "Mutual aspect between planets: two planets in exact 7th aspect "
            "form a conjunction-like connection. Their energies strongly "
            "interact for the period when both are in same axis."
        ),
        confidence=0.85,
        verse="Ch.50 v.12-14",
        tags=["aspect", "mutual_aspect", "opposition"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP018",
        source="BPHS",
        chapter="Ch.50",
        school="parashari",
        category="aspect",
        description=(
            "Graha drishti vs. rashi drishti: graha (planetary) aspects are "
            "about specific planet energy; rashi (sign) aspects reflect the "
            "natural sign relationships used in Jaimini analysis."
        ),
        confidence=0.655,
        verse="Ch.50 v.15-17",
        tags=["aspect", "graha_drishti", "rashi_drishti", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP019",
        source="BPHS",
        chapter="Ch.50",
        school="parashari",
        category="aspect",
        description=(
            "Parivartana and aspects: when two planets exchange signs, they "
            "also effectively aspect the other's house. Exchange strengthens "
            "both houses AND the aspect between them."
        ),
        confidence=0.8,
        verse="Ch.50 v.18-20",
        tags=["aspect", "parivartana", "exchange"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="ASP020",
        source="BPHS",
        chapter="Ch.50",
        school="parashari",
        category="aspect",
        description=(
            "Argala (intervention): planets in H2, H4, H11, H5 from any "
            "planet or house form an 'argala' (bolting pin effect). "
            "Argala strengthens or blocks the aspected house's results."
        ),
        confidence=0.8,
        verse="Ch.50 v.21-24",
        tags=["aspect", "argala", "intervention", "house_strengthening"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_ASPECTS_REGISTRY.add(_r)
