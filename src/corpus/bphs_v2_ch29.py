"""src/corpus/bphs_v2_ch29.py — BPHS Ch.29: Bhava Padas (Arudha Pada).

S314: BPHS Phase 2 — Pada-based predictions.
Slokas 1-7 are Arudha computation (methodology, not encoded).
Slokas 8-37 are pada-based predictions: 11th/12th from Pada (wealth/expenses),
7th from Pada (health/character/wealth), 2nd from Pada (status/wealth),
and Dara Pada mutual positions (relationships/career).

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.292-303.
Verse audit: data/verse_audits/ch29_audit.json (37 claims, 37 slokas).

Condition primitive: planet_in_derived_house with derivation="arudha_pada".
Every "occupied or aspected" is split into two rules (occupies + aspects)
linked by rule_relationship, preserving BPHS OR-semantics.
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.29", category="pada_effects",
    id_start=2900, session="S314", sloka_count=37,
    chapter_tags=["arudha", "pada", "jaimini"],
    entity_target="native",
    prediction_type="trait",
    min_ratio=0.5,  # 27 predictive slokas, ~39 rules; some non-computable
)


def _pada(offset: int, planet: str, mode: str, signal: str,
          direction: str, intensity: str, primary_domain: str,
          preds: list[dict], verse_ref: str, desc: str, commentary: str,
          base_house: int = 1,
          extra_conditions: list[dict] | None = None,
          modifiers: list[dict] | None = None,
          exceptions: list[str] | None = None,
          concordance: list[str] | None = None,
          rule_rel: dict | None = None,
          **kwargs) -> None:
    """Helper for planet_in_derived_house(arudha_pada) rules."""
    conds = [{"type": "planet_in_derived_house", "derivation": "arudha_pada",
              "base_house": base_house, "offset": offset,
              "planet": planet, "mode": mode}]
    if extra_conditions:
        conds.extend(extra_conditions)
    b.add(
        conditions=conds,
        signal_group=signal,
        direction=direction, intensity=intensity,
        primary_domain=primary_domain,
        predictions=preds,
        verse_ref=verse_ref,
        description=desc,
        commentary_context=commentary,
        concordance_texts=concordance or [],
        modifiers=modifiers or [],
        exceptions=exceptions or [],
        rule_relationship=rule_rel or {},
        **kwargs,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 11TH FROM LAGNA PADA — WEALTH & GAINS (Slokas 8-15, pp.298-299)
# ═══════════════════════════════════════════════════════════════════════════════

# --- C02: Benefic in 11th → virtuous wealth + happy ---

_pada(11, "any_benefic", "occupies", "pada_h11_benefic_occ_virtuous_wealth",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "wealthy_through_virtuous_means",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
       {"entity": "native", "claim": "general_happiness_and_contentment",
        "domain": "character", "direction": "favorable", "magnitude": 0.7}],
      "Ch.29 v.8-11",
      "Benefic occupying 11th from Lagna Pada: native will be happy and wealthy through virtuous means.",
      "Santhanam: The 11th from Arudha ascendant determines financial gains. A benefic here confers wealth through righteous channels. Text explicitly states 'occupied or aspected' — this rule covers occupancy; see aspects-mode sibling.",
      modifiers=[
          {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "strong"}], "effect": "amplifies",
           "target": "prediction", "strength": "strong", "scope": "local"},
          {"condition": [{"type": "planet_not_aspecting", "planet": "any_benefic", "house": "self"}], "effect": "amplifies",
           "target": "prediction", "strength": "medium", "scope": "local"},
          {"condition": [{"type": "planet_in_derived_house", "derivation": "arudha_pada", "base_house": 1, "offset": 12, "planet": "any_malefic", "mode": "occupies"}], "effect": "attenuates",
           "target": "prediction", "strength": "strong", "scope": "local"},
      ],
      rule_rel={"type": "alternative", "related_rules": ["BPHS2901"]})

_pada(11, "any_benefic", "aspects", "pada_h11_benefic_asp_virtuous_wealth",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "wealthy_through_virtuous_means",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
       {"entity": "native", "claim": "general_happiness_and_contentment",
        "domain": "character", "direction": "favorable", "magnitude": 0.7}],
      "Ch.29 v.8-11",
      "Benefic aspecting 11th from Lagna Pada: native will be happy and wealthy through virtuous means.",
      "Santhanam: Aspect variant of the 11th-from-Pada wealth rule. BPHS states 'occupied or aspected' — this preserves the aspect trigger. Inactive until engine computes aspects on derived houses.",
      modifiers=[
          {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "strong"}], "effect": "amplifies",
           "target": "prediction", "strength": "strong", "scope": "local"},
          {"condition": [{"type": "planet_not_aspecting", "planet": "any_benefic", "house": "self"}], "effect": "amplifies",
           "target": "prediction", "strength": "medium", "scope": "local"},
          {"condition": [{"type": "planet_in_derived_house", "derivation": "arudha_pada", "base_house": 1, "offset": 12, "planet": "any_malefic", "mode": "occupies"}], "effect": "attenuates",
           "target": "prediction", "strength": "strong", "scope": "local"},
      ],
      rule_rel={"type": "alternative", "related_rules": ["BPHS2900"]})

# --- C03: Malefic in 11th → questionable wealth + happy ---

_pada(11, "any_malefic", "occupies", "pada_h11_malefic_occ_questionable_wealth",
      "mixed", "strong", "wealth",
      [{"entity": "native", "claim": "wealthy_through_questionable_means",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
       {"entity": "native", "claim": "general_happiness_and_contentment",
        "domain": "character", "direction": "favorable", "magnitude": 0.7}],
      "Ch.29 v.8-11",
      "Malefic occupying 11th from Lagna Pada: native will be happy and wealthy through questionable means.",
      "Santhanam: A malefic in the 11th from Arudha confers wealth but through morally dubious channels. Direction is 'mixed' — wealth is favorable but the means are questionable.",
      modifiers=[
          {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "strong"}], "effect": "amplifies",
           "target": "prediction", "strength": "strong", "scope": "local"},
          {"condition": [{"type": "planet_in_derived_house", "derivation": "arudha_pada", "base_house": 1, "offset": 12, "planet": "any_malefic", "mode": "occupies"}], "effect": "attenuates",
           "target": "prediction", "strength": "strong", "scope": "local"},
      ],
      rule_rel={"type": "alternative", "related_rules": ["BPHS2903"]})

_pada(11, "any_malefic", "aspects", "pada_h11_malefic_asp_questionable_wealth",
      "mixed", "strong", "wealth",
      [{"entity": "native", "claim": "wealthy_through_questionable_means",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
       {"entity": "native", "claim": "general_happiness_and_contentment",
        "domain": "character", "direction": "favorable", "magnitude": 0.7}],
      "Ch.29 v.8-11",
      "Malefic aspecting 11th from Lagna Pada: native will be happy and wealthy through questionable means.",
      "Santhanam: Aspect variant. Inactive until engine computes aspects on derived houses.",
      modifiers=[
          {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "strong"}], "effect": "amplifies",
           "target": "prediction", "strength": "strong", "scope": "local"},
      ],
      rule_rel={"type": "alternative", "related_rules": ["BPHS2902"]})

# --- C04: Both benefic and malefic in 11th → wealth through both means ---

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "any_benefic", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "any_malefic", "mode": "occupies"},
    ],
    signal_group="pada_h11_both_occ_dual_wealth",
    direction="mixed", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealthy_through_both_virtuous_and_questionable_means",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
        {"entity": "native", "claim": "general_happiness_and_contentment",
         "domain": "character", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.29 v.8-11",
    description="Both benefic and malefic occupying 11th from Lagna Pada: wealth through both virtuous and questionable means.",
    commentary_context="Santhanam: When both a benefic and a malefic occupy the 11th from Arudha, wealth comes through both fair and unfair channels. The dual nature of the influence is reflected in the 'mixed' direction.",
    concordance_texts=[],
)


# ═══════════════════════════════════════════════════════════════════════════════
# 12TH FROM LAGNA PADA — EXPENSES & LOSSES (Slokas 16-21, pp.299-300)
# ═══════════════════════════════════════════════════════════════════════════════

# --- C11: Both benefic + malefic aspecting 12th → abundant earnings + expenses ---

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 12, "planet": "any_benefic", "mode": "aspects"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 12, "planet": "any_malefic", "mode": "aspects"},
    ],
    signal_group="pada_h12_both_asp_earnings_expenses",
    direction="mixed", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "abundant_earnings",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
        {"entity": "native", "claim": "plenty_of_expenses",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.29 v.16-17",
    description="Both benefic and malefic aspecting 12th from Lagna Pada: abundant earnings but plenty of expenses.",
    commentary_context="Santhanam: When both benefics and malefics aspect the 12th from Arudha, the native earns abundantly but spends equally. The net wealth effect depends on relative strengths. In the standard nativity, the 12th from Arudha (Pisces) is aspected by Mars (8th aspect) — hence expenses are equally high.",
    concordance_texts=[],
)

# --- C12: Benefic aspecting 12th → fair expenses ---

_pada(12, "any_benefic", "aspects", "pada_h12_benefic_asp_fair_expenses",
      "unfavorable", "moderate", "wealth",
      [{"entity": "native", "claim": "expenses_through_fair_means",
        "domain": "wealth", "direction": "unfavorable", "magnitude": 0.5}],
      "Ch.29 v.16-17",
      "Benefic aspecting 12th from Lagna Pada: expenses through fair means.",
      "Santhanam: The benefic nature ensures expenses go to righteous causes — charity, religious activities, family obligations. The expenditure itself is not avoidable but its nature is virtuous.")

# --- C13: Malefic aspecting 12th → unfair expenses ---

_pada(12, "any_malefic", "aspects", "pada_h12_malefic_asp_unfair_expenses",
      "unfavorable", "moderate", "wealth",
      [{"entity": "native", "claim": "expenses_through_unfair_means",
        "domain": "wealth", "direction": "unfavorable", "magnitude": 0.5}],
      "Ch.29 v.16-17",
      "Malefic aspecting 12th from Lagna Pada: expenses through unfair means.",
      "Santhanam: A malefic aspecting the 12th from Arudha causes expenses through litigation, penalties, vices, or wrongful dealings.")

# --- C14: Sun+Venus+Rahu in 12th → loss through authority ---

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 12, "planet": "sun", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 12, "planet": "venus", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 12, "planet": "rahu", "mode": "occupies"},
    ],
    signal_group="pada_h12_sun_venus_rahu_occ_loss_authority",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "loss_of_wealth_through_authority",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.29 v.18",
    description="Sun, Venus, and Rahu conjunct in 12th from Lagna Pada: loss of wealth through the king (authority).",
    commentary_context="Santhanam: The conjunction of Sun (government), Venus (luxury), and Rahu (deception) in the 12th from Arudha signals losses through government action, legal penalties, or confiscation. The audit originally placed this as 'conjunct Lagna Pada' but the text clearly says '12th from Lagna Pada.'",
    concordance_texts=[],
    modifiers=[
        {"condition": "moon_aspecting_12th_from_pada", "effect": "amplifies",
         "target": "prediction", "strength": "strong", "scope": "local"},
    ],
)

# --- C16: Mercury in 12th with benefic → expenses through paternal relatives ---

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 12, "planet": "mercury", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 12, "planet": "any_benefic", "mode": "occupies"},
    ],
    signal_group="pada_h12_mercury_benefic_occ_paternal_expenses",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "expenses_through_paternal_relatives",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.29 v.19",
    description="Mercury in 12th from Lagna Pada with benefic: expenses through paternal relatives.",
    commentary_context="Santhanam: Mercury (communication, commerce) combined with a benefic in the 12th from Arudha channels expenses through the father's side — support obligations, inheritance matters, family business losses. The benefic mitigates severity but not occurrence.",
    concordance_texts=[],
)

# --- C17: Malefic Mercury in 12th → loss through disputes ---

_pada(12, "mercury", "occupies", "pada_h12_mercury_malefic_occ_disputes",
      "unfavorable", "moderate", "wealth",
      [{"entity": "native", "claim": "loss_of_wealth_through_disputes",
        "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6}],
      "Ch.29 v.19",
      "Mercury (as malefic) in 12th from Lagna Pada: loss of wealth through disputes.",
      "Santhanam: When Mercury acts as a malefic (conjunct malefic or in malefic association), placement in the 12th from Arudha causes losses through litigation, arguments, and contractual disputes. Mercury is treated as malefic when conjunct a malefic.",
      extra_conditions=[
          {"type": "planet_in_derived_house", "derivation": "arudha_pada",
           "base_house": 1, "offset": 12, "planet": "any_malefic", "mode": "occupies"},
      ])

# --- C18: Jupiter in 12th aspected → expenses through taxes ---

_pada(12, "jupiter", "occupies", "pada_h12_jupiter_occ_tax_expenses",
      "unfavorable", "moderate", "wealth",
      [{"entity": "native", "claim": "expenses_through_taxes_and_self",
        "domain": "wealth", "direction": "unfavorable", "magnitude": 0.5}],
      "Ch.29 v.20",
      "Jupiter in 12th from Lagna Pada aspected by others: expenses through taxes on one's own.",
      "Santhanam: Jupiter (dharma, expansion) in the 12th from Arudha with aspects from other planets causes expenses through taxation, religious donations, or obligations to institutions. The 'aspected by others' clause suggests the effect needs external activation.")

# --- C19: Saturn+Mars in 12th → expenses through co-born ---

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 12, "planet": "saturn", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 12, "planet": "mars", "mode": "occupies"},
    ],
    signal_group="pada_h12_saturn_mars_occ_coborn_expenses",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "expenses_through_coborn",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.29 v.21",
    description="Saturn and Mars conjunct in 12th from Lagna Pada aspected by others: expenses through co-born (siblings).",
    commentary_context="Santhanam: Saturn (restriction, delays) combined with Mars (aggression, competition) in the 12th from Arudha signals expenses caused by siblings — financial support, joint property disputes, sibling-related obligations.",
    concordance_texts=[],
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKA 22 MIRRORS — 11TH FROM PADA SOURCE-SPECIFIC GAINS (p.300)
# "Whatever sources of expenses are indicated for 12th, gains through
#  similar sources will occur if the 11th house so features."
# ═══════════════════════════════════════════════════════════════════════════════

# --- C34: Sun+Venus+Rahu in 11th → gains from authority (mirror of C14) ---

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "sun", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "venus", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "rahu", "mode": "occupies"},
    ],
    signal_group="pada_h11_sun_venus_rahu_occ_authority_gains",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "gains_from_authority_or_government",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.29 v.22",
    description="Sun, Venus, and Rahu conjunct in 11th from Lagna Pada: gains from authority/government.",
    commentary_context="Santhanam: Sloka 22 explicitly states that whatever sources cause expenses in the 12th from Pada will cause gains if present in the 11th. This mirrors the loss-through-authority rule (v.18) to gains through authority.",
    concordance_texts=[],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2908"]},
)

# --- C35: Mercury in 11th with benefic → gains through paternal relatives ---

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "mercury", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "any_benefic", "mode": "occupies"},
    ],
    signal_group="pada_h11_mercury_benefic_occ_paternal_gains",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "gains_through_paternal_relatives",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.29 v.22",
    description="Mercury with benefic in 11th from Lagna Pada: gains through paternal relatives.",
    commentary_context="Santhanam: Mirror of v.19 expense rule. Mercury + benefic in the 11th from Arudha channels gains through father's family — inheritance, family business profits, paternal support.",
    concordance_texts=[],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2909"]},
)

# --- C36: Jupiter in 11th → gains through taxes/self ---

_pada(11, "jupiter", "occupies", "pada_h11_jupiter_occ_tax_gains",
      "favorable", "moderate", "wealth",
      [{"entity": "native", "claim": "gains_through_taxes_or_institutional_sources",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.5}],
      "Ch.29 v.22",
      "Jupiter in 11th from Lagna Pada: gains through taxes, institutional sources, or one's own efforts.",
      "Santhanam: Mirror of v.20 expense rule. Jupiter in the 11th from Arudha brings income through tax benefits, institutional employment, religious endowments, or self-directed enterprise.",
      rule_rel={"type": "contrary_mirror", "related_rules": ["BPHS2911"]})

# --- C37: Saturn+Mars in 11th → gains through co-born ---

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "saturn", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "mars", "mode": "occupies"},
    ],
    signal_group="pada_h11_saturn_mars_occ_coborn_gains",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "gains_through_coborn",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.29 v.22",
    description="Saturn and Mars conjunct in 11th from Lagna Pada: gains through co-born (siblings).",
    commentary_context="Santhanam: Mirror of v.21 expense rule. Saturn + Mars in the 11th from Arudha brings income through siblings — joint ventures, sibling-provided opportunities, shared property gains.",
    concordance_texts=[],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2912"]},
)


# ═══════════════════════════════════════════════════════════════════════════════
# 7TH FROM LAGNA PADA — HEALTH, CHARACTER, WEALTH (Slokas 23-26, p.301)
# ═══════════════════════════════════════════════════════════════════════════════

# --- C20: Rahu in 7th from Pada → stomachial disorders or fire ---

_pada(7, "rahu", "occupies", "pada_h7_rahu_occ_stomach_fire",
      "unfavorable", "moderate", "health",
      [{"entity": "native", "claim": "stomachial_disorders",
        "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
       {"entity": "native", "claim": "trouble_by_fire",
        "domain": "health", "direction": "unfavorable", "magnitude": 0.7}],
      "Ch.29 v.23",
      "Rahu in 7th from Lagna Pada: native troubled by stomachial disorders or fire.",
      "Santhanam: Rahu in the 7th from Arudha disrupts digestive health and creates vulnerability to fire-related accidents or fevers. The 'or' indicates either manifestation, not necessarily both.")

# --- C20b: Ketu in 7th from Pada → stomachial disorders or fire ---

_pada(7, "ketu", "occupies", "pada_h7_ketu_occ_stomach_fire",
      "unfavorable", "moderate", "health",
      [{"entity": "native", "claim": "stomachial_disorders",
        "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
       {"entity": "native", "claim": "trouble_by_fire",
        "domain": "health", "direction": "unfavorable", "magnitude": 0.7}],
      "Ch.29 v.23",
      "Ketu in 7th from Lagna Pada: native troubled by stomachial disorders or fire.",
      "Santhanam: Text says 'Rahu or Ketu' — either node in the 7th from Arudha triggers this. Ketu's nature (headless, fire-element) aligns with both digestive issues and fire hazards.",
      rule_rel={"type": "alternative", "related_rules": ["BPHS2917"]})

# --- C21+C22: Ketu in 7th with malefic → adventurous + grey hair + physical ---

_pada(7, "ketu", "occupies", "pada_h7_ketu_malefic_occ_adventurous",
      "mixed", "moderate", "character",
      [{"entity": "native", "claim": "adventurous",
        "domain": "character", "direction": "favorable", "magnitude": 0.7},
       {"entity": "native", "claim": "prematurely_grey_hair",
        "domain": "health", "direction": "unfavorable", "magnitude": 0.5},
       {"entity": "native", "claim": "large_male_organ",
        "domain": "character", "direction": "neutral", "magnitude": 0.5}],
      "Ch.29 v.24",
      "Ketu in 7th from Lagna Pada with malefic aspect or conjunction: native will be adventurous, with premature grey hair and large male organ.",
      "Santhanam: Ketu combined with malefic influence in the 7th from Arudha produces a bold, risk-taking temperament alongside premature aging signs. The physical predictions are gender-specific (male). The 'adventurous' quality is generally favorable while the physical effects are neutral/mixed.",
      extra_conditions=[
          {"type": "planet_in_derived_house", "derivation": "arudha_pada",
           "base_house": 1, "offset": 7, "planet": "any_malefic", "mode": "occupies"},
      ],
      )

# --- C23: Jupiter in 7th → very wealthy ---

_pada(7, "jupiter", "occupies", "pada_h7_jupiter_occ_wealthy",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "very_wealthy",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      "Ch.29 v.25",
      "Jupiter in 7th from Lagna Pada: native will be very wealthy.",
      "Santhanam: Text says 'one, two or all three of Jupiter, Venus and the Moon in the 7th' — each independently triggers wealth. Jupiter in the 7th from Arudha is the strongest wealth indicator in Pada analysis.",
      rule_rel={"type": "alternative", "related_rules": ["BPHS2921", "BPHS2922"]})

_pada(7, "venus", "occupies", "pada_h7_venus_occ_wealthy",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "very_wealthy",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      "Ch.29 v.25",
      "Venus in 7th from Lagna Pada: native will be very wealthy.",
      "Santhanam: Venus in the 7th from Arudha signals wealth through luxury, comfort, and Venusian enterprises.",
      rule_rel={"type": "alternative", "related_rules": ["BPHS2920", "BPHS2922"]})

_pada(7, "moon", "occupies", "pada_h7_moon_occ_wealthy",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "very_wealthy",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      "Ch.29 v.25",
      "Moon in 7th from Lagna Pada: native will be very wealthy.",
      "Santhanam: Moon in the 7th from Arudha — public perception of prosperity, popular support, wealth through masses/public.",
      rule_rel={"type": "alternative", "related_rules": ["BPHS2920", "BPHS2921"]})

# --- C24: Benefic or malefic exalted in 7th → affluent + famous ---

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 7, "planet": "any_planet", "mode": "occupies"},
        {"type": "planet_dignity", "planet": "any_planet", "dignity": "exalted"},
    ],
    signal_group="pada_h7_exalted_occ_affluent_famous",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "affluent_and_prosperous",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.8},
        {"entity": "native", "claim": "widespread_fame_and_recognition",
         "domain": "career", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.29 v.26",
    description="Benefic or malefic exalted in 7th from Lagna Pada: native will be affluent and famous.",
    commentary_context="Santhanam: Text says 'whether a benefic or a malefic if be exalted in the 7th' — exaltation state is the trigger, not planet identity. The planet's exalted status overrides natural benefic/malefic distinction. Exaltation is encoded as a structured condition (planet_dignity), not just a modifier. GPT review: this rule captures state + house, not planet identity.",
    concordance_texts=[],
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKA 27 MIRRORS — 2ND FROM PADA APPLIES 7TH-FROM-PADA RULES (p.301)
# "These yogas narrated with reference to the 7th from Lagna Pada
#  be also considered from the 2nd of Lagna Pada."
# ═══════════════════════════════════════════════════════════════════════════════

_pada(2, "rahu", "occupies", "pada_h2_rahu_occ_stomach_fire",
      "unfavorable", "moderate", "health",
      [{"entity": "native", "claim": "stomachial_disorders",
        "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
       {"entity": "native", "claim": "trouble_by_fire",
        "domain": "health", "direction": "unfavorable", "magnitude": 0.7}],
      "Ch.29 v.27",
      "Rahu in 2nd from Lagna Pada: stomachial disorders or fire trouble (mirror of 7th-from-Pada rule).",
      "Santhanam: Sloka 27 explicitly instructs applying 7th-from-Pada rules to the 2nd from Pada as well. This mirrors the Rahu-in-7th health prediction.",
      rule_rel={"type": "addition", "related_rules": ["BPHS2917"]})

_pada(2, "ketu", "occupies", "pada_h2_ketu_occ_stomach_fire",
      "unfavorable", "moderate", "health",
      [{"entity": "native", "claim": "stomachial_disorders",
        "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
       {"entity": "native", "claim": "trouble_by_fire",
        "domain": "health", "direction": "unfavorable", "magnitude": 0.7}],
      "Ch.29 v.27",
      "Ketu in 2nd from Lagna Pada: stomachial disorders or fire trouble (mirror of 7th-from-Pada rule).",
      "Santhanam: Sloka 27 mirror. Ketu in the 2nd from Arudha — same health effects as 7th placement.",
      rule_rel={"type": "addition", "related_rules": ["BPHS2918"]})

_pada(2, "jupiter", "occupies", "pada_h2_jupiter_occ_wealthy",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "very_wealthy",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      "Ch.29 v.27",
      "Jupiter in 2nd from Lagna Pada: native will be very wealthy (mirror of 7th-from-Pada rule).",
      "Santhanam: Sloka 27 mirror. Jupiter in the 2nd from Arudha — wealth through accumulated resources, speech, and family.",
      rule_rel={"type": "addition", "related_rules": ["BPHS2920"]})

_pada(2, "venus", "occupies", "pada_h2_venus_occ_wealthy",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "very_wealthy",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      "Ch.29 v.27",
      "Venus in 2nd from Lagna Pada: native will be very wealthy (mirror of 7th-from-Pada rule).",
      "Santhanam: Sloka 27 mirror. Venus in the 2nd from Arudha — wealth through beauty, arts, luxury goods.",
      rule_rel={"type": "addition", "related_rules": ["BPHS2921"]})

_pada(2, "moon", "occupies", "pada_h2_moon_occ_wealthy",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "very_wealthy",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      "Ch.29 v.27",
      "Moon in 2nd from Lagna Pada: native will be very wealthy (mirror of 7th-from-Pada rule).",
      "Santhanam: Sloka 27 mirror. Moon in the 2nd from Arudha — wealth through public, emotional intelligence, maternal family.",
      rule_rel={"type": "addition", "related_rules": ["BPHS2922"]})


# ═══════════════════════════════════════════════════════════════════════════════
# 2ND FROM LAGNA PADA — SPECIFIC PREDICTIONS (Slokas 28, 30-37, pp.301-303)
# ═══════════════════════════════════════════════════════════════════════════════

# --- C25: Mercury/Jupiter/Venus exalted in 2nd → rich ---

_pada(2, "mercury", "occupies", "pada_h2_mercury_exalted_occ_rich",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "rich_through_accumulated_wealth",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      "Ch.29 v.28",
      "Mercury exalted in 2nd from Lagna Pada with strength: native will be rich.",
      "Santhanam: Text says 'anyone of Mercury, Jupiter and Venus be exalted in the 2nd from Lagna Pada and be with strength.' Exaltation is a gating condition — the rule only fires when the planet is in exalted dignity.",
      modifiers=[
          {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "exalted"}], "effect": "gates",
           "target": "rule", "strength": "strong", "scope": "local"},
      ],
      rule_rel={"type": "alternative", "related_rules": ["BPHS2932", "BPHS2933"]})

_pada(2, "jupiter", "occupies", "pada_h2_jupiter_exalted_occ_rich",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "rich_through_accumulated_wealth",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      "Ch.29 v.28",
      "Jupiter exalted in 2nd from Lagna Pada with strength: native will be rich.",
      "Santhanam: Jupiter exalted in the 2nd from Arudha is the strongest single-planet wealth indicator in Pada analysis. The 'with strength' clause implies Shadbala or dignity-based confirmation.",
      modifiers=[
          {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "exalted"}], "effect": "gates",
           "target": "rule", "strength": "strong", "scope": "local"},
      ],
      rule_rel={"type": "alternative", "related_rules": ["BPHS2931", "BPHS2933"]})

_pada(2, "venus", "occupies", "pada_h2_venus_exalted_occ_rich",
      "favorable", "strong", "wealth",
      [{"entity": "native", "claim": "rich_through_accumulated_wealth",
        "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      "Ch.29 v.28",
      "Venus exalted in 2nd from Lagna Pada with strength: native will be rich.",
      "Santhanam: Venus exalted in the 2nd from Arudha — wealth through Venusian channels (arts, luxury, beauty) with accumulation (2nd house = dhana).",
      modifiers=[
          {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "exalted"}], "effect": "gates",
           "target": "rule", "strength": "strong", "scope": "local"},
      ],
      rule_rel={"type": "alternative", "related_rules": ["BPHS2931", "BPHS2932"]})

# --- C26: Mercury in 2nd → lord over country ---

_pada(2, "mercury", "occupies", "pada_h2_mercury_occ_lord_country",
      "favorable", "strong", "career",
      [{"entity": "native", "claim": "lord_over_whole_country",
        "domain": "career", "direction": "favorable", "magnitude": 0.9}],
      "Ch.29 v.30-37",
      "Mercury in 2nd from Arudha Lagna: native will lord over the whole country.",
      "Santhanam: Mercury in the 2nd from Arudha — administrative authority, eloquence in governance, command through intellectual capacity. 'Lord over the whole country' indicates highest level of professional authority.")

# --- C27: Venus in 2nd → poet/speaker ---

_pada(2, "venus", "occupies", "pada_h2_venus_occ_poet_speaker",
      "favorable", "moderate", "career",
      [{"entity": "native", "claim": "poet_or_speaker",
        "domain": "career", "direction": "favorable", "magnitude": 0.6}],
      "Ch.29 v.30-37",
      "Venus in 2nd from Lagna Pada: native will be a poet or speaker.",
      "Santhanam: Venus in the 2nd from Arudha — creative expression through speech, writing, and artistic communication. The 2nd house governs speech (vak sthana), and Venus adds aesthetic quality.")


# ═══════════════════════════════════════════════════════════════════════════════
# DARA PADA MUTUAL POSITIONS — RELATIONSHIPS & STATUS (Slokas 30-37, pp.302-303)
# These require a derived_house_relationship primitive not yet implemented.
# Encoded as L2 rules with descriptive conditions for corpus completeness.
# ═══════════════════════════════════════════════════════════════════════════════

# --- C28: Dara Pada in angle/trine from Lagna Pada → rich + famous ---

b.add(
    conditions=[
        {"type": "derived_points_relationship",
         "point_a": {"derivation": "arudha_pada", "house": 1},
         "point_b": {"derivation": "arudha_pada", "house": 7},
         "relationship": "kendra_trikona"},
    ],
    signal_group="dara_pada_kendra_trikona_rich_famous",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "rich_and_famous_in_country",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
        {"entity": "native", "claim": "famous_in_country",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.29 v.30-37",
    description="Dara Pada (7th house Arudha) in angle or trine from Lagna Pada, or both have strong planets: native will be rich and famous.",
    commentary_context="Santhanam: The mutual angular/trinal relationship between Lagna Pada and Dara Pada (Arudha of 7th) with strong planetary support indicates public recognition and wealth. Requires derived_house_relationship primitive — currently non-computable.",
    concordance_texts=[],
)

# --- C29: Dara Pada in 6/8/12 from Lagna Pada → poor ---

b.add(
    conditions=[
        {"type": "derived_points_relationship",
         "point_a": {"derivation": "arudha_pada", "house": 1},
         "point_b": {"derivation": "arudha_pada", "house": 7},
         "relationship": "dusthana"},
    ],
    signal_group="dara_pada_dusthana_poor",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "poverty_and_lack_of_resources",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.29 v.30-37",
    description="Dara Pada in 6th, 8th, or 12th from Lagna Pada: native will be poor.",
    commentary_context="Santhanam: When the 7th house Arudha falls in dusthana from Lagna Pada, the native lacks public standing and accumulation. Requires derived_house_relationship primitive.",
    concordance_texts=[],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2937"]},
)

# --- C30: Strong planet in Pada and 7th → marital happiness ---

b.add(
    conditions=[
        {"type": "planet_at_derived_point", "derivation": "arudha_pada", "base_house": 1, "offset": 1, "dignity": "strong"},
        {"type": "planet_at_derived_point", "derivation": "arudha_pada", "base_house": 1, "offset": 7, "dignity": "strong"},
    ],
    signal_group="pada_h1_h7_strong_marital_happiness",
    direction="favorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "happiness_between_husband_and_wife",
         "domain": "relationships", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.29 v.30-37",
    description="Lagna Pada and 7th from it occupied by strong planet: happiness between husband and wife.",
    commentary_context="Santhanam: When both the Arudha Lagna itself and its 7th house have strong planetary occupants, marital harmony is indicated. 'Strong' implies dignity or Shadbala — requires strength evaluation primitive.",
    concordance_texts=[],
)

# --- C31: Pada and Dara Pada mutually angular/trinal → amity ---

b.add(
    conditions=[
        {"type": "derived_points_relationship",
         "point_a": {"derivation": "arudha_pada", "house": 1},
         "point_b": {"derivation": "arudha_pada", "house": 7},
         "relationship": "kendra_trikona"},
    ],
    signal_group="pada_dara_pada_kendra_trikona_amity",
    direction="favorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "amity_between_couple",
         "domain": "relationships", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.29 v.30-37",
    description="Lagna Pada and Dara Pada mutually angular or trinal: amity between couple.",
    commentary_context="Santhanam: Angular or trinal mutual placement of the two Padas indicates harmony, shared goals, and mutual support between spouses.",
    concordance_texts=[],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2941"]},
)

# --- C32: Pada and Dara Pada mutually 6/8/12 → enmity ---

b.add(
    conditions=[
        {"type": "derived_points_relationship",
         "point_a": {"derivation": "arudha_pada", "house": 1},
         "point_b": {"derivation": "arudha_pada", "house": 7},
         "relationship": "dusthana"},
    ],
    signal_group="pada_dara_pada_dusthana_enmity",
    direction="unfavorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "enmity_between_couple",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.29 v.30-37",
    description="Lagna Pada and Dara Pada mutually 6th, 8th, or 12th: enmity between couple.",
    commentary_context="Santhanam: Dusthana mutual placement of the two Padas indicates discord, conflict, and incompatibility between spouses.",
    concordance_texts=[],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2940"]},
)

# --- C33: Pada and Dara Pada mutually angular/3rd/11th/trinal → king ---

b.add(
    conditions=[
        {"type": "derived_points_relationship",
         "point_a": {"derivation": "arudha_pada", "house": 1},
         "point_b": {"derivation": "arudha_pada", "house": 7},
         "relationship": "kendra_trikona_upachaya"},
    ],
    signal_group="pada_dara_pada_supportive_king",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "king_ruling_earth",
         "domain": "career", "direction": "favorable", "magnitude": 0.9},
    ],
    verse_ref="Ch.29 v.30-37",
    description="Lagna Pada and Dara Pada mutually angular, 3rd/11th, or trinal: native will be a king ruling the earth.",
    commentary_context="Santhanam: The strongest mutual placement between Lagna Pada and Dara Pada produces the highest career outcome. The 3rd/11th addition (upachaya) strengthens beyond simple kendra/trikona. 'King ruling earth' = apex of professional/political authority in modern context.",
    concordance_texts=[],
)


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

BPHS_V2_CH29_REGISTRY = b.build()
