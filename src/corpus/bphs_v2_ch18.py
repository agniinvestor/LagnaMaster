"""src/corpus/bphs_v2_ch18.py — BPHS Ch.18 (7th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.160-169.
Chapter: 18 — Effects of the Seventh House (Yuvati Bhava Phala)
Slokas: 42. MOST timing-rich chapter. Marriage ages: 5-34. Wife death ages: 13-33.
Entity: spouse (most), native (some for marriage timing).
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.18", category="7th_house_effects",
    id_start=1800, session="S311", sloka_count=42,
    chapter_tags=["7th_house", "yuvati_bhava"],
    entity_target="spouse",
)

# ═══ v.1: Full happiness through wife ════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": "any"},
                {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "strong"}],
    signal_group="h7_lord_strong_happy_marriage",
    direction="favorable", intensity="strong", domains=["marriage"],
    predictions=[{"entity": "spouse", "claim": "full_happiness_through_wife",
                  "domain": "marriage", "direction": "favorable", "magnitude": 0.8}],
    verse_ref="Ch.18 v.1",
    description="7th lord in own sign or exaltation: full happiness through wife and marriage.",
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1801"]},
)

# ═══ v.2: Sick wife ══════════════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": [6, 8, 12]}],
    signal_group="h7_lord_dusthana_sick_wife",
    direction="unfavorable", intensity="moderate", domains=["marriage", "physical_health"],
    predictions=[{"entity": "spouse", "claim": "wife_will_be_sickly",
                  "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.18 v.2",
    description="7th lord in 6th, 8th or 12th: the wife will be sickly.",
    commentary_context="Does not apply to own house or exaltation placement. Venus in exaltation in 7th house for Aries native need not be feared.",
    concordance_texts=["Saravali"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1800"]},
)

# ═══ v.3: Excessive libidinousness / death of wife ═══════════════════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Venus", "house": 7}],
    signal_group="venus_h7_libidinous",
    direction="mixed", intensity="moderate", domains=["marriage", "character_temperament"],
    predictions=[
        {"entity": "native", "claim": "exceedingly_libidinous",
         "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.6},
        {"entity": "spouse", "claim": "death_of_wife_if_venus_joins_malefic",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.5},
    ],
    entity_target="general",
    verse_ref="Ch.18 v.3",
    description="Venus in 7th: native exceedingly libidinous. Venus joining a malefic in any house will cause loss of wife.",
    concordance_texts=["Saravali"],
)

# ═══ v.4-5: 7th lord strong + benefic → wealthy, honourable ══════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": [1, 4, 5, 7, 9, 10]},
                {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "strong"}],
    signal_group="h7_lord_kendra_strong_wealthy",
    direction="favorable", intensity="strong", domains=["marriage", "wealth"],
    predictions=[
        {"entity": "native", "claim": "wealthy_honourable_happy_fortunate",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    entity_target="native",
    verse_ref="Ch.18 v.4-5",
    description="7th lord endowed with strength, conjunct/aspected by benefic: native wealthy, honourable, happy and fortunate.",
    commentary_context="Plurality of wives and sickness to them will come from the 7th lord occupying his sign of debilitation or having got combust or inimical placement.",
    concordance_texts=["Saravali"],
)

# ═══ v.6: Plurality of wives ═════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": "any"}],
    signal_group="h7_lord_saturn_venus_sign_many_wives",
    direction="neutral", intensity="moderate", domains=["marriage"],
    predictions=[{"entity": "native", "claim": "many_wives",
                  "domain": "marriage", "direction": "neutral", "magnitude": 0.5}],
    entity_target="native",
    verse_ref="Ch.18 v.6",
    description="7th lord in a sign of Saturn or Venus, aspected by a benefic: there will be many wives. 7th lord in exaltation → same effect.",
    concordance_texts=[],
    modifiers=[{"condition": "in_saturn_or_venus_sign", "effect": "conditionalizes", "strength": "moderate"},
               {"condition": "aspected_by_benefic", "effect": "amplifies", "strength": "moderate"}],
)

# ═══ v.14-15: Worthy spouse ══════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": "any"},
                {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "exalted"}],
    signal_group="h7_lord_exalted_worthy_spouse",
    direction="favorable", intensity="strong", domains=["marriage", "progeny"],
    predictions=[
        {"entity": "spouse", "claim": "spouse_with_seven_principal_virtues",
         "domain": "marriage", "direction": "favorable", "magnitude": 0.8},
        {"entity": "children", "claim": "sons_and_grandsons",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    entity_target="general",
    verse_ref="Ch.18 v.14-15",
    description="7th lord exalted + 7th with benefic + strong ascendant lord and benefic: spouse endowed with seven principal virtues, expanding dynasty by sons and grandsons.",
    concordance_texts=["Saravali"],
)

# ═══ v.17: Loss of spouse (early death) ══════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": [6, 8, 12]},
                {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "weak"}],
    signal_group="h7_lord_dusthana_weak_wife_death",
    direction="unfavorable", intensity="strong", domains=["marriage", "longevity"],
    predictions=[{"entity": "spouse", "claim": "wife_destroyed_early_death",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.18 v.17",
    description="7th lord devoid of strength in 6th/8th/12th or if 7th lord is in fall: the native's wife will be destroyed (i.e. she will die early).",
    concordance_texts=["Saravali"],
)

# ═══ v.22-34: TIMING OF MARRIAGE — each age as its own rule ══════════════════

_MARRIAGE_TIMING = [
    ("Ch.18 v.22", [5, 9], "7th lord in benefic's house + Venus exalted/own sign",
     [{"type": "lord_in_house", "lord_of": 7, "house": "any"}]),
    ("Ch.18 v.23", [7, 11], "Sun in 7th + dispositor conjunct Venus",
     [{"type": "planet_in_house", "planet": "Sun", "house": 7}]),
    ("Ch.18 v.24", [10, 16], "Venus in 2nd + 7th lord in 11th",
     [{"type": "planet_in_house", "planet": "Venus", "house": 2}]),
    ("Ch.18 v.25", [11], "Venus in angle from ascendant + ascendant lord in Cap/Aqu",
     [{"type": "planet_in_house", "planet": "Venus", "house": [1, 4, 7, 10]}]),
    ("Ch.18 v.26", [12, 19], "Venus in angle + Saturn in 7th from Venus",
     [{"type": "planet_in_house", "planet": "Venus", "house": [1, 4, 7, 10]}]),
    ("Ch.18 v.27", [18], "Venus in 7th from Moon + Saturn in 7th from Venus",
     [{"type": "planet_in_house", "planet": "Venus", "house": "any"}]),
    ("Ch.18 v.28", [15], "2nd lord in 11th + ascendant lord in 10th",
     [{"type": "lord_in_house", "lord_of": 2, "house": 11}]),
    ("Ch.18 v.29", [13], "Exchange of 2nd and 11th lords",
     [{"type": "lord_in_house", "lord_of": 2, "house": 11},
      {"type": "lord_in_house", "lord_of": 11, "house": 2}]),
    ("Ch.18 v.30", [22, 27], "Venus in 7th from 8th + dispositor conjunct Mars",
     [{"type": "planet_in_house", "planet": "Venus", "house": "any"}]),
    ("Ch.18 v.31", [23, 26], "7th lord in 12th + natal asc lord in 7th Navamsa",
     [{"type": "lord_in_house", "lord_of": 7, "house": 12}]),
    ("Ch.18 v.32", [25, 33], "8th lord in 7th + Venus in Navamsa ascendant",
     [{"type": "lord_in_house", "lord_of": 8, "house": 7}]),
    ("Ch.18 v.33", [31, 33], "Venus in 9th from 5th + Rahu in one of said houses",
     [{"type": "planet_in_house", "planet": "Venus", "house": "any"}]),
    ("Ch.18 v.34", [30, 27], "Venus in ascendant + 7th lord in 7th itself",
     [{"type": "planet_in_house", "planet": "Venus", "house": 1}]),
]

for vref, ages, desc_suffix, conds in _MARRIAGE_TIMING:
    age_val = ages[0] if len(ages) == 1 else ages
    tw_type = "age" if len(ages) == 1 else "age_range"
    b.add(
        conditions=conds,
        entity_target="native",
        signal_group=f"marriage_timing_{ages[0]}",
        direction="favorable", intensity="moderate", domains=["marriage"],
        predictions=[{"entity": "native", "claim": f"marriage_at_age_{ages[0]}",
                      "domain": "marriage", "direction": "favorable", "magnitude": 0.5}],
        timing_window={"type": tw_type, "value": age_val, "precision": "approximate"},
        verse_ref=vref,
        description=f"Marriage timing: {desc_suffix} → marry at age {'/'.join(str(a) for a in ages)}.",
        commentary_context="Santhanam: The age of marriage indicated in the text will not be practical in all cases in modern social conditions. These will be simply helpful in knowing of early and belated marriages." if vref == "Ch.18 v.22" else "",
    )

# ═══ v.35-39: TIMING OF WIFE'S DEATH ════════════════════════════════════════

_WIFE_DEATH_TIMING = [
    ("Ch.18 v.35", [18, 33], "7th lord in fall + Venus in 8th",
     [{"type": "lord_in_house", "lord_of": 7, "house": "any"},
      {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "debilitated"}]),
    ("Ch.18 v.36", [19], "7th lord in 8th + 12th lord in 7th",
     [{"type": "lord_in_house", "lord_of": 7, "house": 8},
      {"type": "lord_in_house", "lord_of": 12, "house": 7}]),
    ("Ch.18 v.38", [17, 21], "Venus in 8th + dispositor in Saturn sign",
     [{"type": "planet_in_house", "planet": "Venus", "house": 8}]),
    ("Ch.18 v.39", [13], "Ascendant lord in debilitation + 2nd lord in 8th",
     [{"type": "lord_in_house", "lord_of": 1, "house": "any"},
      {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "debilitated"}]),
]

for vref, ages, desc_suffix, conds in _WIFE_DEATH_TIMING:
    age_val = ages[0] if len(ages) == 1 else ages
    tw_type = "age" if len(ages) == 1 else "age_range"
    b.add(
        conditions=conds,
        signal_group=f"wife_death_{ages[0]}",
        direction="unfavorable", intensity="strong", domains=["marriage", "longevity"],
        predictions=[{"entity": "spouse", "claim": f"loss_of_wife_at_age_{ages[0]}",
                      "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7}],
        timing_window={"type": tw_type, "value": age_val, "precision": "approximate"},
        verse_ref=vref,
        description=f"Wife's death timing: {desc_suffix} → loss of wife at age {'/'.join(str(a) for a in ages)}.",
    )

# v.37: Wife dies within 3 days of marriage (snake bite!)
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Rahu", "house": 2},
                {"type": "planet_in_house", "planet": "Mars", "house": 7}],
    signal_group="rahu_h2_mars_h7_wife_death_3_days",
    direction="unfavorable", intensity="strong", domains=["marriage", "longevity"],
    predictions=[{"entity": "spouse", "claim": "wife_dies_within_3_days_of_marriage_snakebite",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    timing_window={"type": "after_event", "value": "marriage", "precision": "exact"},
    verse_ref="Ch.18 v.37",
    description="Rahu in 2nd + Mars in 7th: the native's wife will die within three days of marriage due to snake bite.",
    concordance_texts=[],
)

# ═══ v.42: Mars/Rahu/Saturn in 6-7-8 → wife will not live long ═══════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 6},
                {"type": "planet_in_house", "planet": "Rahu", "house": 7},
                {"type": "planet_in_house", "planet": "Saturn", "house": 8}],
    signal_group="mars_rahu_saturn_678_wife_short_life",
    direction="unfavorable", intensity="strong", domains=["marriage", "longevity"],
    predictions=[{"entity": "spouse", "claim": "wife_will_not_live_long",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.18 v.42",
    description="If the 6th, 7th and 8th are in their order occupied by Mars, Rahu and Saturn, the native's wife will not live long.",
    concordance_texts=[],
)

BPHS_V2_CH18_REGISTRY = b.build()
