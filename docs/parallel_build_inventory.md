# Parallel Build Inventory — Systemic Duplication Map

**Created:** S317 (2026-04-06)
**Context:** Codebase has grown over 300+ sessions with organic duplication.

## Avastha: 5 modules
1. `avasthas.py` (S317) — BPHS Ch.45 authoritative. Baaladi+Jagradadi+Lajjitadi+Sayanadi.
2. `avastha_v2.py` (S39) — Now delegates to avasthas.py. Used by scoring_v3, planet_effectiveness.
3. `avastha.py` (unknown) — Separate implementation. Has Mudita/Lajjitadi.
4. `planet_avasthas.py` (S138) — Saravali/Phaladeepika. Has Deeptadi (9 states). Even-sign bug fixed S317.
5. `sayanadi_full.py` (unknown) — Full Sayanadi with Kopa/Sthira/Mudita/Kshuditha/Trashita/Prakrita.

## Aspect/Drishti: 5+ sources
1. `sputa_drishti.py` — BPHS speculum (S317) + old house-based. Authoritative.
2. `scoring_patches.py` — Has own ASPECT_STRENGTH dict + get_aspect_strength.
3. `orb_strength.py` — Another aspect computation.
4. `rule_firing.py` — Binary _SPECIAL_ASPECTS for condition matching.
5. `bphs_aspects.py` (corpus) — Aspect rules as V2 corpus entries.

## Friendship tables: 4+ duplicates
1. `dignity.py:_NAISARGIKA` — Authoritative (S317 verified against BPHS Ch.3 v.55).
2. `panchadha_maitri.py:_NAT_FRIEND_DICT/_NAT_ENEMY_DICT` — Authoritative (S317 verified).
3. `friendship.py` — Separate module, not audited.
4. `sayanadi_full.py` — Has own relationship tables.
5. Various corpus files reference relationships.

## Sign Lord: 10+ copies of same table
`_SIGN_LORD` / `_SIGN_LORDS` / `_SIGN_LORDS_BB` / `_SIGN_LORDS_NB` duplicated in:
dignity.py, rule_firing.py, bhava_bala.py, shadbala.py, avasthas.py, avastha_v2.py,
multi_axis_scoring.py, sayanadi_full.py, planetary_state.py, and more.

## Malefic/Benefic: 5+ hardcoded sets
1. `rule_firing.py` — _MALEFICS/_BENEFICS (static) + is_natural_malefic (chart-aware, S317).
2. `scoring_patches.py` — Own benefic/malefic sets.
3. `shadbala.py` — Now uses is_natural_malefic (S317).
4. `bhava_bala.py` — Now uses is_natural_malefic (S317).
5. `yogas_additions.py` — Likely has own sets.

## Shadbala: 3 modules
1. `shadbala.py` — Main (S317 major corrections). Authoritative.
2. `shadbala_patches.py` — Patches module.
3. `dig_bala.py` — Separate dig bala implementation.

## Scoring: 5 modules
1. `multi_axis_scoring.py` — R01-R23, main house scoring. Authoritative.
2. `scoring_v2.py` — V2 scorer.
3. `scoring_v3.py` — V3 scorer.
4. `scoring_patches.py` — Patches and helpers.
5. `scoring.py` — Root-level scorer.

## Consolidation Priority
1. **Sign Lord** — single canonical `SIGN_LORDS` in one place, all others import from there
2. **Friendship** — dignity.py and panchadha_maitri.py are authoritative, delete/redirect others
3. **Malefic/Benefic** — is_natural_malefic is authoritative, wire remaining consumers
4. **Avastha** — avasthas.py is BPHS authoritative, merge/redirect remaining 4 modules
5. **Aspect** — sputa_drishti.py BPHS functions are authoritative, consolidate scoring_patches
6. **Scoring** — determine which scorer is primary, document the others' purposes
