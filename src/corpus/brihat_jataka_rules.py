"""
src/corpus/brihat_jataka_rules.py — Brihat Jataka Rule Encoding (S206)

Varahamihira's Brihat Jataka (6th century CE) — the oldest systematic
treatise on Jyotish. Famous for planetary characteristics, house results,
and yogas. More compact and aphoristic than BPHS.

All rules here: implemented=False (pending Phase 1 encoding)
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BRIHAT_JATAKA_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Planetary characteristics (Ch.2) ─────────────────────────────────────
    RuleRecord(
        rule_id="BJ001",
        source="Brihat Jataka",
        chapter="Ch.2 v.4",
        school="all",
        category="dignity",
        description=(
            "Sun: exaltation in Aries 10°, debilitation in Libra 10°, own signs Leo. "
            "Moon: exaltation in Taurus 3°, debilitation in Scorpio 3°, own sign Cancer."
        ),
        confidence=0.95,
        tags=["sun", "moon", "exaltation", "debilitation", "own_sign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ002",
        source="Brihat Jataka",
        chapter="Ch.2 v.5",
        school="all",
        category="dignity",
        description=(
            "Mars: exaltation Capricorn 28°, debilitation Cancer 28°. "
            "Mercury: exaltation Virgo 15°, debilitation Pisces 15°."
        ),
        confidence=0.95,
        tags=["mars", "mercury", "exaltation", "debilitation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ003",
        source="Brihat Jataka",
        chapter="Ch.2 v.6",
        school="all",
        category="dignity",
        description=(
            "Jupiter: exaltation Cancer 5°, debilitation Capricorn 5°. "
            "Venus: exaltation Pisces 27°, debilitation Virgo 27°. "
            "Saturn: exaltation Libra 20°, debilitation Aries 20°."
        ),
        confidence=0.95,
        tags=["jupiter", "venus", "saturn", "exaltation", "debilitation"],
        implemented=False,
    ),
    # ── Natural benefic/malefic classification (Ch.2) ───────────────────────
    RuleRecord(
        rule_id="BJ004",
        source="Brihat Jataka",
        chapter="Ch.2 v.16",
        school="all",
        category="house_quality",
        description=(
            "Natural benefics: Jupiter, Venus, Mercury (when not with malefics), "
            "bright Moon (Shukla Paksha). These planets give auspicious results "
            "from the houses they occupy and aspect."
        ),
        confidence=0.95,
        tags=["natural_benefic", "jupiter", "venus", "mercury", "moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ005",
        source="Brihat Jataka",
        chapter="Ch.2 v.17",
        school="all",
        category="house_quality",
        description=(
            "Natural malefics: Sun, Mars, Saturn, Rahu, Ketu, dark Moon (Krishna Paksha), "
            "Mercury with malefics. These planets give challenging results from their "
            "occupied houses."
        ),
        confidence=0.95,
        tags=["natural_malefic", "sun", "mars", "saturn", "rahu", "ketu"],
        implemented=False,
    ),
    # ── Planetary mutual relationships (Ch.3) ────────────────────────────────
    RuleRecord(
        rule_id="BJ006",
        source="Brihat Jataka",
        chapter="Ch.3 v.1-5",
        school="all",
        category="yoga",
        description=(
            "Permanent friendship/enmity between planets (Naisargika Maitri). "
            "Sun: friendly with Moon/Mars/Jupiter; neutral with Mercury; "
            "enemy of Venus/Saturn."
        ),
        confidence=0.9,
        tags=["naisargika_maitri", "friendship", "enmity", "sun"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ007",
        source="Brihat Jataka",
        chapter="Ch.3 v.6",
        school="all",
        category="yoga",
        description=(
            "Tatkalika Maitri (temporary friendship): planets in mutual 2nd, 3rd, "
            "4th, 10th, 11th, 12th become temporary friends during a chart. "
            "Panchadha Maitri = combined permanent + temporary relationship."
        ),
        confidence=0.85,
        tags=["tatkalika_maitri", "temporary_friendship", "panchadha"],
        implemented=False,
    ),
    # ── House results (Ch.7) ──────────────────────────────────────────────────
    RuleRecord(
        rule_id="BJ008",
        source="Brihat Jataka",
        chapter="Ch.7 v.1",
        school="all",
        category="house_quality",
        description=(
            "1st house (Lagna): body, self, health, personality, beginning of life. "
            "Strongest house — all planetary positions relative to lagna. "
            "Lagna lord is most important planet in any chart."
        ),
        confidence=0.95,
        tags=["1st_house", "lagna", "body", "self", "health"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ009",
        source="Brihat Jataka",
        chapter="Ch.7 v.2",
        school="all",
        category="house_quality",
        description=(
            "2nd house: wealth, speech, family, food, right eye, accumulated resources. "
            "2nd lord in good position → good wealth and pleasant speech."
        ),
        confidence=0.9,
        tags=["2nd_house", "wealth", "speech", "family"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ010",
        source="Brihat Jataka",
        chapter="Ch.7 v.3",
        school="all",
        category="house_quality",
        description=(
            "3rd house: siblings, courage, short journeys, communication, right ear, "
            "valor. Mars especially strong here (upachaya)."
        ),
        confidence=0.9,
        tags=["3rd_house", "siblings", "courage", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ011",
        source="Brihat Jataka",
        chapter="Ch.7 v.4",
        school="all",
        category="house_quality",
        description=(
            "4th house: mother, happiness, home, property, vehicles, education "
            "(foundational). Moon as 4th natural karak — Moon in 4th strengthens."
        ),
        confidence=0.9,
        tags=["4th_house", "mother", "happiness", "home", "property"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ012",
        source="Brihat Jataka",
        chapter="Ch.7 v.5",
        school="all",
        category="house_quality",
        description=(
            "5th house: intellect, children, past-life merit (poorvapunya), "
            "speculation, mantra. Jupiter as 5th natural karak."
        ),
        confidence=0.9,
        tags=["5th_house", "children", "intellect", "poorvapunya", "jupiter"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ013",
        source="Brihat Jataka",
        chapter="Ch.7 v.6",
        school="all",
        category="house_quality",
        description=(
            "6th house: disease, enemies, debts, service, litigation, maternal uncle. "
            "Saturn and Mars do well here (upachaya position for malefics)."
        ),
        confidence=0.9,
        tags=["6th_house", "disease", "enemies", "debts", "service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ014",
        source="Brihat Jataka",
        chapter="Ch.7 v.7",
        school="all",
        category="house_quality",
        description=(
            "7th house: spouse, partnerships, open enemies, sexual relations, "
            "business partners. Venus as 7th natural karak."
        ),
        confidence=0.9,
        tags=["7th_house", "spouse", "partnership", "venus"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ015",
        source="Brihat Jataka",
        chapter="Ch.7 v.8",
        school="all",
        category="house_quality",
        description=(
            "8th house: longevity, inheritance, obstacles, in-laws, hidden matters, "
            "transformation, chronic disease. Saturn natural karak for 8th."
        ),
        confidence=0.9,
        tags=["8th_house", "longevity", "transformation", "obstacles"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ016",
        source="Brihat Jataka",
        chapter="Ch.7 v.9",
        school="all",
        category="house_quality",
        description=(
            "9th house: dharma, fortune, father, guru, long journeys, higher learning. "
            "Most powerful trikona — Jupiter and Sun as 9th natural karaks."
        ),
        confidence=0.9,
        tags=["9th_house", "dharma", "fortune", "father", "guru"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ017",
        source="Brihat Jataka",
        chapter="Ch.7 v.10",
        school="all",
        category="house_quality",
        description=(
            "10th house: career, action, status, government, father (secondary), "
            "profession. Sun, Mercury, Jupiter, Saturn as 10th natural karaks."
        ),
        confidence=0.9,
        tags=["10th_house", "career", "action", "status"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ018",
        source="Brihat Jataka",
        chapter="Ch.7 v.11",
        school="all",
        category="house_quality",
        description=(
            "11th house: gains, elder siblings, fulfillment of desires, income, "
            "social networks. Strongest upachaya house — planets grow here."
        ),
        confidence=0.9,
        tags=["11th_house", "gains", "income", "fulfillment", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ019",
        source="Brihat Jataka",
        chapter="Ch.7 v.12",
        school="all",
        category="house_quality",
        description=(
            "12th house: losses, expenses, liberation (moksha), foreign lands, "
            "sleep, hospitals, confinement. Saturn and Ketu as 12th natural karaks."
        ),
        confidence=0.9,
        tags=["12th_house", "losses", "moksha", "foreign", "liberation"],
        implemented=False,
    ),
    # ── Planetary aspect rules (Ch.8) ────────────────────────────────────────
    RuleRecord(
        rule_id="BJ020",
        source="Brihat Jataka",
        chapter="Ch.8 v.1-3",
        school="parashari",
        category="house_quality",
        description=(
            "All planets have full (100%) 7th house aspect. "
            "Jupiter additionally aspects 5th and 9th (full). "
            "Saturn additionally aspects 3rd and 10th. "
            "Mars additionally aspects 4th and 8th."
        ),
        confidence=0.95,
        tags=["aspect", "7th", "jupiter_aspect", "saturn_aspect", "mars_aspect"],
        implemented=False,
    ),
    # ── Yoga rules (Ch.15) ───────────────────────────────────────────────────
    RuleRecord(
        rule_id="BJ021",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="parashari",
        category="yoga",
        description=(
            "Adhi Yoga: benefics (Jupiter, Venus, Mercury) in the 6th, 7th, 8th "
            "from Moon — gives status, authority, good health, and long life. "
            "One of the most powerful wealth and status yogas."
        ),
        confidence=0.9,
        tags=["adhi_yoga", "benefic", "moon", "6th", "7th", "8th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ022",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="parashari",
        category="yoga",
        description=(
            "Sunapha Yoga: benefic planet in 2nd from Moon — gives wealth and "
            "good speech. One of the standard Moon-based yogas."
        ),
        confidence=0.85,
        tags=["sunapha", "moon_yoga", "benefic", "2nd_from_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ023",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="parashari",
        category="yoga",
        description=(
            "Anapha Yoga: benefic planet in 12th from Moon — gives good physical "
            "appearance, renunciation, and liberation themes."
        ),
        confidence=0.85,
        tags=["anapha", "moon_yoga", "benefic", "12th_from_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ024",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="parashari",
        category="yoga",
        description=(
            "Durudhara Yoga: benefics in both 2nd and 12th from Moon — "
            "native is prosperous, generous, and enjoys conveyances."
        ),
        confidence=0.85,
        tags=["durudhara", "moon_yoga", "benefic", "2nd", "12th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ025",
        source="Brihat Jataka",
        chapter="Ch.15",
        school="parashari",
        category="yoga",
        description=(
            "Kemadruma Yoga: no planet in 2nd or 12th from Moon (excluding Sun). "
            "Gives poverty, misfortune, or difficult circumstances unless cancelled "
            "by strong lagna or kendra planets."
        ),
        confidence=0.85,
        tags=["kemadruma", "moon_yoga", "poverty", "cancelled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJ026",
        source="Brihat Jataka",
        chapter="Ch.6",
        school="all",
        category="special",
        description=(
            "Hora chart (D2): the first hora of any sign belongs to Sun (male), "
            "second hora to Moon (female). Used for wealth and health analysis."
        ),
        confidence=0.85,
        tags=["hora", "d2", "divisional", "sun_hora", "moon_hora"],
        implemented=False,
    ),
]

for _r in _RULES:
    BRIHAT_JATAKA_REGISTRY.add(_r)
