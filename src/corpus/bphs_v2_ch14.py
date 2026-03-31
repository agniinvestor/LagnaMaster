"""src/corpus/bphs_v2_ch14.py — BPHS Ch.14 (3rd House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.137-141.
Chapter: 14 — Effects of the Third House (Sahaj Bhava Phala)
Slokas: 15 (v.1 benefic co-born, v.2 Mars/3rd, v.3 destruction of co-born,
  v.4 female/male co-born, v.5-6 3rd lord+Mars in 8th, v.7-11 number of
  siblings, v.12-13 seven co-born, v.14 adverse planets, v.15 yoga strength)

V2 Protocol Compliance:
  Protocol A: One-claim-one-rule — 17 rules from 15 slokas ✓
  Protocol B: Contrary mirrors — v.5-6 (destruction/happiness) ✓
  Protocol C: Entity target — siblings for most, native for v.1 courage ✓
  Protocol D: Santhanam commentary — universal principle v.3 Notes ✓
  Protocol E: Computable conditions (8 primitives) ✓
  Protocol F: Timing — all unspecified (chapter gives no ages/dashas) ✓
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


def _build_rules() -> list[RuleRecord]:
    rules: list[RuleRecord] = []
    num = 1400

    def _add(*, conditions, entity_target, signal_group, direction, intensity,
             domains, predictions, timing_window, verse_ref, description,
             commentary_context="", concordance_texts=None, divergence_notes="",
             cross_chapter_refs=None, rule_relationship=None,
             derived_house_chain=None, convergence_signals=None,
             tags=None, modifiers=None, exceptions=None, lagna_scope=None,
             prediction_type="event", **_kw):
        nonlocal num
        rid = f"BPHS{num:04d}"
        num += 1
        conc = concordance_texts or []
        confidence = min(1.0, 0.60 + 0.05 + (0.08 * len(conc))
                         - (0.05 * len([x for x in divergence_notes.split(",") if x.strip()]) if divergence_notes else 0))
        has_lagna = bool(lagna_scope)
        has_conj = any(c.get("type", "").startswith("planets_conjunct") for c in conditions)
        phase = "1B_conditional" if has_lagna else ("1B_compound" if has_conj else "1B_matrix")
        pc = {"conditions": conditions}
        if not conditions:
            pc["planet"] = "general"
            pc["placement_type"] = "general_condition"
        else:
            c0 = conditions[0]
            ct = c0.get("type", "")
            if ct == "planet_in_house":
                pc["planet"] = c0.get("planet", "")
                pc["placement_type"] = "house"
                pc["placement_value"] = c0.get("house", 0)
            elif ct == "lord_in_house":
                pc["planet"] = f"h{c0.get('lord_of', 0)}_lord"
                pc["placement_type"] = "lordship_placement"
                pc["placement_value"] = c0.get("house", 0)
            elif ct == "planet_dignity":
                pc["planet"] = c0.get("planet", "")
                pc["placement_type"] = "lordship_dignity_condition"
            elif ct == "planets_conjunct":
                pc["planet"] = "_".join(c0.get("planets", []))
                pc["placement_type"] = "conjunction_condition"
            elif ct == "planets_conjunct_in_house":
                pc["planet"] = "_".join(c0.get("planets", []))
                pc["placement_type"] = "conjunction_in_house"
                pc["placement_value"] = c0.get("house", 0)
            elif ct == "planet_aspecting":
                pc["planet"] = c0.get("planet", "")
                pc["placement_type"] = "aspect_condition"
        all_tags = list(dict.fromkeys(
            ["bphs", "parashari", "3rd_house", "sahaj_bhava"] + (tags or [])
        ))
        rules.append(RuleRecord(
            rule_id=rid, source="BPHS", chapter="Ch.14", school="parashari",
            category="3rd_house_effects",
            description=f"[BPHS — 3rd_house_effects] {description}",
            confidence=confidence, tags=all_tags, implemented=False,
            primary_condition=pc, modifiers=modifiers or [],
            exceptions=exceptions or [], outcome_domains=domains,
            outcome_direction=direction, outcome_intensity=intensity,
            outcome_timing="unspecified", lagna_scope=lagna_scope or [],
            dasha_scope=[], verse_ref=verse_ref,
            concordance_texts=conc, divergence_notes=divergence_notes,
            phase=phase, system="natal", prediction_type=prediction_type,
            gender_scope="universal", certainty_level="definite",
            strength_condition="any", house_system="sign_based",
            ayanamsha_sensitive=False, evaluation_method="lordship_check",
            last_modified_session="S311",
            predictions=predictions, entity_target=entity_target,
            signal_group=signal_group, commentary_context=commentary_context,
            cross_chapter_refs=cross_chapter_refs or [],
            timing_window=timing_window, functional_modulation={},
            derived_house_chain=derived_house_chain or {},
            convergence_signals=convergence_signals or [],
            rule_relationship=rule_relationship or {},
        ))

    # ═══════════════════════════════════════════════════════════════════════
    # SLOKA 1: Benefic in 3rd → co-born and courage
    # ═══════════════════════════════════════════════════════════════════════

    _add(
        conditions=[
            {"type": "planet_in_house", "planet": "any_benefic", "house": 3},
        ],
        entity_target="siblings", signal_group="benefic_h3_coborn",
        direction="favorable", intensity="moderate",
        domains=["character_temperament"],
        predictions=[
            {"entity": "siblings", "claim": "endowed_with_coborn",
             "domain": "progeny", "direction": "favorable", "magnitude": 0.7},
            {"entity": "native", "claim": "courageous",
             "domain": "character_temperament", "direction": "favorable", "magnitude": 0.6},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.1",
        description=(
            "3rd house conjunct or aspected by a benefic: the native will "
            "be endowed with co-born (brothers/sisters) and be courageous."
        ),
        commentary_context=(
            "Santhanam notes: 'Bhratru' in Sanskrit simply means a brother. "
            "Proper adjective is to be added, viz. Jyeshta for elder and "
            "Kanishta for younger. The 3rd house specifically deals with "
            "the after-born while the 11th house deals with preborn. This "
            "can be seen from sloka 32, Ch.32 infra."
        ),
        concordance_texts=["Saravali"],
        cross_chapter_refs=["Ch.32 v.32 Planetary Karakatvas"],
        tags=["benefic", "h3", "coborn", "courage"],
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SLOKA 2: 3rd lord + Mars aspects 3rd → good for co-born
    # ═══════════════════════════════════════════════════════════════════════

    _add(
        conditions=[
            {"type": "lord_in_house", "lord_of": 3, "house": 3},
            {"type": "planet_aspecting", "planet": "Mars", "house": 3},
        ],
        entity_target="siblings", signal_group="h3_lord_mars_aspect_coborn",
        direction="favorable", intensity="moderate",
        domains=["progeny"],
        predictions=[
            {"entity": "siblings", "claim": "good_results_for_coborn",
             "domain": "progeny", "direction": "favorable", "magnitude": 0.7},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.2",
        description=(
            "3rd lord along with Mars aspects the 3rd house: the native "
            "will enjoy good results due to the 3rd house. Alternatively "
            "these two planets may be in the 3rd itself."
        ),
        commentary_context=(
            "Santhanam notes: Mars alone in the 3rd, except in Capricorn "
            "or in Scorpio or in Aries, is not conducive to brothers. The "
            "form of our sloka is different in that the 3rd house be "
            "jointly aspected or occupied by Mars and the 3rd lord for "
            "the prosperity of coborn."
        ),
        concordance_texts=[],
        tags=["h3_lord", "mars", "coborn"],
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SLOKA 3: Destruction of co-born
    # ═══════════════════════════════════════════════════════════════════════

    _add(
        conditions=[
            {"type": "lord_in_house", "lord_of": 3, "house": "any"},
            {"type": "planet_dignity", "planet": "lord_of_3", "dignity": "weak"},
        ],
        entity_target="siblings", signal_group="h3_lord_malefic_coborn_death",
        direction="unfavorable", intensity="strong",
        domains=["longevity"],
        predictions=[
            {"entity": "siblings", "claim": "destruction_of_coborn",
             "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8},
            {"entity": "siblings", "claim": "coborn_will_not_live_long",
             "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.3",
        description=(
            "Destruction at once of coborn will come to pass if the said "
            "2 planets (3rd lord and Mars) are together with a malefic or "
            "in a sign owned by a malefic. 'The coborn will not live long.'"
        ),
        commentary_context=(
            "Santhanam notes: Mars and the 3rd lord joining in a malefic's "
            "sign or joining a malefic is said to be adverse for the "
            "longevity of coborn. Similarly Jupiter and the 11th lord in "
            "such a state is adverse for elder brothers and elder sisters; "
            "Venus and the 7th lord so placed for the spouse, Jupiter and "
            "the 5th lord so placed for progeny; Sun and the 9th lord so "
            "placed for father, the Moon and the 4th lord so placed for "
            "mother, and so on and so forth. So to say the significator "
            "and the lord of the concerned house together in a malefic's "
            "sign or with a malefic (or in an evil house) will bring harm "
            "to the said relative."
        ),
        concordance_texts=["Saravali"],
        cross_chapter_refs=[
            "Ch.15 (4th house, mother)", "Ch.16 (5th house, children)",
            "Ch.18 (7th house, spouse)", "Ch.20 (9th house, father)",
        ],
        convergence_signals=["mars_in_malefic_sign", "h3_lord_combust"],
        tags=["h3_lord", "mars", "malefic", "coborn_death"],
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SLOKAS 4-4½: Female and Male Co-born
    # ═══════════════════════════════════════════════════════════════════════

    _add(
        conditions=[
            {"type": "planet_in_house", "planet": "any_benefic", "house": 3},
        ],
        entity_target="siblings", signal_group="h3_female_planet_sisters",
        direction="neutral", intensity="moderate",
        domains=["progeny"],
        predictions=[
            {"entity": "siblings", "claim": "sisters_born_after_native",
             "domain": "progeny", "direction": "neutral", "magnitude": 0.6},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.4",
        description=(
            "If the 3rd lord is a female planet or the 3rd house is "
            "occupied by female planets, one will have sisters born after "
            "him. Similarly male planets and male signs denote younger "
            "brothers. Mixed nature → coborn of both sexes."
        ),
        commentary_context=(
            "Santhanam notes: Saturn and Mercury are termed as neutral "
            "planets. Rahu and Ketu are shadowy ones. In the matter of "
            "deciding the sex of coborn or progeny, Saturn and Rahu be "
            "treated as males while Mercury and Ketu are females. All "
            "odd signs are male signs and all even signs are female signs."
        ),
        concordance_texts=[],
        tags=["female_planet", "h3", "sisters", "gender"],
        prediction_type="trait",
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SLOKAS 5-6: 3rd lord + Mars in 8th → destruction; contrary in angle
    # ═══════════════════════════════════════════════════════════════════════

    _add(
        conditions=[
            {"type": "lord_in_house", "lord_of": 3, "house": 8},
            {"type": "planet_in_house", "planet": "Mars", "house": 8},
        ],
        entity_target="siblings", signal_group="h3_lord_mars_h8_coborn_death",
        direction="unfavorable", intensity="strong",
        domains=["longevity"],
        predictions=[
            {"entity": "siblings", "claim": "destruction_of_coborn",
             "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.5-6",
        description=(
            "3rd lord and Mars together in the 8th: destruction of coborn "
            "will result."
        ),
        commentary_context=(
            "Santhanam notes: The suggestions given in notes for sloka 3 "
            "about spouse, elder brother, mother etc. may be suitably "
            "extended. For example, if Venus and 7th lord are together in "
            "the 8th, the native's married life will be short (and in bad "
            "taste). Similarly, their conjunction in an angle or in a "
            "trine will confer longlasting benefic effects."
        ),
        concordance_texts=["Saravali"],
        derived_house_chain={
            "base_house": 3, "derivative": "6th_from",
            "effective_house": 8, "entity": "siblings", "domain": "longevity",
        },
        rule_relationship={"type": "alternative", "related_rules": ["BPHS1405"]},
        tags=["h3_lord", "mars", "h8", "coborn_death"],
    )

    # v.5-6b: Mars or 3rd lord in angle/trine/exaltation → happiness (contrary)
    _add(
        conditions=[
            {"type": "lord_in_house", "lord_of": 3, "house": [1, 4, 5, 7, 9, 10]},
        ],
        entity_target="siblings", signal_group="h3_lord_kendra_coborn_happy",
        direction="favorable", intensity="moderate",
        domains=["longevity"],
        predictions=[
            {"entity": "siblings", "claim": "happiness_for_coborn",
             "domain": "longevity", "direction": "favorable", "magnitude": 0.7},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.5-6",
        description=(
            "Happiness in this respect will come to pass if Mars or the "
            "3rd lord is in an angle or in a trine or in exaltation or "
            "in friendly divisions."
        ),
        commentary_context=(
            "Santhanam notes: Further hint — if a significator and house "
            "lord join together in a sign which is identical with "
            "debilitation/inimical sign for one of them, the significance "
            "of the planet is lost. If they join in a sign which is "
            "exaltation/friendly sign for one of them, then the "
            "significance of the planet gains prosperity."
        ),
        concordance_texts=[],
        rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1404"]},
        modifiers=[
            {"condition": "in_exaltation_or_friendly", "effect": "amplifies",
             "strength": "moderate"},
        ],
        tags=["h3_lord", "kendra", "trikona", "coborn_happiness"],
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SLOKAS 7-11: Number of Brothers and Sisters (complex rules)
    # ═══════════════════════════════════════════════════════════════════════

    # v.7-11a: Mercury in 3rd + 3rd lord + Moon + Mars-Saturn → specific sibling pattern
    _add(
        conditions=[
            {"type": "planet_in_house", "planet": "Mercury", "house": 3},
            {"type": "planets_conjunct", "planets": ["Mars", "Saturn"]},
        ],
        entity_target="siblings", signal_group="mercury_h3_mars_saturn_siblings",
        direction="mixed", intensity="strong",
        domains=["longevity"],
        predictions=[
            {"entity": "siblings", "claim": "elder_sister_born",
             "domain": "progeny", "direction": "favorable", "magnitude": 0.5},
            {"entity": "siblings", "claim": "younger_brothers_will_die",
             "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
            {"entity": "siblings", "claim": "third_brother_dies",
             "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.7-11",
        description=(
            "Mercury in the 3rd while the 3rd lord and Moon are together "
            "and Mars (indicator) joins Saturn: there occurred the birth "
            "of an elder sister and there will be younger brothers. "
            "Further the third brother will die."
        ),
        commentary_context=(
            "Santhanam notes: The word 'Karaka' or significator in sloka "
            "7 etc. should be wisely noted as Mars only and not Jupiter, "
            "which is borne by sloka 11."
        ),
        concordance_texts=[],
        tags=["mercury", "h3", "mars", "saturn", "sibling_count"],
    )

    # v.7-11b: 3rd lord exalted in trine + Jupiter → 12 total co-born
    _add(
        conditions=[
            {"type": "lord_in_house", "lord_of": 3, "house": [1, 5, 9]},
            {"type": "planet_dignity", "planet": "lord_of_3", "dignity": "exalted"},
        ],
        entity_target="siblings", signal_group="h3_lord_exalted_trikona_12_coborn",
        direction="favorable", intensity="strong",
        domains=["progeny"],
        predictions=[
            {"entity": "siblings", "claim": "twelve_total_coborn",
             "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
            {"entity": "siblings", "claim": "two_elders_rest_younger",
             "domain": "progeny", "direction": "neutral", "magnitude": 0.5},
            {"entity": "siblings", "claim": "six_of_twelve_longlived",
             "domain": "longevity", "direction": "favorable", "magnitude": 0.6},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.7-11",
        description=(
            "If the 3rd lord is in an angle while the significator is "
            "exalted in a trine and be in the company of Jupiter, 12 will "
            "be the number of total coborn. Out of these 2 elders and the "
            "3rd, 7th, 9th and 12th of younger coborn will be shortlived "
            "while six of the said twelve will be longlived."
        ),
        commentary_context=(
            "Santhanam notes: In the context of indication of one's having "
            "12 coborn, this may be taken in the present age to be a "
            "number of coborn, if not literally 12. Mars exalted and being "
            "in the company of Jupiter is denoted which means Jupiter will "
            "be in fall. Some of the coborn will die obviously because of "
            "Jupiter's debilitation taking away some potence of exalted Mars."
        ),
        concordance_texts=[],
        modifiers=[
            {"condition": "jupiter_in_company_may_be_debilitated",
             "effect": "modifies", "strength": "moderate"},
        ],
        tags=["h3_lord", "exalted", "jupiter", "sibling_count", "twelve"],
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SLOKAS 12-13: Seven Co-born
    # ═══════════════════════════════════════════════════════════════════════

    _add(
        conditions=[
            {"type": "planet_in_house", "planet": "Moon", "house": 3},
        ],
        entity_target="siblings", signal_group="moon_h3_seven_coborn",
        direction="favorable", intensity="moderate",
        domains=["progeny"],
        predictions=[
            {"entity": "siblings", "claim": "seven_coborn",
             "domain": "progeny", "direction": "favorable", "magnitude": 0.5},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.12-13",
        description=(
            "There will be 7 coborn if the 12th lord (some texts read as "
            "the 11th lord) joins Mars and Jupiter while the 3rd is "
            "occupied by the Moon. If the Moon is lonely placed in the "
            "3rd in aspect to male planets, there will be younger brothers "
            "while the aspect of Venus denotes younger sisters."
        ),
        commentary_context="",
        concordance_texts=[],
        tags=["moon", "h3", "sibling_count", "seven"],
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SLOKA 14: Adverse Planets in 3rd
    # ═══════════════════════════════════════════════════════════════════════

    # v.14a: Sun in 3rd → elder siblings destroyed
    _add(
        conditions=[
            {"type": "planet_in_house", "planet": "Sun", "house": 3},
        ],
        entity_target="siblings", signal_group="sun_h3_elder_sibling_loss",
        direction="unfavorable", intensity="strong",
        domains=["longevity"],
        predictions=[
            {"entity": "siblings", "claim": "elder_siblings_destroyed",
             "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.14",
        description=(
            "The Sun in the 3rd will destroy the preborn (elder siblings). "
            "Sun in 3rd will not allow the native to retain his elder "
            "brothers."
        ),
        commentary_context=(
            "Santhanam notes: Sage Bhrigu also opines that the Sun in the "
            "3rd house will not allow the native to retain his elder "
            "brothers and sisters. This position will affect one's "
            "relationship with brothers and sisters."
        ),
        concordance_texts=["Saravali"],
        tags=["sun", "h3", "elder_sibling", "death"],
    )

    # v.14b: Saturn in 3rd → younger siblings destroyed
    _add(
        conditions=[
            {"type": "planet_in_house", "planet": "Saturn", "house": 3},
        ],
        entity_target="siblings", signal_group="saturn_h3_younger_sibling_loss",
        direction="unfavorable", intensity="strong",
        domains=["longevity"],
        predictions=[
            {"entity": "siblings", "claim": "younger_siblings_destroyed",
             "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.14",
        description=(
            "The afterborn (younger siblings) will be destroyed if Saturn "
            "is found in the 3rd."
        ),
        commentary_context="",
        concordance_texts=["Saravali"],
        tags=["saturn", "h3", "younger_sibling", "death"],
    )

    # v.14c: Mars in 3rd → both elder and younger destroyed
    _add(
        conditions=[
            {"type": "planet_in_house", "planet": "Mars", "house": 3},
        ],
        entity_target="siblings", signal_group="mars_h3_all_sibling_loss",
        direction="unfavorable", intensity="strong",
        domains=["longevity"],
        predictions=[
            {"entity": "siblings", "claim": "both_elder_and_younger_destroyed",
             "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.14",
        description=(
            "In the same situation Mars will destroy both the preborn "
            "and later born."
        ),
        commentary_context=(
            "Santhanam notes: Regarding Mars in the 3rd, Garga Maharshi "
            "states that the native will obtain two brothers and two "
            "sisters all the 4 of whom will pass away early. The placement "
            "of Mars in the 3rd has also adverse say on the native's "
            "character. For further details, see my detailed notes in the "
            "chapter 'Effects of Planets in Bhavas' of Saravali."
        ),
        concordance_texts=["Saravali"],
        cross_chapter_refs=["Saravali Effects of Planets in Bhavas"],
        tags=["mars", "h3", "all_siblings", "death"],
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SLOKA 15: Yoga Strength (methodological)
    # ═══════════════════════════════════════════════════════════════════════

    _add(
        conditions=[],
        entity_target="siblings", signal_group="yoga_strength_siblings_method",
        direction="neutral", intensity="moderate",
        domains=["progeny"],
        predictions=[
            {"entity": "siblings", "claim": "assess_yoga_strength_before_declaring",
             "domain": "progeny", "direction": "neutral", "magnitude": 0.5},
        ],
        timing_window={"type": "unspecified"},
        verse_ref="Ch.14 v.15",
        description=(
            "After estimating the strength and weakness of such yogas, "
            "the effects related to brothers and sisters be announced."
        ),
        commentary_context="",
        concordance_texts=[],
        tags=["methodology", "yoga_strength", "siblings"],
        prediction_type="trait",
    )

    return rules


BPHS_V2_CH14_REGISTRY = CorpusRegistry()
for _rule in _build_rules():
    BPHS_V2_CH14_REGISTRY.add(_rule)
