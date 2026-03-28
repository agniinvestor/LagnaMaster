"""
src/corpus/phaladeepika_rules.py — Phaladeepika Rule Encoding (S206)

Mantreshwara's Phaladeepika (16th century) — one of the most cited
secondary references after BPHS. Famous for chapters on planetary
states (avastha), combustion, retrograde, Kartari yoga, and result prediction.

All rules here: implemented=False (pending Phase 1 encoding)
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

PHALADEEPIKA_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Planetary states ─────────────────────────────────────────────────────
    RuleRecord(
        rule_id="PH001",
        source="Phaladeepika",
        chapter="Ch.2 v.1-5",
        school="all",
        category="dignity",
        description=(
            "Planet in exaltation sign — uccha avastha. Gives full results of its "
            "significations. Strongest positive state."
        ),
        confidence=0.95,
        tags=["exaltation", "uccha", "planetary_state"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH002",
        source="Phaladeepika",
        chapter="Ch.2 v.6",
        school="all",
        category="dignity",
        description=(
            "Planet in own sign (svakshetra) — good strength, consistent results. "
            "More stable than exaltation but produces steady, reliable significations."
        ),
        confidence=0.9,
        tags=["own_sign", "svakshetra", "planetary_state"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH003",
        source="Phaladeepika",
        chapter="Ch.2 v.9",
        school="all",
        category="retrograde",
        description=(
            "Retrograde planet has enhanced inner power but irregular external expression. "
            "Results delayed, internalized, or expressed in non-conventional ways. "
            "Outer planets (Jupiter/Saturn) gain; inner planets (Mercury/Venus/Mars) suffer."
        ),
        confidence=0.85,
        tags=["retrograde", "vakra", "inner_expression"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH004",
        source="Phaladeepika",
        chapter="Ch.2 v.10-15",
        school="all",
        category="combustion",
        description=(
            "Combust planet (astanga) loses its individual significations. Results of "
            "the house it rules are diminished. Only cazimi (1°) is exempt and is strengthened."
        ),
        confidence=0.9,
        tags=["combust", "astanga", "sun_proximity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH005",
        source="Phaladeepika",
        chapter="Ch.2 v.16-20",
        school="all",
        category="strength",
        description=(
            "Baaladi Avasthas: planetary age states (infant, young, adult, old, dead). "
            "Adult = strongest (30° of arc from exaltation point). "
            "Infant/dead = weakest results."
        ),
        confidence=0.85,
        tags=["baaladi", "avastha", "planetary_age"],
        implemented=False,
    ),
    # ── Kartari yoga ─────────────────────────────────────────────────────────
    RuleRecord(
        rule_id="PH006",
        source="Phaladeepika",
        chapter="Ch.6 v.3",
        school="all",
        category="kartari",
        description=(
            "Shubha Kartari: natural benefics (Jupiter, Venus, Mercury, bright Moon) "
            "in both the sign before and after the house — the house is 'enclosed' in "
            "benefic protection. Highly auspicious."
        ),
        confidence=0.9,
        verse="Shubhaih parivritam bhavam",
        tags=["kartari", "shubha_kartari", "benefic_flanking"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH007",
        source="Phaladeepika",
        chapter="Ch.6 v.4",
        school="all",
        category="kartari",
        description=(
            "Paapa Kartari: natural malefics (Sun, Mars, Saturn, Rahu/Ketu) in "
            "both flanking signs — house is 'scissored' by malefics. Significantly damages "
            "house themes."
        ),
        confidence=0.9,
        verse="Paapair vritam papaphalapradam",
        tags=["kartari", "paapa_kartari", "malefic_flanking"],
        implemented=False,
    ),
    # ── House strength rules ──────────────────────────────────────────────────
    RuleRecord(
        rule_id="PH008",
        source="Phaladeepika",
        chapter="Ch.7",
        school="parashari",
        category="house_quality",
        description=(
            "House strength determined by: (1) sign quality, (2) bhavesh dignity, "
            "(3) planets in house, (4) aspect on house, (5) aspect on bhavesh. "
            "All five factors evaluated together for house judgment."
        ),
        confidence=0.9,
        tags=["house_judgment", "five_factors", "bhava_bala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH009",
        source="Phaladeepika",
        chapter="Ch.7 v.5",
        school="parashari",
        category="house_quality",
        description=(
            "House is strong when: (1) bhavesh is strong, (2) house has natural benefics, "
            "(3) house sign has malefic aspects cancelled by benefics."
        ),
        confidence=0.85,
        tags=["bhava_bala", "strong_house", "benefic_aspect"],
        implemented=False,
    ),
    # ── Graha Yuddha ─────────────────────────────────────────────────────────
    RuleRecord(
        rule_id="PH010",
        source="Phaladeepika",
        chapter="Ch.2 v.30-35",
        school="all",
        category="war",
        description=(
            "Graha Yuddha (planetary war): two visible planets within 1° longitude. "
            "Planet with lower latitude 'wins'; loser loses significations for life. "
            "Sun and Moon never in war. Rahu/Ketu are excluded."
        ),
        confidence=0.85,
        tags=["graha_yuddha", "planetary_war", "1_degree", "loser"],
        implemented=False,
    ),
    # ── Dasha activation rules ────────────────────────────────────────────────
    RuleRecord(
        rule_id="PH011",
        source="Phaladeepika",
        chapter="Ch.19",
        school="parashari",
        category="dasha",
        description=(
            "Vimshottari MD results: planet in kendra or trikona in good dignity "
            "gives Raja Yoga results during its Mahadasha."
        ),
        confidence=0.85,
        tags=["vimshottari", "mahadasha", "kendra", "trikona", "raja_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH012",
        source="Phaladeepika",
        chapter="Ch.19",
        school="parashari",
        category="dasha",
        description=(
            "Vimshottari MD of 6th/8th/12th lord — difficult period. "
            "Health issues, obstacles, losses depending on the dusthana nature."
        ),
        confidence=0.85,
        tags=["vimshottari", "mahadasha", "dusthana_lord", "difficult"],
        implemented=False,
    ),
    # ── Special ascendant rules ───────────────────────────────────────────────
    RuleRecord(
        rule_id="PH013",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="house_quality",
        description=(
            "Lagna in movable sign (Aries, Cancer, Libra, Capricorn) with lagna lord "
            "strong — native achieves through own initiative, frequent changes of place."
        ),
        confidence=0.8,
        tags=["lagna", "movable_sign", "initiative"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH014",
        source="Phaladeepika",
        chapter="Ch.3",
        school="parashari",
        category="house_quality",
        description=(
            "Lagna in fixed sign (Taurus, Leo, Scorpio, Aquarius) — stability, "
            "determination, persistence. Fixed sign lagna gives steady accumulation."
        ),
        confidence=0.8,
        tags=["lagna", "fixed_sign", "stability"],
        implemented=False,
    ),
    # ── Directional strength rules ────────────────────────────────────────────
    RuleRecord(
        rule_id="PH015",
        source="Phaladeepika",
        chapter="Ch.2",
        school="all",
        category="strength",
        description=(
            "Jupiter and Mercury gain Dig Bala in H1 (East = Lagna). "
            "These planets are most powerful when aspecting the ascendant directly."
        ),
        confidence=0.9,
        tags=["dig_bala", "jupiter", "mercury", "1st_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH016",
        source="Phaladeepika",
        chapter="Ch.2",
        school="all",
        category="strength",
        description=(
            "Moon and Venus gain Dig Bala in H4 (North = IC). "
            "These planets are most powerful in the 4th house."
        ),
        confidence=0.9,
        tags=["dig_bala", "moon", "venus", "4th_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH017",
        source="Phaladeepika",
        chapter="Ch.2",
        school="all",
        category="strength",
        description=(
            "Sun and Mars gain Dig Bala in H10 (South = MC). "
            "These planets are most powerful in the 10th house."
        ),
        confidence=0.9,
        tags=["dig_bala", "sun", "mars", "10th_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH018",
        source="Phaladeepika",
        chapter="Ch.2",
        school="all",
        category="strength",
        description=(
            "Saturn gains Dig Bala in H7 (West = Descendant). "
            "Saturn is most powerful when placed in the 7th house."
        ),
        confidence=0.9,
        tags=["dig_bala", "saturn", "7th_house"],
        implemented=False,
    ),
    # ── Paksha bala (Moon phase) ──────────────────────────────────────────────
    RuleRecord(
        rule_id="PH019",
        source="Phaladeepika",
        chapter="Ch.2",
        school="all",
        category="strength",
        description=(
            "Moon from new to full (Shukla Paksha — waxing) has Paksha Bala. "
            "Full Moon = maximum strength. Waxing Moon progressively stronger."
        ),
        confidence=0.9,
        tags=["moon", "paksha_bala", "shukla_paksha", "waxing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PH020",
        source="Phaladeepika",
        chapter="Ch.2",
        school="all",
        category="strength",
        description=(
            "Moon from full to new (Krishna Paksha — waning) lacks Paksha Bala. "
            "Dark Moon = minimum strength. New Moon weakest."
        ),
        confidence=0.9,
        tags=["moon", "paksha_bala", "krishna_paksha", "waning"],
        implemented=False,
    ),
    # ── Drishti (Aspect) strength ─────────────────────────────────────────────
    RuleRecord(
        rule_id="PH021",
        source="Phaladeepika",
        chapter="Ch.26",
        school="parashari",
        category="house_quality",
        description=(
            "Full (100%) aspect from 7th house — all planets have full 7th aspect. "
            "Half (50%) aspect from 5th/9th. Quarter (25%) aspect from 3rd/10th "
            "for Saturn only."
        ),
        confidence=0.85,
        tags=["aspect_strength", "7th_aspect", "full_aspect", "half_aspect"],
        implemented=False,
    ),
]

for _r in _RULES:
    PHALADEEPIKA_REGISTRY.add(_r)
