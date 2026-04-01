"""
src/corpus/transit_rules.py — Classical Transit (Gochara) Rules (S242)

Encodes classical Gochara (planetary transit) rules from multiple sources:
Sarvartha Chintamani, BPHS Ch.90, and traditional transit literature.

Sources:
  Sarvartha Chintamani (Venkatesh Daivagna) — Ch.10, Gochara Adhyaya
  BPHS Ch.90 — Transit results
  Krishnamurti on transits (KP transit principles)

30 rules total: TRN001-TRN030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

TRANSIT_RULES_REGISTRY = CorpusRegistry()

_TRANSIT_RULES = [
    # --- Fundamental Transit Principles (TRN001-005) ---
    RuleRecord(
        rule_id="TRN001",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Gochara fundamental principle: Transits are counted from the natal Moon sign "
            "(Janma Rashi). The effects of a transiting planet depend on which house "
            "from the natal Moon it occupies, not from the lagna."
        ),
        confidence=0.93,
        verse="BPHS Ch.90 v.1-3",
        tags=["transit", "gochara", "from_moon", "fundamental", "janma_rashi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN002",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Sarvartha Chintamani: Transit results occur only when the natal chart "
            "promises the event AND the dasha supports it. "
            "Transit alone cannot give results not indicated in the natal chart."
        ),
        confidence=0.92,
        verse="SC Ch.10 v.1-3",
        tags=["transit", "natal_promise", "dasha_transit_combined", "fundamental"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN003",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Transit benefic/malefic positions from Moon (Vedha principle): "
            "Certain houses from natal Moon are beneficial for transiting planets. "
            "General: 3, 6, 10, 11 are good positions for transiting planets."
        ),
        confidence=0.88,
        verse="BPHS Ch.90 v.4-7",
        tags=["transit", "vedha", "3_6_10_11_good", "from_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN004",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Vedha (obstruction) principle: Even when a planet is in a favorable "
            "transit position, another planet in the Vedha position from it can "
            "obstruct the benefits. Each beneficial position has a corresponding Vedha point."
        ),
        confidence=0.87,
        verse="BPHS Ch.90 v.8-11",
        tags=["transit", "vedha", "obstruction", "vedha_principle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN005",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Ashtakavarga transit: When a planet transits a sign where it has "
            "high Ashtakavarga bindus (5+ points), the transit is beneficial. "
            "Low bindus (0-3) = difficult transit regardless of house position."
        ),
        confidence=0.90,
        verse="SC Ch.10 v.4-7",
        tags=["transit", "ashtakavarga", "bindus", "quantitative_transit"],
        implemented=False,
    ),
    # --- Sun Transit (TRN006-007) ---
    RuleRecord(
        rule_id="TRN006",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Sun transit results from natal Moon: "
            "Good in 3, 6, 10, 11. Bad in 1, 2, 4, 5, 7, 8, 9, 12. "
            "Sun in 3rd from Moon = courage, victory; 6th = defeat of enemies; "
            "10th = career success; 11th = gains and fulfillment."
        ),
        confidence=0.88,
        verse="BPHS Ch.90 v.12-18",
        tags=["transit", "sun_transit", "from_moon", "3_6_10_11"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN007",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Sun transit difficult positions: Sun in 1st from Moon = fever, eye trouble; "
            "5th = stomach problems, children issues; 9th = father's health, dharma obstacles; "
            "12th = expenses, distant travel forced."
        ),
        confidence=0.86,
        verse="BPHS Ch.90 v.19-24",
        tags=["transit", "sun_transit", "difficult_positions", "1_5_9_12_bad"],
        implemented=False,
    ),
    # --- Moon Transit (TRN008-009) ---
    RuleRecord(
        rule_id="TRN008",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Moon transit results: Good in 1, 3, 6, 7, 10, 11. "
            "Moon transiting its own natal position (1st) = happiness and new beginnings. "
            "3rd = courage; 6th = health; 7th = spouse happiness; 10th = career."
        ),
        confidence=0.87,
        verse="BPHS Ch.90 v.25-30",
        tags=["transit", "moon_transit", "1_3_6_7_10_11_good", "from_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN009",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Moon transit difficult: 4th = mental disturbance, mother issues; "
            "8th = fear, health problems; 12th = loss, loneliness. "
            "Moon transits last about 2.25 days per sign."
        ),
        confidence=0.86,
        verse="BPHS Ch.90 v.31-35",
        tags=["transit", "moon_transit", "4_8_12_bad", "2_days_per_sign"],
        implemented=False,
    ),
    # --- Mars Transit (TRN010-011) ---
    RuleRecord(
        rule_id="TRN010",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Mars transit results: Good in 3, 6, 11. "
            "3rd from Moon = courage, victory over enemies; 6th = defeat of competitors; "
            "11th = gains, fulfillment of desires. Mars transits ~45 days per sign."
        ),
        confidence=0.88,
        verse="BPHS Ch.90 v.36-40",
        tags=["transit", "mars_transit", "3_6_11_good", "45_days"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN011",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Mars transit difficult: 1st from Moon = fever, accidents; 4th = family disputes; "
            "7th = conflict with spouse/partners; 8th = serious health risk; "
            "12th = loss, surgery risk. Extra care needed when Mars transits 8th."
        ),
        confidence=0.87,
        verse="BPHS Ch.90 v.41-46",
        tags=["transit", "mars_transit", "1_4_7_8_12_bad", "accident_risk"],
        implemented=False,
    ),
    # --- Mercury Transit (TRN012-013) ---
    RuleRecord(
        rule_id="TRN012",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Mercury transit results: Good in 2, 4, 6, 8, 10, 11. "
            "2nd from Moon = financial gains, good speech; 6th = success in competition; "
            "11th = fulfillment of intellectual goals. Mercury is generally beneficial."
        ),
        confidence=0.86,
        verse="BPHS Ch.90 v.47-52",
        tags=["transit", "mercury_transit", "2_4_6_8_10_11_good"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN013",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Mercury transit difficult: 1st, 3rd, 5th, 7th, 9th, 12th from Moon "
            "can cause communication issues, contractual disputes, or nervous problems. "
            "Mercury retrograde in difficult positions = delays and misunderstandings."
        ),
        confidence=0.84,
        verse="BPHS Ch.90 v.53-57",
        tags=["transit", "mercury_transit", "retrograde_transit", "odd_houses_bad"],
        implemented=False,
    ),
    # --- Jupiter Transit (TRN014-015) ---
    RuleRecord(
        rule_id="TRN014",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Jupiter transit results: Good in 2, 5, 7, 9, 11. "
            "2nd = family prosperity; 5th = children's welfare, intelligence; "
            "7th = marriage/partnership opportunities; 9th = dharma, guru; "
            "11th = maximum gains. Jupiter transits ~1 year per sign."
        ),
        confidence=0.90,
        verse="BPHS Ch.90 v.58-64",
        tags=["transit", "jupiter_transit", "2_5_7_9_11_good", "1_year_per_sign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN015",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Jupiter transit difficult: 1st from Moon (Janma Guru) = mixed results, "
            "challenges despite Jupiter's nature; 3rd = courage tested; "
            "4th = domestic changes; 8th = health concerns; 12th = spiritual retreat. "
            "Janma Guru (1st) actually brings transformation rather than just harm."
        ),
        confidence=0.86,
        verse="BPHS Ch.90 v.65-70",
        tags=["transit", "jupiter_transit", "janma_guru", "1st_mixed", "transformation"],
        implemented=False,
    ),
    # --- Venus Transit (TRN016-017) ---
    RuleRecord(
        rule_id="TRN016",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Venus transit results: Good in 1, 2, 3, 4, 5, 8, 9, 11, 12. "
            "Most positions are beneficial for Venus. 1st = attractiveness; "
            "2nd = financial gains; 5th = romance; 11th = maximum pleasure and gains."
        ),
        confidence=0.86,
        verse="BPHS Ch.90 v.71-76",
        tags=["transit", "venus_transit", "mostly_good", "pleasure"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN017",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Venus transit difficult: 6th from Moon = health issues for spouse; "
            "7th = relationship conflicts; 10th = career complications. "
            "Venus is generally most beneficial when transiting kendras from natal Moon."
        ),
        confidence=0.84,
        verse="BPHS Ch.90 v.77-80",
        tags=["transit", "venus_transit", "6_7_10_bad", "generally_benefic"],
        implemented=False,
    ),
    # --- Saturn Transit (TRN018-021) ---
    RuleRecord(
        rule_id="TRN018",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Saturn transit results: Good only in 3, 6, 11 from natal Moon. "
            "3rd = courage, victory; 6th = defeat of enemies, good health; "
            "11th = gains, career fulfillment. Saturn transits ~2.5 years per sign."
        ),
        confidence=0.90,
        verse="BPHS Ch.90 v.81-86",
        tags=["transit", "saturn_transit", "3_6_11_good", "2_5_years"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN019",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Sade Sati (7.5 years of Saturn): Saturn in 12th, 1st, or 2nd from natal Moon "
            "constitutes Sade Sati. Divided into three 2.5-year phases. "
            "Rising phase (12th): mental stress; Peak (1st): most difficult; Ending (2nd): financial."
        ),
        confidence=0.92,
        verse="SC Ch.10 v.8-14",
        tags=["transit", "sade_sati", "saturn_7_5_years", "12_1_2_from_moon", "three_phases"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN020",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Sade Sati mitigation: Sade Sati's intensity depends on natal Saturn's strength. "
            "Strong Saturn in D1 or D9 mitigates. Sade Sati in Saturn's own sign (Cap/Aquarius) "
            "or exaltation (Libra) is much less harmful."
        ),
        confidence=0.88,
        verse="SC Ch.10 v.15-18",
        tags=["transit", "sade_sati", "mitigation", "saturn_strength", "own_sign_relief"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN021",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Saturn's Ashtama Shani (8th from Moon transit): 2.5-year period. "
            "Health challenges, career setbacks, isolation. "
            "Can be productive if used for spiritual practice and disciplined work."
        ),
        confidence=0.88,
        verse="SC Ch.10 v.19-22",
        tags=["transit", "ashtama_shani", "saturn_8th", "health_career_risk"],
        implemented=False,
    ),
    # --- Rahu/Ketu Transit (TRN022-023) ---
    RuleRecord(
        rule_id="TRN022",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Rahu transit: Good in 3, 6, 11 from natal Moon. "
            "Rahu in 3rd = unconventional courage; 6th = defeat of enemies through strategy; "
            "11th = unusual gains. Rahu transits ~18 months per sign."
        ),
        confidence=0.85,
        verse="SC Ch.10 v.23-27",
        tags=["transit", "rahu_transit", "3_6_11_good", "18_months"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN023",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Ketu transit: Opposite axis to Rahu. Generally good in 3, 6, 11 from Moon "
            "like Rahu. But 1st from Moon = spiritual confusion; 8th = health crises. "
            "Ketu in 12th from Moon can support spiritual retreats."
        ),
        confidence=0.83,
        verse="SC Ch.10 v.28-31",
        tags=["transit", "ketu_transit", "3_6_11_good", "12th_spiritual"],
        implemented=False,
    ),
    # --- Combined Transit Principles (TRN024-030) ---
    RuleRecord(
        rule_id="TRN024",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Double transit principle: Jupiter and Saturn transiting the same house "
            "or 7th from each other simultaneously triggers major life events. "
            "Both aspecting the natal Moon sign = peak event period."
        ),
        confidence=0.88,
        verse="SC Ch.10 v.32-36",
        tags=["transit", "double_transit", "jupiter_saturn", "major_events"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN025",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Triple transit trigger for events: For an event to manifest, "
            "a transiting planet must (1) be in a favorable house from Moon, "
            "(2) transit over a natal significator, AND (3) support the dasha period."
        ),
        confidence=0.87,
        verse="SC Ch.10 v.37-40",
        tags=["transit", "triple_trigger", "favorable_house", "natal_significator", "dasha_support"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN026",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Transit over natal planets: When a transiting planet passes over a natal planet's "
            "degree, it activates that natal planet's significations. "
            "Jupiter transiting natal Venus = marriage/pleasure events."
        ),
        confidence=0.86,
        verse="BPHS Ch.90 v.87-90",
        tags=["transit", "natal_degree_trigger", "planet_activation", "exact_transit"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN027",
        source="BPHS",
        chapter="Ch.90",
        school="parashari",
        category="transit",
        description=(
            "Transit over dasha lord natal position: When the slow planet (Jupiter, Saturn) "
            "transits over the natal degree of the current dasha lord, "
            "it activates the dasha's themes most intensely."
        ),
        confidence=0.85,
        verse="BPHS Ch.90 v.91-94",
        tags=["transit", "dasha_lord_natal", "dasha_activation", "slow_planet"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN028",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Moon's monthly transit trigger: Moon transiting over the natal position "
            "of the current dasha lord activates daily/weekly events. "
            "Moon conjunct dasha lord = peak of dasha's themes in that fortnight."
        ),
        confidence=0.83,
        verse="SC Ch.10 v.41-44",
        tags=["transit", "moon_monthly", "dasha_lord_trigger", "short_term"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN029",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Retrograde planets in transit: Retrograde planet transiting a natal planet "
            "creates a three-pass transit (direct, retrograde, direct again). "
            "Events signified by the natal planet occur three times or extend in time."
        ),
        confidence=0.84,
        verse="SC Ch.10 v.45-48",
        tags=["transit", "retrograde_transit", "three_pass", "extended_events"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="TRN030",
        source="SarvarthaChintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="transit",
        description=(
            "Tajika / Solar Return transit: The solar return chart (when Sun returns "
            "to natal degree each year) governs the year's events. "
            "Planets in the solar return 1st, 10th, or 11th = active themes for that year."
        ),
        confidence=0.82,
        verse="SC Ch.10 v.49-52",
        tags=["transit", "tajika", "solar_return", "annual_chart", "year_themes"],
        implemented=False,
    ),
]

for _r in _TRANSIT_RULES:
    TRANSIT_RULES_REGISTRY.add(_r)
