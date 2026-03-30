"""
src/corpus/bphs_dignities_ext.py — BPHS Dignity Rules Extended (S225)

Encodes BPHS Ch.45-47: Planetary dignity effects beyond basic exaltation/
debilitation. Includes own-sign strength, moolatrikona, and dignity in
divisional charts.

Sources:
  BPHS Ch.45 — Exaltation and debilitation effects
  BPHS Ch.46 — Own sign and moolatrikona
  BPHS Ch.47 — Dignity combinations

20 rules. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_DIGNITIES_EXT_REGISTRY = CorpusRegistry()

_RULES = [
    RuleRecord(
        rule_id="DIG001",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="dignity",
        description=(
            "Exalted planet in kendra: exalted planet in angle houses "
            "(1/4/7/10) has maximum positive effect on its significations. "
            "Full strength for house and planet themes."
        ),
        confidence=0.95,
        verse="Ch.45 v.1-3",
        tags=["dignity", "exaltation", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG002",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="dignity",
        description=(
            "Exalted planet in trikona: exalted planet in trine (1/5/9) "
            "brings exceptional fortune and merit. Past-life credit made "
            "active through the exalted planet's domain."
        ),
        confidence=0.9,
        verse="Ch.45 v.4-6",
        tags=["dignity", "exaltation", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG003",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="dignity",
        description=(
            "Debilitated planet in kendra: debilitated planet in angle "
            "creates challenges for that house and planet's themes. "
            "Neecha Bhanga can cancel if lord in kendra."
        ),
        confidence=0.85,
        verse="Ch.45 v.7-9",
        tags=["dignity", "debilitation", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG004",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="dignity",
        description=(
            "Debilitated planet in dusthana (6/8/12): debilitated planet in "
            "dusthana has minimal negative impact on positive houses. "
            "The debilitation harms dusthana themes instead."
        ),
        confidence=0.655,
        verse="Ch.45 v.10-12",
        tags=["dignity", "debilitation", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG005",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="dignity",
        description=(
            "Sun exaltation (Aries 10°): Sun at maximum strength gives "
            "brilliant career, government connections, father's blessings, "
            "exceptional vitality."
        ),
        confidence=0.9,
        verse="Ch.45 v.13-14",
        tags=["dignity", "sun", "exaltation", "aries"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG006",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="dignity",
        description=(
            "Moon exaltation (Taurus 3°): Moon in maximum strength gives "
            "emotional stability, mother's strong support, excellent memory, "
            "public favor."
        ),
        confidence=0.9,
        verse="Ch.45 v.15-16",
        tags=["dignity", "moon", "exaltation", "taurus"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG007",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="dignity",
        description=(
            "Jupiter exaltation (Cancer 5°): Jupiter at maximum strength "
            "gives profound wisdom, multiple children, exceptional dharma, "
            "respected by society."
        ),
        confidence=0.9,
        verse="Ch.45 v.17-18",
        tags=["dignity", "jupiter", "exaltation", "cancer"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG008",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="dignity",
        description=(
            "Saturn exaltation (Libra 20°): Saturn in maximum strength gives "
            "disciplined wealth, delayed but lasting authority, ability to "
            "govern masses."
        ),
        confidence=0.9,
        verse="Ch.45 v.19-20",
        tags=["dignity", "saturn", "exaltation", "libra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG009",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="dignity",
        description=(
            "Moolatrikona sign: planet in moolatrikona is second only to "
            "exaltation in strength. Sun's moolatrikona is Leo 0-20°; "
            "Moon's is Taurus 4-20°."
        ),
        confidence=0.85,
        verse="Ch.46 v.1-4",
        tags=["dignity", "moolatrikona", "strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG010",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="dignity",
        description=(
            "Own sign strength: planet in its own sign gives strong "
            "expression of its natural qualities. Second after moolatrikona "
            "in dignity hierarchy: exalt > moolatrikona > own > friendly > neutral > enemy > debilitated."
        ),
        confidence=0.9,
        verse="Ch.46 v.5-8",
        tags=["dignity", "own_sign", "strength_hierarchy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG011",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="dignity",
        description=(
            "Planetary friendship: planet in a friendly sign has 50% of "
            "exaltation strength. Natural friends: Sun-Moon-Mars, "
            "Mercury-Venus, Jupiter-Sun-Moon, Saturn-Mercury-Venus."
        ),
        confidence=0.85,
        verse="Ch.46 v.9-12",
        tags=["dignity", "friendly_sign", "natural_friendship"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG012",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="dignity",
        description=(
            "Temporal friendship (tatkalik maitri): two planets in adjacent "
            "signs or mutually supportive positions become temporary friends, "
            "even natural enemies. Enhances temporary period effects."
        ),
        confidence=0.8,
        verse="Ch.46 v.13-15",
        tags=["dignity", "temporal_friendship", "tatkalik"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG013",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="dignity",
        description=(
            "Vargottama: planet in the same sign in both D1 and D9 (Navamsha). "
            "Greatly strengthened; especially powerful for Sun and Moon. "
            "Effects of the planet are stable and permanent."
        ),
        confidence=0.9,
        verse="Ch.47 v.1-4",
        tags=["dignity", "vargottama", "d9", "navamsha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG014",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="dignity",
        description=(
            "Pushkara Navamsha: specific degrees in each sign where planets "
            "in D9 receive special strength (pushkara). A planet in pushkara "
            "navamsha is unusually well-supported."
        ),
        confidence=0.8,
        verse="Ch.47 v.5-8",
        tags=["dignity", "pushkara", "navamsha", "d9"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG015",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="dignity",
        description=(
            "Combustion (Asta): planet within certain degrees of Sun is "
            "combust. Natural significations of the combust planet are "
            "suppressed. Degrees vary by planet."
        ),
        confidence=0.9,
        verse="Ch.47 v.9-12",
        tags=["dignity", "combustion", "combust", "sun"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG016",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="dignity",
        description=(
            "Retrograde planet: retrograde (vakra) motion gives a planet "
            "unusual strength in expression. Results may be delayed, reversed, "
            "or intensified compared to direct motion."
        ),
        confidence=0.85,
        verse="Ch.47 v.13-15",
        tags=["dignity", "retrograde", "vakra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG017",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="dignity",
        description=(
            "Planet in deep exaltation degree: planet exactly at peak "
            "exaltation degree (not just in exaltation sign) has maximum "
            "possible strength. Rare and exceptionally powerful."
        ),
        confidence=0.9,
        verse="Ch.47 v.16-18",
        tags=["dignity", "exaltation", "peak_exaltation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG018",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="dignity",
        description=(
            "Planet in deep debilitation degree: planet exactly at lowest "
            "debilitation degree (opposite of exaltation) has minimum "
            "strength. Most severe neecha effects."
        ),
        confidence=0.85,
        verse="Ch.47 v.19-21",
        tags=["dignity", "debilitation", "peak_debilitation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG019",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="dignity",
        description=(
            "Digbala (directional strength): Sun/Mars strong in H10; "
            "Jupiter/Mercury in H1; Moon/Venus in H4; Saturn in H7. "
            "Maximum directional strength when a planet is in its "
            "digbala house."
        ),
        confidence=0.9,
        verse="Ch.47 v.22-24",
        tags=["dignity", "digbala", "directional_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DIG020",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="dignity",
        description=(
            "Planetary war (graha yuddha): two visible planets within 1° "
            "conjunction. The planet with lower latitude wins; loser loses "
            "strength. Affects both planets' significations."
        ),
        confidence=0.85,
        verse="Ch.47 v.25-27",
        tags=["dignity", "graha_yuddha", "planetary_war"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_DIGNITIES_EXT_REGISTRY.add(_r)
