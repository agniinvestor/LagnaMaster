# CLASSICAL_CORPUS.md — Classical Knowledge Status
> **Update this file as texts are encoded and corpus grows.**
> Phase 1 (S216–S410) is the most critical phase in the project.

---

## Core Insight (Revised After Corpus Quality Audit — S262)

> "Sessions S216–S262 produced 2,634 rules labeled 'exhaustive' that were actually
> representative samplings — undershooting true text depth by 5.7× on average.
> A rule with only a prose description is a catalog entry, not a structured prediction.
> Phase 1B replaces count targets with coverage maps and replaces descriptions with
> machine-readable condition/outcome pairs."

**Phase 1A (S216–S262) is complete and relabeled: Representative Layer — 2,634 rules.**
**Phase 1B (S263+) is the research-grade corpus — target ~9,200 structured predictions.**

The distinction matters for every downstream use:
- Phase 1A: valid as a topic index and breadth coverage check
- Phase 1B: required for SHAP analysis, concordance scoring, and feature engineering

---

## Phase 1A — Representative Layer (COMPLETE, S216–S262)

Phase 1A is the breadth pass. It is complete and should not be extended. Its function
is a coverage index — confirming which topics each text addresses. It is not suitable
as primary ML input because its rules are prose descriptions, not structured predictions.

| Metric | Actual |
|--------|--------|
| Total rules | 2,634 (corpus 2514 + 120 PHX from S262) |
| Tests passing | 2,227 |
| Files | 49 source files across `src/corpus/` |
| Rule structure | Prose descriptions — `category`, `description`, `tags` only |
| Verse attribution | Chapter-level only (not verse-specific) |
| Outcome structure | None — all outcomes in prose `description` field |
| Concordance | None — no cross-text linking |
| Lagna scope | Implicit — no `lagna_scope` field |
| ML readiness | Not directly; requires Phase 1B structured layer |

**Phase 1A files encode (representative, not exhaustive):**
BPHS (S216–S254) · Brihat Jataka (S255) · Uttara Kalamrita (S256) · Jataka Parijata (S257)
· Sarvartha Chintamani (S258) · Jaimini Sutras (S259) · Lal Kitab (S260)
· Chandra Kala Nadi (S261) · Phaladeepika (S262)

---

## Phase 1B — Sutra-Level Encoding (S263+)

Phase 1B is the research-grade corpus. It does not replace Phase 1A — it builds a
structured prediction layer on top of it. The claim Phase 1B must support:

> "9,200 structured predictions with source attribution, outcome taxonomy, and
> cross-text confidence calibration — traceable to original Sanskrit/Tamil verses,
> uncontestable on coverage, and analytically ready for feature engineering."

Phase 1B is gated behind four protocols that must be completed in S263 before any
encoding begins. These protocols are what prevent Phase 1A's failure mode from recurring.

---

### Protocol 1 — The Rule Contract (Phase 1B only)

Every Phase 1B rule must satisfy this contract. A rule missing any mandatory field
is rejected — not committed, not counted. No exceptions.

**Mandatory fields beyond current RuleRecord:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `primary_condition` | structured | `{planet, placement_type, placement_value}` | `{planet: Jupiter, placement_type: house, placement_value: 7}` |
| `modifiers` | list | Each: `{condition, effect: amplifies\|negates\|conditionalizes, strength}` | `{condition: "aspected_by_saturn", effect: negates, strength: strong}` |
| `exceptions` | list | Conditions that fully cancel the rule | `["if_lagna_lord_in_6_8_12"]` |
| `outcome_domains` | list | From fixed taxonomy only — no free-form | `["marriage", "wealth"]` |
| `outcome_direction` | enum | `favorable \| unfavorable \| neutral \| mixed` | `favorable` |
| `outcome_intensity` | enum | `strong \| moderate \| weak \| conditional` | `moderate` |
| `lagna_scope` | str or list | `"universal"` or explicit lagna list | `["scorpio", "cancer"]` |
| `dasha_scope` | str or list | `"universal"` or dasha lord list | `"universal"` |
| `verse_ref` | str | Chapter AND verse — not chapter only | `"Ch.14 v.23"` |
| `concordance_texts` | list | Populated at encoding time — not retroactive | `["BPHS", "Saravali"]` |
| `divergence_notes` | str | What other texts say differently | `"Saravali says moderate, BPHS says strong"` |
| `phase` | enum | `1B_matrix \| 1B_conditional \| 1B_compound` | `1B_matrix` |

**Rule types:**
- `1B_matrix`: systematic placement rules (9×12 grids, nakshatra series) — 120-150/session
- `1B_conditional`: lagna-conditional or dasha-conditional rules — 80-100/session
- `1B_compound`: multi-planet combinations, yoga triggers, exception overrides — 80-100/session

**Confidence formula (mechanical, not editorial):**
`confidence = 0.5 + (0.1 × len(concordance_texts)) − (0.05 × len(divergence_notes))`
A rule corroborated by 3 texts across different schools reaches confidence ≥ 0.8 automatically.

**Known limitation to document:** Verse citations are best-effort from training knowledge,
not from primary philological verification. They are navigation aids for human verification,
not independently verified citations. The corpus documentation must state this explicitly.

---

### Protocol 2 — The Outcome Taxonomy

Fixed before any Phase 1B encoding begins. Not extensible during encoding sessions.
Any outcome that doesn't map to this taxonomy means the taxonomy needs revision
— done in S263 schema session, never mid-encoding.

**15 Primary Domains:**
`longevity` · `physical_health` · `mental_health` · `wealth` · `career_status`
· `marriage` · `progeny` · `spirituality` · `intelligence_education`
· `character_temperament` · `physical_appearance` · `foreign_travel`
· `enemies_litigation` · `property_vehicles` · `fame_reputation`

**4 Outcome Directions:** `favorable` · `unfavorable` · `neutral` · `mixed`

**4 Intensities:** `strong` · `moderate` · `weak` · `conditional`

**5 Timing Qualifiers:** `early_life` (before 30) · `middle_life` (30–60)
· `late_life` (60+) · `dasha_dependent` · `unspecified`

---

### Protocol 3 — Coverage Maps

For every text in Phase 1B, a coverage map is committed before the first encoding
session for that text. The coverage map defines what "exhaustively encoded" means
for that specific text. A text is not marked complete until all sections in its
coverage map reach their minimum rule count.

**Coverage map structure:**
1. Chapter inventory — every chapter listed with topic
2. Section map per chapter — what prediction categories exist
3. Expected rule count per section — pre-encoding estimate
4. Completion tracking — actual vs. expected, flagged if below minimum

Sessions are scoped to "complete these sections of this coverage map" — not
"write N rules." The count follows from the coverage map, not vice versa.

---

### Protocol 4 — Real-Time Concordance Workflow

Concordance is not a retroactive exercise. Every Phase 1B rule follows this sequence:

1. Identify the prediction in the source text
2. **Before encoding:** query existing corpus for rules with same `primary_condition`
3. If match found — determine: same prediction (concordance) or different prediction
   about same configuration (divergence)?
4. Concordance → populate `concordance_texts`, update existing rule's `concordance_texts`
5. Divergence → populate `divergence_notes` with what the existing rule claims and why they differ
6. No match → encode normally, `concordance_texts` empty (this becomes the primary source)

This workflow produces concordance-calibrated confidence automatically. It also identifies
where schools genuinely disagree — analytically more valuable than where they agree.

---

### Phase 1B Priority Order

Priority is determined by analytical value, not by what's easiest to encode.

**Priority 1 — Laghu Parashari (S264–S266, ~306 rules)**
Reason: The 9×12 functional nature table (is Saturn a yogakaraka/benefic/malefic/maraka
for each of 12 lagnas?) is the master lookup that makes all other Parashari yoga rules
interpretable. Every subsequent text's yoga predictions are modified by functional nature.
Encode this before any other text's yoga rules.

**Priority 2 — Bhavartha Ratnakara (S267–S272, ~800 rules)**
Reason: Lagna-conditional rules are the highest-discrimination signal in the corpus.
"For Scorpio lagna, if Saturn occupies H5..." distinguishes Scorpio lagna charts from
all others — these rules create the analytical signal that generic rules can't provide.
The entire text is lagna-specific by design. `lagna_scope` will be fully populated.

**Priority 3 — Saravali: Conjunctions first (S273–S276 of full Saravali run)**
Reason: The 2-planet through multi-planet conjunction matrix is where Saravali differs
most from BPHS. Encode the divergent content before the concordant content.

**Priority 4 — Full Saravali systematic (S277–S281)**
Planet-in-house matrix, planet-in-sign matrix, dasha results — systematic Phase 1B_matrix.

**Priority 5 — Chamatkara Chintamani (S282–S285, ~550 rules)**
Priority 6 — Hora Ratnam (S286–S290, ~600 rules)
Priority 7 — Prasna Marga (S291–S297, ~950 rules) — horary system, `system: horary` flag
Priority 8 — Tajika Neelakanthi (S298–S300, ~255 rules) — annual charts, `system: varshaphala`
Priority 9 — Mansagari (S301–S302, ~300 rules)
Priority 10 — KP Comprehensive (S303–S304, ~300 rules)
Priority 11 — Bhrigu/Suka/Dhruva Nadi (S305–S307, ~240 rules)
Priority 12 — Jataka Tattva + Stri Jataka (S308–S309, ~270 rules)

**Note on Prasna Marga and Tajika:** These are separate astrological systems (horary
and annual charts respectively), not extensions of natal astrology. All rules from
these texts must carry a `system` field (`horary` / `varshaphala`) to prevent
contamination of natal chart analyses.

---

## Phase 1B Session Plan

| Sessions | Text | Type | Rules | Notes |
|----------|------|------|-------|-------|
| S263 | Schema definition | Planning | 0 | Rule contract + taxonomy + concordance workflow committed |
| S264–S266 | Laghu Parashari (8 chapters) | 1B_matrix + 1B_conditional | ~306 | Functional nature table 9×12 = 108 core rules |
| S267–S272 | Bhavartha Ratnakara (20 chapters) | 1B_conditional | ~800 | All lagna-conditional; lagna_scope fully populated |
| S273–S305 | Saravali (68 chapters) | 1B_matrix + 1B_compound | 2,898 | ✅ COMPLETE |
| S282–S285 | Chamatkara Chintamani (28 chapters) | 1B_matrix | ~550 | Short-verse formulation; ~108 placement rules |
| S286–S290 | Hora Ratnam (22 chapters) | 1B_matrix + 1B_conditional | ~600 | Includes Tajika bridge rules in final session |
| S291–S297 | Prasna Marga (32 chapters) | 1B_matrix + 1B_compound | ~950 | system=horary on all rules |
| S298–S300 | Tajika Neelakanthi (16 chapters) | 1B_matrix + 1B_conditional | ~255 | system=varshaphala; 50 Sahams in S299 |
| S339–S360 | Mansagari (30 chapters) | 1B_matrix + 1B_conditional | ~3,300 | sutra-level depth |
| S303–S304 | KP Comprehensive | 1B_conditional + 1B_compound | ~300 | Sublord chains; school=kp on all rules |
| S305–S307 | Bhrigu/Suka/Dhruva Nadi | 1B_compound | ~240 | Nadi pair-reading; school=nadi |
| S361–S390 | Jataka Tattva (22 tarangas) | 1B_matrix + 1B_compound | ~4,700 | sutra-level depth |
| S391–S400 | Stri Jataka (13 chapters) | 1B_conditional | ~1,500 | Female-specific rules |
| S310–S316 | Verification sessions (one per text after completion) | Audit | 0 | Coverage map check + contract compliance spot check |

**Phase 1B corpus total: ~25,000+ rules** (Phase 1A re-encode ~7,500 + new texts ~14,000 + existing 3,955)
**Phase 1B gate:** Every text has a committed coverage map, all sections complete,
≥90% of Phase 1B rules have all mandatory fields, verse_ref populated on all rules.

---

### Phase 1B Convergence Layer Priority

Not all Phase 1B work has equal analytical impact:

**Highest priority — directly strengthens Layer I concordance:**
- Laghu Parashari functional nature table (9×12) — unlocks correct yogakaraka weighting
  for every subsequent yoga rule; addresses root cause of OB-3 low axis-specific r
- Any rule where `concordance_texts` will reach 3+ entries — these are the high-confidence
  anchor rules that the SHAP model will identify as strongest features
- Rules with `lagna_scope` populated — these are the discrimination signals

**High priority — strengthens Layer II capacity/delivery:**
- Dasha-conditional rules (`dasha_scope` populated) — directly govern `promise_engine.py`
- Transit-conditional rules from Prasna Marga and Hora Ratnam

**Medium priority — deepens Layer I but single-school:**
- Additional Parashari placement rules where concordance will remain at 1 text
- Nabhasa and structural yogas — valid but lower concordance potential

**Research layer (horary/annual, Phase 6+ primary use):**
- Prasna Marga rules (`system: horary`) — not wired to natal engine; Phase 6 research
- Tajika Neelakanthi rules (`system: varshaphala`) — annual chart system, separate pipeline

---

## Open Source Library Ecosystem

### MIT License (Can Import Directly)

| Library | Key Features | Integration |
|---------|-------------|-------------|
| **VedAstro** | 1,000+ yogas, all planets/houses, Muhurtha, Life predictor | ✅ S191: Installed (v1.23.20), cross-validate script in tools/ |
| **VedAstro MCP Server** | MCP server — Claude directly to Vedic calculations in real-time | S191: Dev tool only, NOT production |
| **VedAstro DOB Dataset** | 15,800 records, Rodden AA, accurate timezone+DST | ✅ S191: data/vedastro/ created, download pending |
| **VedAstro Marriage Dataset** | 15,000 records, marriage type/divorce dates/outcome | S611: H7 validation |
| **jyotishganit** | D1–D60, Shadbala 6-fold, Vimshottari, Panchanga | Cross-validate D1–D60 |
| **pyswisseph** | Swiss Ephemeris Python binding, DE431 | Already integrated (S188: real files active) |

### AGPL-3.0 (Algorithm Study ONLY — NEVER import in production src/)

| Library | Key Features to Study |
|---------|----------------------|
| **PyJHora** | 22 graha dashas + 22 rasi dashas, D1–D144, full Shadbala verified vs BV Raman, 7,678 tests |
| **Maitreya 8/9** | Yogas from Parasara/Saravali/Brihat Jataka, Jaimini, Shadbala, Ashtakavarga |

**⚠️ G17:** Add ruff rule at S191 — no jhora imports in `src/`. Enforce in CI. First action of Phase 0.

---

## Classical Texts

### Available in Repository (Already Uploaded)

| Text | Translator | Est. Rules | Priority |
|------|-----------|-----------|---------|
| Sarwarthachintamani Vol 1 | B. Suryanarain Rao | ~200 | HIGH — yogas |
| Jaimini Astrology | P.S. Sastri | ~120 | HIGH — Jaimini system |
| Lal Kitab 1952 | Pt. Laxmi Kant Vashisth | ~150 | HIGH — separate schema |
| Chandra Kala Nadi Vol 2 | C.G. Rajan | ~100 | MED — Nadi schema |
| Vedic Astrology Integrated | PVR Narasimha Rao | Algorithm reference | HIGH |

### Download from archive.org at S191

| Text | Translator | Est. Rules | Chapters |
|------|-----------|-----------|---------|
| BPHS (97 chapters) | R. Santhanam + Girish Chand Sharma (both translations) | ~800 | 97 |
| Brihat Jataka | V. Subrahmanya Sastri | ~150 | 28 |
| Uttara Kalamrita | — | ~80 (timing-focused) | 7 |
| Jataka Parijata Vol I+II | V. Subrahmanya Sastri | ~200 | ~30 |

### Phase 1B New Texts (sutra-level estimates)

| Text | Chapters | Phase 1B Rules | Error vs. Phase 1A estimate |
|------|----------|---------------|------------------------------|
| Saravali (Kalyana Varma) | 68 | 2,898 (actual) | ✅ COMPLETE |
| Chamatkara Chintamani | 28 | ~550 | 6× more |
| Bhavartha Ratnakara | 20 | ~800 | 7× more (lagna-conditional multiplier) |
| Laghu Parashari | 8 | ~306 | 4× more |
| Hora Ratnam | 22 | ~600 | 5× more |
| Prasna Marga | 32 | ~950 | 5× more |
| Tajika Neelakanthi | 16 | ~255 | 2.5× more |
| Muhurtha Chintamani | 20 ullasas | ~2,700 | NEW — system=muhurtha |
| Mansagari | 30 | ~3,300 (revised) | sutra-level estimate |
| KP Comprehensive | — | ~300 | new |
| Bhrigu/Suka/Dhruva Nadi | — | ~240 | new |
| Jataka Tattva | 22 tarangas | ~4,700 (revised) | sutra-level estimate |
| Stri Jataka | 13 | ~1,500 (revised) | sutra-level estimate |

---

## Classical Rules DB Schema (`docs/classical_rules_db.json`)

```json
{
  "rule_id": "BPHS_CH36_V14",
  "source_text": "BPHS",
  "chapter": 36,
  "verse": "14",
  "planet": "Jupiter",
  "condition": "in_kendra",
  "house": 10,
  "effect_domain": "career",
  "effect_direction": 1,
  "effect_magnitude": 0.8,
  "classical_weight": 2.0,
  "school": "parashari",
  "authority": "pvrnr",
  "notes": "",
  "dispute": false,
  "concordance_score": 0.85
}
```

**Tradition-specific schemas (separate files required):**
- `jaimini_rules.json` — adds `chara_karaka`, `pada_lagna`, `house_system: 'whole_sign'` fields
- `lal_kitab_rules.json` — uses `house_position` (not sign-based), `remedy_primary` field  
- `nadi_rules.json` — uses `nadi_sequence`, `planetary_combination` fields

---

## Phase 1 Complete Picture

| Phase | Sessions | Rules | Status |
|-------|----------|-------|--------|
| Phase 1A — Representative | S216–S262 | 2,634 | ✅ Complete |
| Phase 1B — Sutra-Level | S263–S316+ | ~6,600 new | 🔲 Gated on S263 schema session |
| **Combined Phase 1 target** | — | **~9,200** | — |

**Phase 1 gate (updated):** Not rule count alone. The gate is:
1. Every Phase 1B text has a committed coverage map with all sections complete
2. ≥90% of Phase 1B rules satisfy the full Rule Contract (all 12 mandatory fields)
3. `verse_ref` populated on all Phase 1B rules (chapter + verse, not chapter only)
4. `concordance_texts` populated in real-time for all Phase 1B rules
5. Outcome taxonomy used consistently — no free-form `outcome_domains` values
6. Prasna Marga and Tajika rules have `system` field set (`horary` / `varshaphala`)

**Failure mode prevention:** Phase 1A failed because the definition of done was a
rule count target. Phase 1B sessions are scoped to coverage map sections, not counts.
A session is not done until its targeted sections are complete to minimum count.
The count follows from the map, not from a pre-set target.

---

## Yoga Coverage

| Category | Current | Target | Source |
|----------|---------|--------|--------|
| Pancha Mahapurusha (5) | ✅ | 5 | BPHS Ch.36 |
| Raj Yogas | ~3 | 50+ | BPHS Ch.36 |
| Dhana Yogas | ✅ basic | 30+ | Sarwarthachintamani |
| Lunar Yogas | ✅ 5 | 5 | BPHS |
| Solar Yogas | ✅ 4 | 4 | BPHS |
| Special Yogas | ✅ 3 | 3 | BPHS |
| Arishta Yogas | 0 | 30+ | BPHS |
| Nabhasa Yogas | ~10 | 36 | Brihat Jataka Ch.12 |
| **Total** | **~35** | **310+** | — |

---

## Dasha System Coverage

| System | Status | Authority | When Applicable |
|--------|--------|-----------|----------------|
| Vimshottari (120yr) | ✅ Complete | BPHS Ch.46 | All charts (default) |
| Narayana (81yr) | ✅ Complete | PVRNR / BPHS | Sign-based, all charts |
| Ashtottari (108yr) | 📋 S361 | BPHS Ch.46 | When Rahu NOT in Kendra/Trikona |
| Yogini (36yr) | 📋 S361 | Various | Supplementary |
| Kalachakra | 📋 S361 | BPHS | Moon in specific nakshatras |
| Narayana (Jaimini) | 📋 S361 | Sanjay Rath | Jaimini school |
| Shoola | 📋 S361 | BPHS | Death-adjacent events |
| 22 Graha Dashas (PyJHora) | 📋 Phase 1 | Various | Various conditions |
| 22 Rasi Dashas (PyJHora) | 📋 Phase 1 | Various | Various conditions |

---

## Authoritative Classical Reference Library

### Primary Classical Texts
- **BPHS** — Brihat Parasara Hora Sastra (PVRNR, Sagar Publications)
- **Brihat Jataka** — Varahamihira (B.S. Rao, Ranjan Publications) — Nabhasa Yogas
- **Phaladeepika** — Mantreswara (G.S. Kapoor, Ranjan Publications) — Avasthas, Muhurtha
- **Uttarakalamrita** — Kalidasa (P.S. Sastri) — timing, Neecha Bhanga Raja Yoga (NBRY)
- **Saravali** — Kalyanarma (R. Santhanam) — Graha Yuddha (Ch.4 v.18-22), aspects
- **Sarvartha Chintamani** — Venkatesha (B. Suryanarain Rao) — yogas
- **Jataka Parijata** — Vaidyanatha Dikshita — Avasthas, special rules
- **Jaimini Sutras** — Sanjay Rath commentary

### Software Validation Reference
- **Jagannatha Hora 8.0** (PVRNR) — free; gold standard cross-validation
- **Swiss Ephemeris Manual** — ayanamshas and planet flags


---

## Phase 1A Re-Encode Plan (CRITICAL — before new text encoding)

The 7 primary Parashari texts have Phase 1A encodings (prose descriptions, no structured
fields). These MUST be re-encoded at Phase 1B depth because:
1. BPHS is the concordance anchor — without structured BPHS rules, concordance is incomplete
2. These texts' rules can't fire in rule_firing.py (empty primary_condition)
3. They represent ~7,500-9,500 rules at sutra-level that are invisible to the ML pipeline

| Text | Current 1A Rules | Est. 1B Rules | Priority |
|------|-----------------|---------------|----------|
| BPHS (97 chapters) | 1,239 | ~4,000-5,000 | HIGHEST — concordance anchor |
| Brihat Jataka (28 ch) | 190 | ~800-1,000 | HIGH — second most cited |
| Phaladeepika (27 ch) | 189 | ~500-700 | HIGH — third most cited |
| Uttara Kalamrita (7 ch) | 201 | ~600-800 | MEDIUM |
| Jataka Parijata (30 ch) | 197 | ~600-800 | MEDIUM |
| Sarvartha Chintamani | 170 | ~500-600 | MEDIUM |
| Jaimini Sutras | 178 | ~400-500 | MEDIUM (school=jaimini) |

**Re-encode happens BEFORE new text encoding (Chamatkara Chintamani etc.)**

### Texts Requiring Schema Extension (school_specific field)

| Text | School | Extra Fields Needed |
|------|--------|-------------------|
| Jaimini Sutras | jaimini | chara_karaka, pada_lagna, house_system=whole_sign |
| KP Comprehensive | kp | sublord, significator, cusp |
| Lal Kitab | lal_kitab | house_position (not sign-based), remedy |
| Nadi texts | nadi | nadi_sequence, planetary_combination |
| Muhurtha Chintamani | muhurtha | panchanga_element, activity, election_quality, system=muhurtha |

These fields go in the `school_specific` dict on RuleRecord (added S305).
