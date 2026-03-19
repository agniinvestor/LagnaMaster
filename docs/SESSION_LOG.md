# LagnaMaster — Session Log

> Last updated: 2026-03-20 | Sessions 1–32

## Sessions 1–27 — See git history (657 tests)

## Session 28 — Functional Roles
**Tests**: 9 | **Cumulative**: 666

`src/calculations/functional_roles.py` — per-lagna functional role matrix.
Computes: functional benefics/malefics/neutrals (lagna-specific), yogakarakas (kendra+trikona dual lordship), badhaka house/sign/lord (moveable=H11, fixed=H9, dual=H7), maraka lords (H2+H7), dusthana lords (H6+H8+H12), kendradhipati dosha candidates. For Taurus lagna: Saturn is yogakaraka (H9+H10), badhaka=H9 (fixed sign). FunctionalRoles dataclass with helper methods is_yogakaraka(), is_maraka(), is_functional_malefic().

## Session 29 — Avastha Systems
**Tests**: 6 | **Cumulative**: 672

`src/calculations/avastha.py` — three classical state systems.
Deeptadi (6 states: Deepta/Swastha/Mudita/Shanta/Dukha/Kshobhita mapped from DignityLevel). Baladi (5 states by degree: Bala 0-6°, Kumara 6-12°, Yuva 12-18° peak, Vriddha 18-24°, Mrita 24-30°). Lajjitadi: 5th lord state — Lajjita (highest pressure, 1.0) when in dusthana with malefics/combust; Kshobhita (0.8) with nodes/combust; Kshudhita (0.7) dusthana alone; Trushita (0.4) dusthana with benefic; Garvita (0.0) exalted in kendra; Mudita (0.0) with benefic. AvasthaReport combines all three with effective_multipliers (deeptadi×baladi per planet).

## Session 30 — Life Pressure Index Engine
**Tests**: 9 | **Cumulative**: 681

`src/calculations/pressure_engine.py` — the central missing capability.

Formula: PressureIndex = (structural_vulnerability/10) × dasha_activation × transit_load / resilience × 10

Component details:
- structural_vulnerability: Moon debil/combust (+2/1.5), Saturn-Moon conjunction (+2), Moon aspect (+1), badhaka lord in kendra (+1.5), functional malefics in kendras (+0.5 each), dusthana interlocking (+1), Lajjita 5th lord (+2)
- dasha_activation_weight: base 1.0, +0.25 per functional malefic lord, +0.4 badhaka lord, +0.2 maraka lord, +0.25 dusthana placement, -0.3 yogakaraka dasha
- transit_load: Sade Sati Peak +0.6/Rising +0.3/Setting +0.2, Saturn over Lagna +0.4, Rahu over Moon/Lagna +0.3, Mars over Moon +0.2, malefic cluster +0.3
- resilience: Jupiter Shadbala >300V +0.3/<150V -0.2, yogakaraka dasha +0.25, Jupiter in kendra from Moon transit +0.3

PressurePoint dataclass with is_critical (≥7.5) and is_elevated (≥5.0) properties.
compute_pressure_timeline() steps through any date range at configurable monthly intervals.

## Session 31 — Argala + Arudha Lagna
**Tests**: 5 | **Cumulative**: 686

`src/calculations/argala.py` — Jaimini obstruction model.

Argala houses from reference: H2 (primary, opposed by H12), H4 (primary, opposed by H10), H11 (primary, opposed by H3), H5 (secondary, opposed by H9). Virodhargala cancels when obstruction planet count ≥ argala planet count. net_argala_score: +0.5 per unobstructed benefic argala planet, -0.5 per unobstructed malefic argala planet.

Arudha Lagna: count from lagna to lagna lord, project equal distance from lagna lord. Exception: AL on lagna or 7th → move +10 signs. Condition: Afflicted (malefics on AL, reputational pressure), Strong, Mixed, Neutral.

## Session 32 — Graha Yuddha + Scoring Engine v2
**Tests**: 7 | **Cumulative**: 693

Wait — 9+6+9+5+7=36, 657+36=693. Corrected: **693/693**.

`src/calculations/graha_yuddha.py`: Planetary war detection for 5 non-luminary planets. War condition: same sign, within 1° longitude. Loser = lesser longitude. Functional impact: loser's benefic rule scores penalized 50% in v2 engine.

`src/calculations/scoring_v2.py`: Scoring Engine v2. ENGINE_VERSION="2.0.0". Changes from v1: functional (lagna-specific) benefic/malefic classification throughout; Graha Yuddha losers give 50% benefic score; HouseScoreV2 has functional_malefic_bhavesh flag and yuddha_losers_penalized list. RuleResultV2 carries engine_version. score_chart_v2() → ChartScoresV2 with engine_version and yuddha_results.
