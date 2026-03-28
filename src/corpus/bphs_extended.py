"""
src/corpus/bphs_extended.py — BPHS Extended Rule Encoding (S205)

Encodes 30 additional BPHS rules beyond R01-R23.
These rules are NOT yet implemented in the scoring engine.
They are Phase 1 (S216-S250) encoding targets.

Sources:
  - BPHS (Brihat Parashara Hora Shastra), primary reference edition
  - PVRNR commentary (P.V.R. Narasimha Rao)

All rules here: implemented=False (pending Phase 1 encoding)
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_EXTENDED_REGISTRY = CorpusRegistry()

_BPHS_RULES = [
    # ── Lagna-lord rules (BPHS Ch.11, 24) ───────────────────────────────────
    RuleRecord(
        rule_id="B001",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="dignity",
        description=(
            "Lagna lord in kendra or trikona in good dignity — native prospers, "
            "good health and general life fortune. Strongest positive combination."
        ),
        confidence=0.9,
        tags=["lagna_lord", "kendra", "trikona", "dignity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B002",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="dignity",
        description=(
            "Lagna lord in dusthana (6, 8, 12) — poor health, obstacles, difficult "
            "life themes. Strongest single negative for lagna lord."
        ),
        confidence=0.9,
        tags=["lagna_lord", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B003",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="yoga",
        description=(
            "Lagna lord and 9th lord in mutual kendra — Dharma-Karma Adhipati Yoga. "
            "Gives fortune, righteousness, and career success."
        ),
        confidence=0.85,
        tags=["lagna_lord", "9th_lord", "kendra", "dharmakarmayoga"],
        implemented=False,
    ),
    # ── 9th and 10th house rules (BPHS Ch.24, 27) ───────────────────────────
    RuleRecord(
        rule_id="B004",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="yoga",
        description=(
            "9th lord and 10th lord conjunction (Dharma-Karma Adhipati Yoga) — "
            "produces high achievement and dharmic career. Most powerful career yoga."
        ),
        confidence=0.95,
        verse="Navameshe dashameshe va parasparasambandhe",
        tags=["9th_lord", "10th_lord", "dharmakarmayoga", "career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B005",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="yoga",
        description=(
            "9th lord in 10th or 10th lord in 9th — Bhagya-Karma exchange yoga. "
            "Fortune supports career; career is in alignment with dharma."
        ),
        confidence=0.85,
        tags=["9th_lord", "10th_lord", "exchange", "career", "fortune"],
        implemented=False,
    ),
    # ── Vargottama rules (BPHS Ch.6) ────────────────────────────────────────
    RuleRecord(
        rule_id="B006",
        source="BPHS",
        chapter="Ch.6",
        school="all",
        category="strength",
        description=(
            "Vargottama planet (same sign in D1 and D9) — greatly strengthened. "
            "Said to give results as if in moolatrikona. Strong in all schools."
        ),
        confidence=0.9,
        tags=["vargottama", "d9", "navamsha", "strength"],
        implemented=False,
    ),
    # ── Moon rules (BPHS Ch.15, 16) ─────────────────────────────────────────
    RuleRecord(
        rule_id="B007",
        source="BPHS",
        chapter="Ch.15",
        school="all",
        category="strength",
        description=(
            "Moon in Pushya nakshatra — extremely benefic; Pushya is the most "
            "nourishing nakshatra, lord Saturn governs discipline and structure."
        ),
        confidence=0.85,
        tags=["moon", "pushya", "nakshatra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B008",
        source="BPHS",
        chapter="Ch.16",
        school="parashari",
        category="house_quality",
        description=(
            "Moon in 1, 4, 7, 10 (kendra) with full paksha bala (bright fortnight) — "
            "gives emotional stability, public recognition, good results for the house."
        ),
        confidence=0.85,
        tags=["moon", "kendra", "paksha_bala", "bright_fortnight"],
        implemented=False,
    ),
    # ── Exaltation/debilitation rules (BPHS Ch.3, 47) ───────────────────────
    RuleRecord(
        rule_id="B009",
        source="BPHS",
        chapter="Ch.3",
        school="all",
        category="dignity",
        description=(
            "Planet in deep exaltation degree — maximum strength, fully manifests "
            "all positive significations. Rare condition with strong birth promise."
        ),
        confidence=0.95,
        tags=["exaltation", "deep_exaltation", "uccha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B010",
        source="BPHS",
        chapter="Ch.3",
        school="all",
        category="dignity",
        description=(
            "Planet in deep debilitation degree — minimum strength, most negative "
            "for its significations. Neecha Bhanga can partially cancel this."
        ),
        confidence=0.95,
        tags=["debilitation", "deep_debilitation", "neecha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B011",
        source="BPHS",
        chapter="Ch.47",
        school="all",
        category="dignity",
        description=(
            "Neecha Bhanga Raja Yoga: debilitated planet with exaltation lord in "
            "kendra from lagna or Moon — cancels debilitation, can give raja yoga."
        ),
        confidence=0.9,
        tags=["neecha_bhanga", "raja_yoga", "debilitation", "cancellation"],
        implemented=False,
    ),
    # ── Aspect rules (BPHS Ch.26) ────────────────────────────────────────────
    RuleRecord(
        rule_id="B012",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="house_quality",
        description=(
            "Jupiter full aspect (5th, 7th, 9th from occupied house) — strong, "
            "purifying influence on aspected house and its significations."
        ),
        confidence=0.9,
        tags=["jupiter", "full_aspect", "5th", "9th", "purifying"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B013",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="house_quality",
        description=(
            "Saturn full aspect (3rd, 7th, 10th from occupied house) — restrictive, "
            "disciplining influence. Delays and burdens the aspected house themes."
        ),
        confidence=0.9,
        tags=["saturn", "full_aspect", "3rd", "10th", "restrictive"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B014",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="house_quality",
        description=(
            "Mars full aspect (4th, 7th, 8th from occupied house) — aggressive, "
            "energizing but also potentially destructive for aspected houses."
        ),
        confidence=0.9,
        tags=["mars", "full_aspect", "4th", "8th", "aggressive"],
        implemented=False,
    ),
    # ── 2nd and 11th house rules (income, speech) ───────────────────────────
    RuleRecord(
        rule_id="B015",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="house_quality",
        description=(
            "2nd lord in 2nd or 11th — good for finances, accumulation of wealth. "
            "2nd house speech and family well-supported."
        ),
        confidence=0.85,
        tags=["2nd_lord", "wealth", "income", "speech"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B016",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="house_quality",
        description=(
            "11th lord in 11th or 2nd — strong upachaya (gain) house position. "
            "Income from multiple sources, elder siblings prosper."
        ),
        confidence=0.85,
        tags=["11th_lord", "upachaya", "income", "gains"],
        implemented=False,
    ),
    # ── Parivartana yoga (exchange) ──────────────────────────────────────────
    RuleRecord(
        rule_id="B017",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="yoga",
        description=(
            "Parivartana Yoga (mutual exchange): two lords in each other's signs — "
            "both lords gain strength as if in own sign. One of the strongest yogas."
        ),
        confidence=0.9,
        tags=["parivartana", "exchange", "mutual_reception"],
        implemented=False,
    ),
    # ── Rahu/Ketu rules (BPHS Ch.47) ────────────────────────────────────────
    RuleRecord(
        rule_id="B018",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="house_quality",
        description=(
            "Rahu in kendra (1, 4, 7, 10) — can give strong material results but "
            "with obsession or illusion. Must be evaluated with dispositor dignity."
        ),
        confidence=0.8,
        tags=["rahu", "kendra", "material", "illusion"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B019",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="house_quality",
        description=(
            "Ketu in 12th house — excellent for liberation, spiritual practices, "
            "foreign travel, and moksha themes. Ketu natural karaka for 12th."
        ),
        confidence=0.85,
        tags=["ketu", "12th_house", "moksha", "liberation"],
        implemented=False,
    ),
    # ── Atmakaraka rules (Jaimini) ───────────────────────────────────────────
    RuleRecord(
        rule_id="B020",
        source="BPHS",
        chapter="Ch.32",
        school="jaimini",
        category="karak",
        description=(
            "Atmakaraka (AK — planet at highest degree) indicates the soul's primary "
            "lesson and dominant life theme. AK lord of navamsha (Karakamsha) "
            "reveals spiritual destiny."
        ),
        confidence=0.9,
        tags=["atmakaraka", "jaimini", "karakamsha", "soul"],
        implemented=False,
    ),
    # ── 5th and 9th house rules (dharma, wisdom) ────────────────────────────
    RuleRecord(
        rule_id="B021",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="house_quality",
        description=(
            "5th lord in trikona with Jupiter — strong for intellect, children, "
            "past-life merit (poorvapunya). Beneficial for education and creativity."
        ),
        confidence=0.85,
        tags=["5th_lord", "trikona", "jupiter", "intellect", "children"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B022",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="house_quality",
        description=(
            "9th lord in lagna — the bhagya lord (fortune lord) in the body house. "
            "Self-made fortune, native's own efforts bring dharmic results."
        ),
        confidence=0.85,
        tags=["9th_lord", "lagna", "fortune", "dharma"],
        implemented=False,
    ),
    # ── Yogakaraka rules (lagna-specific) ───────────────────────────────────
    RuleRecord(
        rule_id="B023",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="yoga",
        description=(
            "Yogakaraka planet (lord of both kendra and trikona) in kendra or trikona — "
            "Raja Yoga. Lagna-specific: Saturn for Taurus/Libra, Mars for Cancer/Leo."
        ),
        confidence=0.95,
        tags=["yogakaraka", "raja_yoga", "kendra", "trikona"],
        implemented=False,
    ),
    # ── Argala rules (BPHS Ch.28) ────────────────────────────────────────────
    RuleRecord(
        rule_id="B024",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="special",
        description=(
            "Argala (intervention): planet in 2nd, 4th, or 11th from a reference "
            "point creates Argala (obstruction or support). 2nd and 4th are strongest."
        ),
        confidence=0.85,
        tags=["argala", "virodha_argala", "intervention"],
        implemented=False,
    ),
    # ── Transit rules (BPHS Ch.50) ───────────────────────────────────────────
    RuleRecord(
        rule_id="B025",
        source="BPHS",
        chapter="Ch.50",
        school="all",
        category="timing",
        description=(
            "Jupiter transit over natal Moon — auspicious period for expansion, "
            "growth, and new beginnings. One of the most reliable transit indicators."
        ),
        confidence=0.85,
        tags=["jupiter", "transit", "moon", "gochar"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="B026",
        source="BPHS",
        chapter="Ch.50",
        school="all",
        category="timing",
        description=(
            "Saturn transit over natal Moon (Sade Sati — 7½ year Saturn cycle): "
            "one of the most significant life-transforming transit periods."
        ),
        confidence=0.9,
        tags=["saturn", "transit", "moon", "sade_sati", "gochar"],
        implemented=False,
    ),
    # ── Moolatrikona rules ───────────────────────────────────────────────────
    RuleRecord(
        rule_id="B027",
        source="BPHS",
        chapter="Ch.3",
        school="all",
        category="dignity",
        description=(
            "Planet in moolatrikona sign (primary own sign zone) — second strongest "
            "dignity after exaltation. Full significations expressed naturally."
        ),
        confidence=0.9,
        tags=["moolatrikona", "dignity", "own_sign"],
        implemented=False,
    ),
    # ── 8th house rules ──────────────────────────────────────────────────────
    RuleRecord(
        rule_id="B028",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="house_quality",
        description=(
            "8th lord in 8th — 'Sarpa Yoga' context — can indicate longevity "
            "(strong 8th) or serious health challenges depending on dignity. "
            "Mixed results depending on school interpretation."
        ),
        confidence=0.75,
        tags=["8th_lord", "8th_house", "longevity", "transformation"],
        implemented=False,
    ),
    # ── 4th house rules (happiness, property) ───────────────────────────────
    RuleRecord(
        rule_id="B029",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="house_quality",
        description=(
            "4th lord in 4th or 1st — domestic happiness, good mother relationship, "
            "property ownership. 4th lord in own sign is especially strong."
        ),
        confidence=0.85,
        tags=["4th_lord", "4th_house", "happiness", "property", "mother"],
        implemented=False,
    ),
    # ── Upachaya house growth rules (BPHS Ch.11) ────────────────────────────
    RuleRecord(
        rule_id="B030",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Malefics in upachaya houses (3, 6, 10, 11) — natural malefics gain "
            "strength and give better results in upachaya houses than in trines. "
            "Rule: 'Papa in upachaya, shubha in trikona.'"
        ),
        confidence=0.9,
        verse="Papas trikonasthita na shubha upachayasthita shubhah",
        tags=["malefic", "upachaya", "3rd", "6th", "10th", "11th"],
        implemented=False,
    ),
    # ── Bonus rule 31 ────────────────────────────────────────────────────────
    RuleRecord(
        rule_id="B031",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Benefics in trikona (1, 5, 9) — natural benefics in trine houses "
            "give the highest auspicious results for those houses and life themes. "
            "Rule: benefics in trikona, malefics in upachaya."
        ),
        confidence=0.9,
        tags=["benefic", "trikona", "1st", "5th", "9th", "auspicious"],
        implemented=False,
    ),
]

for _r in _BPHS_RULES:
    BPHS_EXTENDED_REGISTRY.add(_r)
