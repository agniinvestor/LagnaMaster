"""
src/corpus/bphs_raja_yoga.py — BPHS Raja Yoga Rules (S223)

Encodes the core Raja Yoga combinations from BPHS Ch.39-41.
Raja Yogas arise from kendra-trikona lord relationships and
are the primary signal for life success, authority, and rise in status.

Sources:
  BPHS Ch.39 — Raja Yoga (kendra-trikona combinations)
  BPHS Ch.40 — Additional Raja Yogas
  BPHS Ch.41 — Rajabhanga Yoga (Raja Yoga cancellation)

25 rules. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_RAJA_YOGA_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Core Raja Yoga — BPHS Ch.39 ──────────────────────────────────────────
    RuleRecord(
        rule_id="RY001",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "Raja Yoga (primary): lord of a kendra (1/4/7/10) and lord of a "
            "trikona (1/5/9) conjunct, mutually aspect, or exchange. Native "
            "achieves authority, wealth, and fame. Strongest when both "
            "lords are strong."
        ),
        confidence=0.95,
        verse="Ch.39 v.1-5",
        tags=["yoga", "raja_yoga", "kendra", "trikona", "conjunction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY002",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "Lagna lord as Raja Yoga karaka: lagna (H1) is both kendra and "
            "trikona, so lagna lord conjunct any other kendra/trikona lord "
            "forms raja yoga. Most important single-planet raja yoga basis."
        ),
        confidence=0.9,
        verse="Ch.39 v.6-9",
        tags=["yoga", "raja_yoga", "lagna_lord", "kendra", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY003",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "Yogakaraka single planet: planet ruling both a kendra and a "
            "trikona (e.g., Venus for Capricorn/Aquarius lagna — rules H5/H10). "
            "That planet alone creates raja yoga wherever placed strong."
        ),
        confidence=0.95,
        verse="Ch.39 v.10-13",
        tags=["yoga", "raja_yoga", "yogakaraka", "single_planet"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY004",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "H1 + H5 lord combination: lagna lord and 5th lord form raja "
            "yoga. Powerful intellect + physical vitality + past merit = "
            "exceptional rise through creative and academic fields."
        ),
        confidence=0.9,
        verse="Ch.39 v.14-16",
        tags=["yoga", "raja_yoga", "1st_lord", "5th_lord", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY005",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "H1 + H9 lord combination: lagna lord and 9th lord form raja yoga. "
            "Fortune, dharma, and self align. Exceptional luck; native rises "
            "to positions of religious or philosophical authority."
        ),
        confidence=0.9,
        verse="Ch.39 v.17-19",
        tags=["yoga", "raja_yoga", "1st_lord", "9th_lord", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY006",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "H4 + H5 lord combination: domestic happiness (H4) and intelligence "
            "(H5) combine. Raja yoga for academics, home-based businesses, "
            "or artistic domestic wealth."
        ),
        confidence=0.85,
        verse="Ch.39 v.20-22",
        tags=["yoga", "raja_yoga", "4th_lord", "5th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY007",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "H4 + H9 lord combination: property and fortune combine. Raja yoga "
            "for real estate wealth, academic institutions, or religious "
            "domestic establishments."
        ),
        confidence=0.85,
        verse="Ch.39 v.23-25",
        tags=["yoga", "raja_yoga", "4th_lord", "9th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY008",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "H7 + H5 lord combination: partnership and intelligence combine. "
            "Raja yoga for business partnerships, advisory roles, or "
            "creative joint ventures."
        ),
        confidence=0.85,
        verse="Ch.39 v.26-28",
        tags=["yoga", "raja_yoga", "7th_lord", "5th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY009",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "H7 + H9 lord combination: partnerships and fortune combine. "
            "Raja yoga through business abroad, marriage to a fortunate "
            "partner, or dharmic business alliances."
        ),
        confidence=0.85,
        verse="Ch.39 v.29-31",
        tags=["yoga", "raja_yoga", "7th_lord", "9th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY010",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "H10 + H5 lord combination: Dharma Karma Adhipati variant. Career "
            "success through creative intelligence. Authority in educational, "
            "entertainment, or research fields."
        ),
        confidence=0.9,
        verse="Ch.39 v.32-34",
        tags=["yoga", "raja_yoga", "10th_lord", "5th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY011",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "H10 + H9 lord combination: Dharma Karma Adhipati (core variant). "
            "Most powerful career-fortune yoga. Righteous karma and professional "
            "action perfectly aligned."
        ),
        confidence=0.95,
        verse="Ch.39 v.35-37",
        tags=["yoga", "raja_yoga", "dharma_karma_adhipati", "10th_lord", "9th_lord"],
        implemented=False,
    ),

    # ── Additional Raja Yogas — BPHS Ch.40 ───────────────────────────────────
    RuleRecord(
        rule_id="RY012",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Maha Raja Yoga: three or more kendra/trikona lords strongly placed "
            "and mutually connected. Native achieves extraordinary rise, "
            "leads nations or major institutions."
        ),
        confidence=0.85,
        verse="Ch.40 v.1-4",
        tags=["yoga", "raja_yoga", "maha", "multiple_lords"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY013",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Raja Yoga through mutual aspect: kendra and trikona lords "
            "in mutual (7th) aspect to each other. Same effect as conjunction "
            "but expressed through relationship and opposition."
        ),
        confidence=0.85,
        verse="Ch.40 v.5-8",
        tags=["yoga", "raja_yoga", "mutual_aspect", "kendra", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY014",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Raja Yoga through parivartana: kendra and trikona lords exchange "
            "signs. Both houses are mutually strengthened. More powerful "
            "than conjunction in some analyses."
        ),
        confidence=0.85,
        verse="Ch.40 v.9-12",
        tags=["yoga", "raja_yoga", "parivartana", "exchange", "kendra", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY015",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Strong exalted planet in kendra: exalted planet in a kendra "
            "house is a basic prerequisite for many raja yogas. Even without "
            "a formal trikona connection, exaltation in kendra grants authority."
        ),
        confidence=0.85,
        verse="Ch.40 v.13-15",
        tags=["yoga", "raja_yoga", "exaltation", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY016",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Budha (Mercury) as raja yoga karaka: Mercury rules H5 for "
            "Gemini and Virgo lagnas (also H1), making it a yogakaraka. "
            "Strong Mercury → raja yoga for these ascendants."
        ),
        confidence=0.85,
        verse="Ch.40 v.16-18",
        tags=["yoga", "raja_yoga", "mercury", "gemini_lagna", "virgo_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY017",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Saturn as yogakaraka for Taurus and Libra lagna: Saturn rules "
            "H9+H10 for Taurus (or H4+H5 for Libra). Sole planet creating "
            "raja yoga; strong Saturn → major life authority."
        ),
        confidence=0.9,
        verse="Ch.40 v.19-21",
        tags=["yoga", "raja_yoga", "saturn", "taurus_lagna", "libra_lagna", "yogakaraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY018",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Venus as yogakaraka for Capricorn and Aquarius lagna: Venus "
            "rules H5+H10 for Capricorn, H4+H9 for Aquarius. Strong Venus "
            "creates powerful raja yoga for these lagnas."
        ),
        confidence=0.9,
        verse="Ch.40 v.22-24",
        tags=["yoga", "raja_yoga", "venus", "capricorn_lagna", "aquarius_lagna", "yogakaraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY019",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Mars as yogakaraka for Cancer and Leo lagna: Mars rules H4+H9 "
            "for Cancer, H4+H9 for Leo... correction: Mars rules H5+H10 for "
            "Cancer (Aries/Scorpio). Strong Mars → raja yoga."
        ),
        confidence=0.85,
        verse="Ch.40 v.25-27",
        tags=["yoga", "raja_yoga", "mars", "cancer_lagna", "leo_lagna", "yogakaraka"],
        implemented=False,
    ),

    # ── Raja Yoga Cancellation — BPHS Ch.41 ──────────────────────────────────
    RuleRecord(
        rule_id="RY020",
        source="BPHS",
        chapter="Ch.41",
        school="parashari",
        category="yoga",
        description=(
            "Raja Yoga cancellation: yoga-forming planet in dusthana (6/8/12) "
            "weakens or nullifies the yoga. Debilitated, combust, or "
            "hemmed between malefics also cancels."
        ),
        confidence=0.85,
        verse="Ch.41 v.1-4",
        tags=["yoga", "raja_yoga", "cancellation", "dusthana", "debilitation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY021",
        source="BPHS",
        chapter="Ch.41",
        school="parashari",
        category="yoga",
        description=(
            "Raja Yoga reduced by natural malefic: even if trikona-kendra "
            "lords meet, if they are natural malefics (Saturn, Mars) for a "
            "given lagna AND in mutual enmity, yoga quality is reduced."
        ),
        confidence=0.75,
        verse="Ch.41 v.5-8",
        tags=["yoga", "raja_yoga", "malefic_reduction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY022",
        source="BPHS",
        chapter="Ch.41",
        school="parashari",
        category="yoga",
        description=(
            "Timing of raja yoga: raja yoga becomes active in the MD/AD "
            "of the yoga-forming planets. Both lords must be in their "
            "period for full manifestation."
        ),
        confidence=0.85,
        verse="Ch.41 v.9-12",
        tags=["yoga", "raja_yoga", "dasha_timing", "activation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY023",
        source="BPHS",
        chapter="Ch.41",
        school="parashari",
        category="yoga",
        description=(
            "Raja Yoga in Navamsha: if raja yoga forming planets are also "
            "conjunct or mutually supportive in D9 (Navamsha), the yoga is "
            "greatly strengthened and permanent."
        ),
        confidence=0.8,
        verse="Ch.41 v.13-15",
        tags=["yoga", "raja_yoga", "navamsha", "d9_confirmation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY024",
        source="BPHS",
        chapter="Ch.41",
        school="parashari",
        category="yoga",
        description=(
            "Partial Raja Yoga: one planet aspecting both a kendra and "
            "trikona lord (but not directly conjunct) forms a partial raja "
            "yoga — moderate rise and authority, not full."
        ),
        confidence=0.75,
        verse="Ch.41 v.16-18",
        tags=["yoga", "raja_yoga", "partial", "aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RY025",
        source="BPHS",
        chapter="Ch.41",
        school="parashari",
        category="yoga",
        description=(
            "Raja Yoga and Atma Karaka: if Atma Karaka (highest longitude "
            "planet, Jaimini system) is involved in a raja yoga, the "
            "soul-level ambition powerfully manifests the yoga."
        ),
        confidence=0.75,
        verse="Ch.41 v.19-21",
        tags=["yoga", "raja_yoga", "atma_karaka", "jaimini", "cross_school"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_RAJA_YOGA_REGISTRY.add(_r)
