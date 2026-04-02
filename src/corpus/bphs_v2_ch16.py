"""src/corpus/bphs_v2_ch16.py — BPHS Ch.16 (5th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.145-151.
Chapter: 16 — Effects of the Fifth House (Putra Bhava Phala)
Slokas: 32. Rich timing data (ages 30, 32, 33, 36, 40, 56).
Entity: children (most), native (some), general (mixed).
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.16", category="5th_house_effects",
    id_start=1600, session="S311", sloka_count=32,
    chapter_tags=["5th_house", "putra_bhava"],
    entity_target="children",
)

# ═══ v.1-3: Lords in own signs → happiness through children ══════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": [1, 4, 5, 7, 9, 10]},
    ],
    signal_group="h5_lord_kendra_children",
    direction="favorable", intensity="strong",
    domains=["progeny", "intelligence_education"],
    predictions=[
        {"entity": "children", "claim": "happiness_through_children",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.16 v.1-3",
    description=(
        "Lords of ascendant and 5th in their own signs or in angle/trine: "
        "one will enjoy thorough happiness through children."
    ),
    commentary_context=(
        "Santhanam notes: 'Suta' in Sanskrit used in compound word or as "
        "an adjective does not exclude a female issue for it means 'begotten'. "
        "The conjunction of the 5th lord with the ascendant lord in a good "
        "house will ensure early obtainment of children apart from happiness "
        "through them."
    ),
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1601"]},
)

# v.1-3b: 5th lord in dusthana → no offspring (contrary)
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": [6, 8, 12]}],
    signal_group="h5_lord_dusthana_no_children",
    direction="unfavorable", intensity="strong",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "no_offspring_or_early_loss",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.16 v.1-3",
    commentary_context="Santhanam: 5th lord with ascendant lord in evil house = defect. Combust/weak 5th lord = children quit world soon.",
    description=(
        "5th lord in 6th, 8th, or 12th: there will be no offspring. If the "
        "5th lord is combust or be with malefics and be weak, there will be "
        "no children; even if per chance obtained they will quit the world soon."
    ),
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1600"]},
)

# ═══ v.4: 5th lord in 6th + Mars → lose first child ═════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": 6},
        {"type": "planets_conjunct", "planets": ["lord_of_1", "Mars"]},
    ],
    signal_group="h5_lord_h6_mars_child_loss",
    direction="unfavorable", intensity="strong",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "lose_first_child",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.7},
        {"entity": "spouse", "claim": "female_not_fertile_thereafter",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6},
    ],
    entity_target="general",
    verse_ref="Ch.16 v.4",
    commentary_context="No separate Santhanam note. Dual affliction: 5th lord in 6th + Mars conjunction = compound yoga for child loss.",
    description=(
        "5th lord in 6th as the ascendant lord is conjunct Mars: the native "
        "will lose his very first child whereafter his female will not be "
        "fertile to yield an offspring."
    ),
    concordance_texts=[],
)

# ═══ v.5-6: One child only conditions ════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": [6, 8, 12]},
        {"type": "planet_in_house", "planet": "Mercury", "house": 5},
    ],
    signal_group="h5_lord_dusthana_mercury_ketu_one_child",
    direction="unfavorable", intensity="moderate",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "one_child_only",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.16 v.5-6",
    description=(
        "5th lord in fall/6th/8th/12th while Mercury and Ketu are in the "
        "5th: wife will give birth to one child only. Similarly if 5th lord "
        "in fall, not aspecting 5th, with Saturn and Mercury in 5th."
    ),
    commentary_context=(
        "Santhanam notes: The very presence of Mercury, or Ketu, or Saturn "
        "in the 5th will present a doubtful picture of progeny. If two of "
        "them join in the 5th, then there will be Kakavandhya Dosha "
        "(obtaining only a single issue) for the wife of the native, or "
        "even childlessness."
    ),
    concordance_texts=[],
    modifiers=[{"condition": "ketu_also_in_5th", "effect": "amplifies", "strength": "moderate"}],
)

# ═══ v.8: Difficulty in begetting ════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": [6, 8, 12]},
    ],
    signal_group="h5_lord_dusthana_difficulty",
    direction="unfavorable", intensity="moderate",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "beget_issues_with_difficulty",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.16 v.8",
    commentary_context="No separate note. Multiple dusthana/inimical placements all produce difficulty in begetting.",
    description=(
        "5th lord in 6th/8th/12th or in an inimical sign or in fall or "
        "in the 5th itself: the native will beget issues with difficulty."
    ),
    concordance_texts=["Saravali"],
)

# ═══ v.9: Adopted issues ═════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Saturn", "house": 5},
    ],
    signal_group="saturn_mandi_h5_adoption",
    direction="mixed", intensity="moderate",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "adopted_issues",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.16 v.9",
    description=(
        "5th house owned by Saturn or Mercury and be occupied or aspected "
        "by Saturn and Mandi: one will have adopted issues."
    ),
    commentary_context=(
        "Santhanam notes: 'Mandi' is the word used in the text which means "
        "Gulika. The rule applies to Aquarius, Taurus, Virgo and Libra lagnas. "
        "For the latter two, Saturn though rules the 5th, is helpless due to "
        "Gulika affliction. Otherwise Saturn related to the 5th house as its "
        "owner will not deprive one of progeny, making him go in for adoption."
    ),
    concordance_texts=[],
    modifiers=[{"condition": "mandi_aspecting_5th", "effect": "conditionalizes", "strength": "strong"}],
)

# ═══ v.10: 3 mothers or 2 fathers ════════════════════════════════════════════

b.add(
    conditions=[{"type": "planets_conjunct", "planets": ["Sun", "Moon"]}],
    entity_target="general",
    signal_group="sun_moon_conjunct_rasi_navamsa_parents",
    direction="unfavorable", intensity="moderate",
    domains=["longevity"],
    predictions=[
        {"entity": "native", "claim": "brought_up_by_3_mothers_or_2_fathers",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.16 v.10",
    description=(
        "Sun and Moon together in a Rasi and in the same Navamsa: the "
        "native will be brought up by 3 mothers or 2 fathers. This hints "
        "at possible loss of mother or father soon after birth."
    ),
    commentary_context=(
        "Santhanam notes: The luminaries should be in the same Rasi and "
        "same Navamsa. The child will be brought up by 3 females equal to "
        "mother or two men as father (i.e. paternal reatives etc.)."
    ),
    concordance_texts=[],
    cross_chapter_refs=["Ch.12 v.10 same combination"],
)

# ═══ v.11: Adopted issue ═════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": 12},
    ],
    signal_group="h5_lord_h12_adopted",
    direction="mixed", intensity="moderate",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "adopted_issue_indicated",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.16 v.11",
    commentary_context="No separate note. 6 planets in 5th + lord in 12th + strong Moon/ascendant = adoption indicated.",
    description=(
        "Adopted issue is indicated if the 5th is tenanted by six planets "
        "while its lord is in the 12th, and the Moon and ascendant are "
        "endowed with strength."
    ),
    concordance_texts=[],
)

# ═══ v.12: Many children ═════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": "any"},
        {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "strong"},
    ],
    signal_group="h5_lord_strong_many_children",
    direction="favorable", intensity="strong",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "many_children",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.16 v.12",
    commentary_context="No separate note. Strong 5th lord + 5th aspected by Mercury/Jupiter/Venus = many children.",
    description=(
        "There will be many children if the 5th lord is strong while the "
        "5th is aspected by strong Mercury, Jupiter and Venus."
    ),
    concordance_texts=["Saravali"],
)

# ═══ v.13: Daughters ═════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planets_conjunct", "planets": ["lord_of_5", "Moon"]},
    ],
    signal_group="h5_lord_moon_daughters",
    direction="neutral", intensity="moderate",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "beget_daughters",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.6},
    ],
    verse_ref="Ch.16 v.13",
    description=(
        "5th lord with the Moon or in her decanate: the native will beget "
        "daughters, so say astrologers."
    ),
    commentary_context=(
        "Santhanam notes: The 5th lord's joining the Moon will confer "
        "daughters rather than sons. The Moon is a planet of multiplicity "
        "and hence there will be a number of daughters. Moon's decanates "
        "are: first 10° of Cancer, second 10° of Pisces, third 10° of "
        "Scorpio."
    ),
    concordance_texts=[],
    prediction_type="trait",
)

# ═══ v.14: Questionable birth ════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Saturn", "house": 5},
        {"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "movable"},
        {"type": "planets_conjunct", "planets": ["moon", "rahu"]},
    ],
    signal_group="h5_lord_movable_saturn_rahu_illegitimate",
    direction="unfavorable", intensity="strong",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "questionable_or_illegitimate_birth",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.16 v.14",
    description=(
        "5th lord in a movable sign while Saturn is in the 5th as Rahu is "
        "with the Moon: the child (so born) is of questionable birth."
    ),
    commentary_context=(
        "Santhanam notes: 3 conditions — (a) 5th lord in movable sign, "
        "(b) 5th house occupied by Saturn, (c) Moon with Rahu (anywhere). "
        "The combinations indicating illegal birth get nullified under "
        "certain conditions."
    ),
    concordance_texts=[],
    modifiers=[],
    exceptions=[
        "strong_jupiter_aspect_on_5th_nullifies",
        "5th_lord_exalted_and_unafflicted_nullifies",
    ],
)

# ═══ v.16: 5th lord exalted + Jupiter → children assured ════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": [2, 5, 9]},
        {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "exalted"},
    ],
    signal_group="h5_lord_exalted_trikona_children",
    direction="favorable", intensity="strong",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "obtainment_of_children_assured",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.16 v.16",
    description=(
        "5th lord exalted or in 2nd/5th/9th from ascendant or conjunct/"
        "aspected by Jupiter: obtainment of children will be there."
    ),
    commentary_context=(
        "Santhanam notes: Anyone of 3 states ensures children — 1) 5th "
        "lord in exaltation, 2) 5th lord in 2nd/5th/9th, 3) 5th lord "
        "related to Jupiter by aspect or conjunction. Even though Jupiter "
        "may be ruler of the 6th or 8th or 12th, his association with the "
        "5th lord will ensure obtainment of children."
    ),
    concordance_texts=["Saravali"],
    convergence_signals=["jupiter_aspecting_5th", "h5_lord_strong"],
)

# ═══ v.18: Offspring at 32nd/33rd year ═══════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Jupiter", "house": 5},
    ],
    signal_group="jupiter_h5_offspring_32",
    direction="favorable", intensity="moderate",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "offspring_at_age_32_or_33",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age_range", "value": [32, 33], "precision": "approximate"},
    verse_ref="Ch.16 v.18",
    commentary_context="No separate note. Jupiter (karaka) in 5th + lord with Venus = offspring at 32/33.",
    description=(
        "If the 5th is occupied by Jupiter while its lord is with Venus, "
        "one will obtain an offspring in his 32nd/33rd year."
    ),
    concordance_texts=[],
    modifiers=[{"condition": "h5_lord_with_venus", "effect": "conditionalizes", "strength": "moderate"}],
)

# ═══ v.19: Child at 30 or 36 ═════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": [1, 4, 7, 10]},
    ],
    signal_group="h5_lord_kendra_jupiter_child_30_36",
    direction="favorable", intensity="moderate",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "beget_child_at_age_30_or_36",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age_range", "value": [30, 36], "precision": "approximate"},
    verse_ref="Ch.16 v.19",
    commentary_context="No separate note. 5th lord + Jupiter in kendra = child at 30/36. Jupiter as Putra Karaka.",
    description=(
        "5th lord in an angle along with Jupiter the Karaka: one will "
        "beget a child at the age of 30 or 36."
    ),
    concordance_texts=[],
)

# ═══ v.20: Child at 40 ══════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Jupiter", "house": 9},
    ],
    signal_group="jupiter_h9_venus_child_40",
    direction="favorable", intensity="moderate",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "beget_child_at_age_40",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.5},
    ],
    timing_window={"type": "age", "value": 40, "precision": "approximate"},
    verse_ref="Ch.16 v.20",
    commentary_context="No separate note. Jupiter 9th + Venus 9th from Jupiter + ascendant lord = late childbirth at 40.",
    description=(
        "Jupiter in the 9th from the ascendant while Venus is in the 9th "
        "from Jupiter along with the ascendant lord: one will beget a "
        "child at the age of 40."
    ),
    concordance_texts=[],
    modifiers=[
        {"condition": "venus_in_9th_from_jupiter", "effect": "conditionalizes", "strength": "moderate"},
        {"condition": "ascendant_lord_with_venus", "effect": "amplifies", "strength": "moderate"},
    ],
)

# ═══ v.21: Lose child at 32 ══════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Rahu", "house": 5},
    ],
    signal_group="rahu_h5_child_loss_32",
    direction="unfavorable", intensity="strong",
    domains=["progeny", "longevity"],
    predictions=[
        {"entity": "children", "claim": "lose_child_at_age_32",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    timing_window={"type": "age", "value": 32, "precision": "approximate"},
    verse_ref="Ch.16 v.21",
    commentary_context="Triple affliction: Rahu in 5th + 5th lord with malefic + Jupiter debilitated = loss of child at 32.",
    description=(
        "The native will at the age of 32 lose his child if Rahu is in "
        "the 5th, the 5th lord is conjunct a malefic and Jupiter is in "
        "debilitation."
    ),
    concordance_texts=[],
    modifiers=[
        {"condition": "h5_lord_conjunct_malefic", "effect": "amplifies", "strength": "strong"},
        {"condition": "jupiter_debilitated", "effect": "amplifies", "strength": "strong"},
    ],
)

# ═══ v.22: Loss of children at 33 and 36 ═════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_malefic", "house": "any"},
    ],
    signal_group="malefic_5th_from_jupiter_child_loss_33_36",
    direction="unfavorable", intensity="strong",
    domains=["progeny", "longevity"],
    predictions=[
        {"entity": "children", "claim": "loss_of_children_at_33_and_36",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    timing_window={"type": "age_range", "value": [33, 36], "precision": "approximate"},
    verse_ref="Ch.16 v.22",
    commentary_context="Malefic in 5th from Jupiter + another in 5th from ascendant = double affliction causing loss at 33/36.",
    description=(
        "There will be loss of children at 33 and 36 if a malefic is in "
        "the 5th from Jupiter while another is in the 5th from the ascendant."
    ),
    concordance_texts=[],
)

# ═══ v.23: Grief from child loss at 56 ═══════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_malefic", "house": 1},
    ],
    signal_group="mandi_asc_child_loss_56",
    direction="unfavorable", intensity="strong",
    domains=["progeny", "longevity"],
    predictions=[
        {"entity": "children", "claim": "grief_loss_of_child_at_56",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    timing_window={"type": "age", "value": 56, "precision": "approximate"},
    verse_ref="Ch.16 v.23",
    description=(
        "Should Mandi be in the ascendant while the ascendant lord is in "
        "fall: grief on account of loss of child at the age of 56."
    ),
    commentary_context=(
        "Santhanam notes: Mandi and Gulika are one and the same. The "
        "placement of Gulika in the ascendant while its lord is in "
        "debilitation at the native's age of 56 will cause death of an "
        "offspring. Similarly, the debilitation of Gulika's dispositor "
        "will cause harm to the bhava concerned."
    ),
    concordance_texts=[],
    modifiers=[{"condition": "ascendant_lord_in_fall", "effect": "conditionalizes", "strength": "strong"}],
)

# ═══ v.24-32: Number of children (compound rules, key ones) ══════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": "any"},
        {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "exalted"},
    ],
    signal_group="h5_lord_deep_exalt_10_sons",
    direction="favorable", intensity="strong",
    domains=["progeny"],
    predictions=[
        {"entity": "children", "claim": "ten_sons_indicated",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.16 v.24-32",
    description=(
        "There will be 10 sons if the 4th and the 6th are occupied by "
        "malefics while the 5th lord is in deep exaltation joining the "
        "ascendant lord as Jupiter is with another benefic. Nine sons if "
        "Jupiter is in deep exaltation with Rahu, 2nd lord, and 9th "
        "occupied by its own lord. Eight if Jupiter in 5th/9th + 5th lord "
        "strong + 2nd lord in 10th. Seven including twins born twice if "
        "Saturn in 9th from ascendant + 5th lord in 5th."
    ),
    commentary_context=(
        "Santhanam: These are indicative numbers for modern interpretation. "
        "If the 5th lord is with Mars, one will live long but lose his "
        "children one after the other as they are born."
    ),
    concordance_texts=[],
    prediction_type="trait",
    modifiers=[{"condition": "5th_lord_conjunct_mars_lose_children_as_born", "effect": "negates", "strength": "strong"}],
)

# ═══ v.6: Saturn+Mercury in 5th → one child only ═════════════════════════════
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": "any"},
                {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "debilitated"}],
    signal_group="h5_lord_fall_saturn_mercury_one_child",
    direction="unfavorable", intensity="moderate", domains=["progeny"],
    predictions=[{"entity": "children", "claim": "one_child_only_saturn_mercury_in_5th", "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.16 v.6",
    commentary_context="Santhanam: 5th lord in fall and not aspecting 5th while Saturn and Mercury in 5th = wife gives birth to one child only. Kakavandhya Dosha.",
    description="5th lord in fall, not aspecting 5th, while Saturn and Mercury in 5th: one child only.",
    modifiers=[{"condition": "saturn_and_mercury_in_5th", "effect": "conditionalizes", "strength": "strong"}])

# ═══ v.7: 9th lord in ascendant + 5th lord fall + Ketu+Mercury → progeny after ordeal
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 1},
                {"type": "lord_in_house", "lord_of": 5, "house": "any"}],
    signal_group="h9_lord_h1_h5_lord_fall_progeny_ordeal",
    direction="unfavorable", intensity="moderate", domains=["progeny"],
    predictions=[{"entity": "children", "claim": "progeny_after_great_ordeal", "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.16 v.7",
    commentary_context="Santhanam: Mercury, Ketu, or Saturn in 5th = doubtful progeny. Two of them = Kakavandhya Dosha (single issue) or even childlessness.",
    description="9th lord in ascendant + 5th lord in fall + Ketu in 5th with Mercury: progeny after great ordeal.",
    modifiers=[{"condition": "h5_lord_in_fall_ketu_mercury_in_5th", "effect": "conditionalizes", "strength": "strong"}])

# ═══ v.15: Born of other's loins (illegitimate) ══════════════════════════════
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Moon", "house": 8}],
    entity_target="native",
    signal_group="moon_h8_jupiter_8th_from_moon_illegitimate",
    direction="unfavorable", intensity="strong", domains=["progeny"],
    predictions=[{"entity": "native", "claim": "born_of_others_loins_illegitimate", "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.16 v.15",
    commentary_context="Santhanam: Moon in 8th from ascendant + Jupiter in 8th from Moon. Malefic's aspect/association is essential in this Yoga.",
    description="Moon in 8th from ascendant + Jupiter in 8th from Moon: native born of other's loins (illegitimate).",
    modifiers=[{"condition": "jupiter_in_8th_from_moon", "effect": "conditionalizes", "strength": "strong"}])

# ═══ v.17: Mean deeds — 3-4 malefics in 5th ══════════════════════════════════
b.add(
    conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 5}],
    signal_group="malefics_h5_mean_deeds_children",
    direction="unfavorable", intensity="moderate", domains=["progeny", "character_temperament"],
    predictions=[{"entity": "children", "claim": "children_indulge_in_mean_deeds", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.16 v.17",
    commentary_context="Santhanam: 5th occupied by 3-4 malefics + 5th lord in fall + benefic (including Mercury) excluded from 5th = children who indulge in mean deeds.",
    description="5th occupied by 3-4 malefics while 5th lord is in fall and benefic excluded: children indulge in mean deeds.",
    modifiers=[{"condition": "h5_lord_in_fall", "effect": "amplifies", "strength": "strong"},
               {"condition": "no_benefic_in_5th", "effect": "conditionalizes", "strength": "moderate"}])

# ═══ v.25-28: Number of children (individual slokas from the block) ═══════════
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Jupiter", "house": [5, 9]},
                {"type": "lord_in_house", "lord_of": 5, "house": "any"},
                {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "strong"},
                {"type": "lord_in_house", "lord_of": 2, "house": 10}],
    signal_group="jupiter_h5_h9_h5_lord_strong_8_sons",
    direction="favorable", intensity="strong", domains=["progeny"],
    predictions=[{"entity": "children", "claim": "eight_sons_indicated", "domain": "progeny", "direction": "favorable", "magnitude": 0.5}],
    verse_ref="Ch.16 v.26",
    commentary_context="Santhanam: Eight sons if Jupiter in 5th/9th + 5th lord endowed with strength + 2nd lord in 10th.",
    description="Jupiter in 5th/9th + 5th lord strong + 2nd lord in 10th: eight sons.",
    prediction_type="trait",
    modifiers=[])

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 9},
                {"type": "lord_in_house", "lord_of": 5, "house": 5}],
    signal_group="saturn_h9_h5_lord_h5_7_sons_twins",
    direction="favorable", intensity="moderate", domains=["progeny"],
    predictions=[{"entity": "children", "claim": "seven_sons_twins_born_twice", "domain": "progeny", "direction": "favorable", "magnitude": 0.5}],
    verse_ref="Ch.16 v.27",
    commentary_context="Santhanam: Saturn in 9th from ascendant + 5th lord in 5th itself = 7 sons, of whom twins will be born twice.",
    description="Saturn in 9th + 5th lord in 5th: seven sons, twins born twice.",
    prediction_type="trait")

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 5}],
    signal_group="h5_lord_h5_h2_lord_7_sons_3_die",
    direction="mixed", intensity="moderate", domains=["progeny", "longevity"],
    predictions=[
        {"entity": "children", "claim": "seven_sons_but_three_will_pass", "domain": "progeny", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.16 v.28",
    commentary_context="Santhanam: 5th lord in 5th in conjunction with 2nd lord = birth of 7 sons out of which 3 will pass away.",
    description="5th lord in 5th + conjunction with 2nd lord: 7 sons, 3 will pass away.",
    modifiers=[{"condition": "conjunct_h2_lord", "effect": "conditionalizes", "strength": "moderate"}],
    prediction_type="trait")

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": "any"}],
    signal_group="h5_lord_mars_lose_children_as_born",
    direction="unfavorable", intensity="strong", domains=["progeny", "longevity"],
    predictions=[{"entity": "children", "claim": "live_long_but_lose_children_one_after_other", "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7}],
    verse_ref="Ch.16 v.32",
    commentary_context="Santhanam: If the 5th lord is with Mars, one will live long but lose his children one after the other as they are born.",
    description="5th lord with Mars: native lives long but loses children one after the other as born.",
    modifiers=[{"condition": "5th_lord_conjunct_mars_children_lost_one_after_another_as_born", "effect": "conditionalizes", "strength": "strong"}],
    prediction_type="trait")

# ═══ GAP FILLS (identified by PDF-first audit 2026-04-01) ═════════════════════

# v.1-3 gap: 5th lord combust/with malefics/weak → no children (distinct from dusthana)
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": "any"},
                {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "weak"}],
    signal_group="h5_lord_combust_weak_no_children",
    direction="unfavorable", intensity="strong", domains=["progeny"],
    predictions=[{"entity": "children", "claim": "no_children_combust_or_weak_5th_lord",
                  "domain": "progeny", "direction": "unfavorable", "magnitude": 0.7}],
    verse_ref="Ch.16 v.1-3",
    commentary_context="Distinct from dusthana placement. Text: 'Should the lord of the 5th be combust or be with malefics and be weak, there will be no children; even if per chance issues are obtained they will only quit the world soon.'",
    description="5th lord combust or with malefics and weak: no children; if obtained they quit world soon.",
    modifiers=[{"condition": "conjunct_malefics", "effect": "amplifies", "strength": "strong"}])

# v.24-32 gap: 9 sons (Jupiter deep exaltation + Rahu + 2nd lord + 9th own lord)
b.add(
    conditions=[{"type": "planet_dignity", "planet": "Jupiter", "dignity": "exalted"},
                {"type": "planets_conjunct", "planets": ["Rahu", "lord_of_2"]}],
    signal_group="jupiter_deep_exalt_rahu_2nd_lord_9_sons",
    direction="favorable", intensity="strong", domains=["progeny"],
    predictions=[{"entity": "children", "claim": "nine_sons_indicated",
                  "domain": "progeny", "direction": "favorable", "magnitude": 0.5}],
    verse_ref="Ch.16 v.24-32",
    commentary_context="Jupiter in deep exaltation + Rahu with 2nd lord + 9th occupied by own lord → nine sons.",
    description="Jupiter deep exaltation + Rahu with 2nd lord + 9th lord in 9th: nine sons.",
    modifiers=[{"condition": "9th_house_occupied_by_its_own_lord_completes_nine_son_yoga", "effect": "conditionalizes", "strength": "moderate"}],
    prediction_type="trait")

# v.24-32 gap: Only 1 son (malefic 5th from asc + Jupiter 5th from Saturn)
b.add(
    conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 5}],
    signal_group="malefic_5th_jupiter_5th_from_saturn_1_son",
    direction="unfavorable", intensity="moderate", domains=["progeny"],
    predictions=[{"entity": "children", "claim": "only_one_son",
                  "domain": "progeny", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.16 v.24-32",
    commentary_context="Only one son if malefic in 5th from ascendant while Jupiter is in 5th from Saturn or vice versa.",
    description="Malefic in 5th from ascendant + Jupiter in 5th from Saturn (or vice versa): only one son.",
    modifiers=[{"condition": "jupiter_5th_from_saturn_or_vice_versa", "effect": "conditionalizes", "strength": "strong"}],
    prediction_type="trait")

# v.24-32 gap: Offspring through 2nd/3rd wife only
b.add(
    conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 5}],
    signal_group="malefic_h5_saturn_5th_from_jupiter_later_wife",
    direction="unfavorable", intensity="moderate", domains=["progeny", "marriage"],
    predictions=[{"entity": "children", "claim": "offspring_only_through_2nd_or_3rd_wife",
                  "domain": "progeny", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.16 v.24-32",
    commentary_context="If the 5th house has a malefic in it or if Saturn is in the 5th from Jupiter, the native will beget offspring only through his 2nd or 3rd wife.",
    description="Malefic in 5th or Saturn in 5th from Jupiter: offspring only through 2nd or 3rd wife.",
    modifiers=[{"condition": "saturn_5th_from_jupiter", "effect": "conditionalizes", "strength": "moderate"}],
    prediction_type="trait")

BPHS_V2_CH16_REGISTRY = b.build()
