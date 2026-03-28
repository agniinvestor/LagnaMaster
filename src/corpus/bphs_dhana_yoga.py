"""
src/corpus/bphs_dhana_yoga.py — BPHS Dhana Yoga (Wealth Yoga) Rules (S224)

Encodes wealth-producing yogas from BPHS Ch.42-44.
Dhana Yogas involve the H1, H2, H5, H9, and H11 lords and their
connections, as well as Jupiter and Venus positions.

Sources:
  BPHS Ch.42 — Dhana Yoga (wealth accumulation rules)
  BPHS Ch.43 — Specific wealth combinations
  BPHS Ch.44 — Arishta Yoga (misfortune — inverse of Dhana)

25 rules. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_DHANA_YOGA_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Core Dhana Yoga — BPHS Ch.42 ─────────────────────────────────────────
    RuleRecord(
        rule_id="DY001",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Primary Dhana Yoga: lords of H1, H2, H5, H9, and H11 conjunct "
            "or mutually aspecting each other. Maximum combination of "
            "wealth houses. Exceptional financial prosperity."
        ),
        confidence=0.9,
        verse="Ch.42 v.1-4",
        tags=["yoga", "dhana_yoga", "wealth", "1st_lord", "2nd_lord", "5th_lord",
              "9th_lord", "11th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY002",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Dhana Yoga (H1+H2 lords): lagna lord and 2nd lord conjunct or "
            "in mutual aspect. Self-effort creates wealth; financial identity "
            "is core to the native."
        ),
        confidence=0.85,
        verse="Ch.42 v.5-7",
        tags=["yoga", "dhana_yoga", "wealth", "1st_lord", "2nd_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY003",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Dhana Yoga (H2+H11 lords): 2nd and 11th lords conjunct or "
            "mutually aspecting. Treasury (H2) and gains (H11) reinforce "
            "each other. Steady wealth accumulation."
        ),
        confidence=0.85,
        verse="Ch.42 v.8-10",
        tags=["yoga", "dhana_yoga", "wealth", "2nd_lord", "11th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY004",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Dhana Yoga (H5+H9 lords): two trikon lords together (fortune + "
            "merit). Wealth through dharma and intelligence. Excellent for "
            "academics, advisors, and philosophers."
        ),
        confidence=0.85,
        verse="Ch.42 v.11-13",
        tags=["yoga", "dhana_yoga", "wealth", "5th_lord", "9th_lord", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY005",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Jupiter as dhana karaka: Jupiter in H2 or H11 (or aspects H2/H11) "
            "strongly indicates wealth. Jupiter is the natural significator "
            "of wealth, children, and dharma."
        ),
        confidence=0.85,
        verse="Ch.42 v.14-16",
        tags=["yoga", "dhana_yoga", "jupiter", "2nd_house", "11th_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY006",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Venus as dhana karaka: Venus in H2 or H11 (or aspects H2/H11) "
            "indicates luxury wealth, beauty-based income. Venus enhances "
            "financial pleasures and accumulation."
        ),
        confidence=0.8,
        verse="Ch.42 v.17-19",
        tags=["yoga", "dhana_yoga", "venus", "2nd_house", "11th_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY007",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Mercury as dhana karaka: Mercury in H2 or H11 brings wealth "
            "through communication, trade, and business. Income from "
            "intellectual and commercial activities."
        ),
        confidence=0.8,
        verse="Ch.42 v.20-22",
        tags=["yoga", "dhana_yoga", "mercury", "2nd_house", "11th_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY008",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Sun in H11 — Dhana Yoga: Sun in the house of gains gives "
            "income through government, authority, or leadership. Father's "
            "wealth supports gains."
        ),
        confidence=0.8,
        verse="Ch.42 v.23-25",
        tags=["yoga", "dhana_yoga", "sun", "11th_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY009",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Moon in H2 or H11 — Dhana Yoga: Moon's positioning in wealth "
            "houses brings fluctuating but ultimately supportive wealth. "
            "Income through trade, public, or maternal sources."
        ),
        confidence=0.75,
        verse="Ch.42 v.26-28",
        tags=["yoga", "dhana_yoga", "moon", "2nd_house", "11th_house"],
        implemented=False,
    ),

    # ── Specific Wealth Combinations — BPHS Ch.43 ────────────────────────────
    RuleRecord(
        rule_id="DY010",
        source="BPHS",
        chapter="Ch.43",
        school="parashari",
        category="yoga",
        description=(
            "Indu Lagna Dhana: wealth seen from Indu Lagna (special wealth "
            "lagna based on 9th lord from lagna + 9th lord from Moon). "
            "Planets in kendra from Indu Lagna bring wealth."
        ),
        confidence=0.75,
        verse="Ch.43 v.1-5",
        tags=["yoga", "dhana_yoga", "indu_lagna", "wealth_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY011",
        source="BPHS",
        chapter="Ch.43",
        school="parashari",
        category="yoga",
        description=(
            "H2 lord in own sign or exaltation: 2nd lord at maximum strength "
            "gives strong family wealth and accumulated prosperity. Speech "
            "and knowledge sources of income."
        ),
        confidence=0.85,
        verse="Ch.43 v.6-8",
        tags=["yoga", "dhana_yoga", "2nd_lord", "exaltation", "own_sign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY012",
        source="BPHS",
        chapter="Ch.43",
        school="parashari",
        category="yoga",
        description=(
            "H11 lord in own sign or exaltation: 11th lord strong gives "
            "multiple income streams and desire-fulfillment. Gains from "
            "networks and investments are maximized."
        ),
        confidence=0.85,
        verse="Ch.43 v.9-11",
        tags=["yoga", "dhana_yoga", "11th_lord", "exaltation", "own_sign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY013",
        source="BPHS",
        chapter="Ch.43",
        school="parashari",
        category="yoga",
        description=(
            "H2 lord in H11 and H11 lord in H2 (parivartana): mutual exchange "
            "of wealth lords. Extremely powerful dhana yoga — wealth and gains "
            "continuously reinforce each other."
        ),
        confidence=0.9,
        verse="Ch.43 v.12-14",
        tags=["yoga", "dhana_yoga", "parivartana", "2nd_lord", "11th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY014",
        source="BPHS",
        chapter="Ch.43",
        school="parashari",
        category="yoga",
        description=(
            "Benefics in H2 and H11: natural benefics (Jupiter, Venus, "
            "Mercury, Moon) in wealth houses enhance financial outcomes. "
            "Each benefic in H2 or H11 adds to prosperity."
        ),
        confidence=0.8,
        verse="Ch.43 v.15-17",
        tags=["yoga", "dhana_yoga", "benefics", "2nd_house", "11th_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY015",
        source="BPHS",
        chapter="Ch.43",
        school="parashari",
        category="yoga",
        description=(
            "Malefics in H3/H6/H11 (upachaya): natural malefics in upachaya "
            "houses (3/6/10/11) give wealth through competition, struggle, "
            "and eventual triumph. 'Malefics thrive in upachaya.'"
        ),
        confidence=0.8,
        verse="Ch.43 v.18-20",
        tags=["yoga", "dhana_yoga", "malefics", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY016",
        source="BPHS",
        chapter="Ch.43",
        school="parashari",
        category="yoga",
        description=(
            "Dhana Yoga through dasha timing: wealth yoga activates "
            "in the dasha of the yoga-forming planet AND requires transit "
            "support (Jupiter transiting H2, H5, or H11 often triggers)."
        ),
        confidence=0.8,
        verse="Ch.43 v.21-23",
        tags=["yoga", "dhana_yoga", "dasha_timing", "transit_activation"],
        implemented=False,
    ),

    # ── Arishta Yoga (Misfortune — counterpart to wealth) — BPHS Ch.44 ───────
    RuleRecord(
        rule_id="DY017",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "Daridra Yoga (poverty yoga): lord of H6, H8, or H12 in H1 or "
            "H2, AND lagna lord weak. Financial adversity; chronic poverty "
            "or financial instability throughout life."
        ),
        confidence=0.8,
        verse="Ch.44 v.1-4",
        tags=["yoga", "arishta", "poverty", "dusthana_lord", "daridra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY018",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "H2 and H11 lords in dusthana (6/8/12): wealth lords placed in "
            "loss houses weakens financial prospects. Income disrupted by "
            "enemies, hidden losses, or foreign expenditure."
        ),
        confidence=0.8,
        verse="Ch.44 v.5-8",
        tags=["yoga", "arishta", "wealth_loss", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY019",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "Malefics in H2 (Saturn, Mars, Rahu/Ketu): malefics in the wealth "
            "house afflict speech, family, and accumulation. Wealth obtained "
            "with difficulty or through unethical means."
        ),
        confidence=0.8,
        verse="Ch.44 v.9-11",
        tags=["yoga", "arishta", "malefics", "2nd_house", "wealth_affliction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY020",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "H2 lord combust: 2nd lord too close to Sun (combust) loses "
            "strength; wealth house lord unable to protect treasury. "
            "Financial setbacks during Sun periods."
        ),
        confidence=0.75,
        verse="Ch.44 v.12-14",
        tags=["yoga", "arishta", "combust", "2nd_lord", "wealth_reduction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY021",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "Kubera Yoga: lord of H2 in H9, AND H9 lord in H2, AND Jupiter "
            "strong. Native becomes extremely wealthy through dharmic means. "
            "Godlike financial prosperity."
        ),
        confidence=0.8,
        verse="Ch.44 v.15-17",
        tags=["yoga", "dhana_yoga", "kubera", "2nd_lord", "9th_lord", "jupiter"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY022",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "Vasumati Yoga: benefics in upachaya (3/6/10/11) from both "
            "lagna and Moon. Native is wealthy without much effort, "
            "through fortunate positioning."
        ),
        confidence=0.8,
        verse="Ch.44 v.18-20",
        tags=["yoga", "dhana_yoga", "vasumati", "benefics", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY023",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "Chandra-Shukra Dhana Yoga: Moon and Venus conjunct or mutually "
            "aspecting. Wealth through arts, fashion, beauty, trade, or "
            "maternal sources."
        ),
        confidence=0.75,
        verse="Ch.44 v.21-23",
        tags=["yoga", "dhana_yoga", "moon", "venus", "chandra_shukra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY024",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "Guru-Shukra Dhana Yoga: Jupiter and Venus conjunct or in mutual "
            "aspect. Exceptional wealth through religious, artistic, or "
            "advisory professions."
        ),
        confidence=0.8,
        verse="Ch.44 v.24-26",
        tags=["yoga", "dhana_yoga", "jupiter", "venus", "guru_shukra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DY025",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "Shakata Yoga: Moon in H12 or H8 or H6 from Jupiter. Native "
            "faces ups and downs, wheel of fortune. Prosperity comes and "
            "goes; emotional instability affects wealth."
        ),
        confidence=0.75,
        verse="Ch.44 v.27-29",
        tags=["yoga", "moon", "jupiter", "shakata", "fluctuating_wealth"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_DHANA_YOGA_REGISTRY.add(_r)
