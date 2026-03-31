I now have a comprehensive understanding of the entire codebase. Let me produce the exhaustive data governance framework.

---

# LagnaMaster Data Governance Framework

## Document Purpose and Scope

This document is the authoritative data governance specification for the LagnaMaster classical astrology corpus across all 10 phases (S191-S1050+). It covers 25,000+ structured rules from 15+ texts, 4 schools, 4 systems, and governs every operation from encoding a single sloka through to publishing peer-reviewed research. Every control specifies what it prevents, when it matters, and whether to build it now or later.

The framework is organized into 12 governance domains. Within each domain, controls are designated:

- **NOW** = build during Phase 1 encoding (current)
- **FOUNDATION** = lay metadata/schema now, build enforcement later
- **LATER** = build when the phase arrives; no current action needed

---

## 1. DATA QUALITY CONTROLS (Individual Rule Correctness)

### 1.1 Structural Quality (What the schema can enforce mechanically)

**1.1.1 Field Completeness Gate**
- **What it prevents:** Rules shipping with empty mandatory fields that silently default to useless values (the Phase 1A failure mode).
- **When it matters:** Phase 1 onward (every encoding session).
- **Status: BUILT (NOW).** V2ChapterBuilder refuses to build if depth thresholds fail. `corpus_audit.py` has 8 hard errors. `rule_record.py` enforces confidence range in `__post_init__`. The V2 enforcement boundary is `V2_ENFORCEMENT_START = "S310"`.
- **Current enforcement inventory (17 checks):**
  - Build-time gates (6): rules/slokas ratio >= 0.5, commentary coverage >= 40%, concordance coverage >= 25%, sloka coverage (verse_refs span the declared range), commentary uniqueness (no copy-paste), and the V2ChapterBuilder.build() refusal mechanism.
  - Audit hard errors (8): predictions non-empty, entity_target from controlled vocabulary, signal_group non-empty, timing_window non-empty-dict, timing_window.type valid, predictions structure (entity/claim/domain/direction keys), rule_relationship structure, predictions entity vs entity_target consistency.
  - Audit warnings (3): BPHS commentary check, concordance cross-verification, shallow prediction claim detection.
- **Gap identified:** No gate prevents a rule whose `primary_condition.conditions` list contains primitives with typos in `type` (e.g., `"planet_in_hous"` instead of `"planet_in_house"`). The 8 primitives are documented but not enforced by code.
- **Recommendation (NOW):** Add to `V2ChapterBuilder.add()` a validation step that checks every `conditions[i].type` against the 8-primitive whitelist in Protocol E. Reject at build time, not at audit time.

**1.1.2 Controlled Vocabulary Enforcement**
- **What it prevents:** Free-form values in enumerated fields that break downstream aggregation and ML feature extraction.
- **When it matters:** Phase 1 onward.
- **Status: PARTIALLY BUILT.** `corpus_audit.py` validates `entity_target`, `timing_window.type`, `rule_relationship.type`. The `PHASE1B_OUTCOME_TAXONOMY.md` defines 15 domains. `planet_normalization.py` canonicalizes planet names.
- **Gaps identified:**
  - `outcome_domains` values are not validated against the 15-domain taxonomy at build time. A rule with `outcome_domains=["spouse_quality"]` would pass the builder and fail only if someone runs the audit.
  - `outcome_direction` and `outcome_intensity` are not validated at build or audit time.
  - `school` is not validated against the allowed set (parashari, kp, jaimini, nadi, lal_kitab, tajika, all).
  - `system` is not validated against (natal, horary, varshaphala, muhurtha, transit).
  - `phase` is not validated against (1A_representative, 1A_deprecated, 1B_matrix, 1B_conditional, 1B_compound).
  - `evaluation_method` is not validated.
- **Recommendation (NOW):** Add a `_validate_vocabularies()` method to `V2ChapterBuilder.add()` or to `RuleRecord.__post_init__()` that checks all enumerated fields. This is a one-time addition that prevents an entire class of silent corruption.

**1.1.3 Planet Name Canonicalization Gate**
- **What it prevents:** Duplicate rules appearing distinct because one uses `"Jupiter"` and another uses `"jupiter"`, or conjunction pairs ordered differently (`mars_jupiter` vs `jupiter_mars`).
- **When it matters:** Phase 1 onward, critical for concordance matching.
- **Status: PARTIALLY BUILT.** `planet_normalization.py` exists with `normalize_planet_name()` and `is_valid_planet_name()`.
- **Gap:** Not called automatically during rule creation. The V2ChapterBuilder does not normalize planet names in conditions.
- **Recommendation (NOW):** Call `normalize_planet_name()` on every `primary_condition.conditions[i].planet` value inside `V2ChapterBuilder._build_primary_condition()`.

**1.1.4 Confidence Score Mechanical Derivation**
- **What it prevents:** Editorial confidence scores that encode the encoder's opinion rather than structural evidence.
- **When it matters:** Phase 1 onward; critical for Phase 6 ML (confidence as feature weight).
- **Status: BUILT.** Formula is `base=0.6 + 0.08*concordance + 0.05*verse_bonus - 0.05*divergence`, capped [0.1, 1.0]. Computed mechanically in V2ChapterBuilder and overridden by `concordance_map.py` at build time.
- **Governance rule:** No encoder may manually set confidence on a Phase 1B rule. The field is always derived. Any rule with `last_modified_session >= S263` and a confidence that does not match the formula is a hard audit error.
- **Recommendation (NOW):** Add a check to `corpus_audit.py` that recomputes confidence from concordance/divergence/verse data and flags any rule where the stored value differs by more than 0.01.

### 1.2 Semantic Quality (What only human review can catch)

**1.2.1 Claim Specificity Gate**
- **What it prevents:** Rules with generic, unfalsifiable claims like "good" or "beneficial" that pass structural checks but carry zero predictive value.
- **When it matters:** Phase 1 onward; critical for Phase 3 (falsifiability) and Phase 6 (SHAP).
- **Status: BUILT.** Slip-through check 6 in `corpus_audit.py` rejects claims shorter than 10 chars and generic single-word claims.
- **Gap:** The 10-char threshold is low. "wealthy_spouse" passes (15 chars) but is marginally specific. At 25,000 rules, the long tail of barely-passing claims will be significant.
- **Recommendation (FOUNDATION):** Add a `claim_specificity_score` computed at build time (word count, presence of entity, presence of temporal qualifier, presence of domain-specific noun). Do not block on it now, but log it. Phase 3 can use this as a filter for Bayesian eligibility.

**1.2.2 Entity-Description Consistency Check**
- **What it prevents:** Rules where `entity_target=native` but the description clearly discusses the father/spouse/children. This is the most common encoding error.
- **When it matters:** Phase 1 onward; catastrophic for Phase 8 (multigenerational).
- **Status: PARTIALLY BUILT.** Slip-through check 1 compares prediction entities vs entity_target. `ENTITY_CHECK_CATEGORIES` in `corpus_audit.py` flags house categories that commonly predict about non-native entities.
- **Gap:** The check only fires if `predictions[i].entity` differs from `entity_target`. If the encoder wrongly puts `"native"` in both the prediction AND entity_target for a rule that is clearly about the father, no check catches it.
- **Recommendation (NOW):** Extend the audit to run keyword detection (from `v2_scorecard.py`'s `_ENTITY_KEYWORDS`) on every rule's description AND commentary, and flag any rule where the detected entity does not match `entity_target`. This should be a warning (not hard error) because keyword detection has false positives.

**1.2.3 Direction-Description Consistency Check**
- **What it prevents:** Rules where `outcome_direction=favorable` but the description contains clearly negative language ("destroys", "loss of", "death"), or vice versa.
- **When it matters:** Phase 1 onward.
- **Status: PARTIALLY BUILT.** `direction_fixes.py` contains 50 rule IDs that were retroactively corrected to "mixed". But this is a manual list, not a systematic check.
- **Recommendation (NOW):** Build a simple sentiment classifier (negative keyword list: "destroy", "loss", "death", "poverty", "disease", "enemy", "misery"; positive keyword list: "wealth", "happiness", "long life", "fame", "prosperity") and run it at audit time. Flag any rule where the description sentiment strongly conflicts with `outcome_direction`. This is a warning, not a hard error.

**1.2.4 Timing-Description Consistency Check**
- **What it prevents:** Rules where the description mentions specific ages or dasha periods but `timing_window` is set to `{"type": "unspecified"}`.
- **When it matters:** Phase 1 onward; critical for Phase 5 (temporal model).
- **Status: BUILT.** Slip-through check 2 in `corpus_audit.py` regex-scans descriptions for age patterns and flags timing_window=unspecified when ages are mentioned.
- **Gap:** Does not detect dasha references in descriptions ("during Saturn dasha", "in Jupiter period"). These are timing assertions that should map to `timing_window.type = "dasha_period"`.
- **Recommendation (NOW):** Extend the regex in slip-through check 2 to include dasha language patterns: `r'(?:during|in)\s+(\w+)\s+(?:dasha|mahadasha|period|antardasha)'`.

**1.2.5 Commentary Completeness Verification**
- **What it prevents:** Rules where the encoder read only the verse but skipped Santhanam's notes, which often contain critical timing, exception, and edge-case information.
- **When it matters:** Phase 1 (current).
- **Status: BUILT.** V2ChapterBuilder.build() requires MIN_COMMENTARY=40%. The audit warns on BPHS rules with no commentary.
- **Gap:** 40% is the floor. Many chapters have commentary on every sloka. The threshold should be per-text (BPHS Santhanam has extensive notes; Brihat Jataka does not).
- **Recommendation (FOUNDATION):** Add a `text_commentary_richness` metadata field to each source text's builder configuration. BPHS=high (min 60%), BrihatJataka=low (min 20%), Saravali=medium (min 40%). This prevents applying BPHS standards to terse texts.

**1.2.6 Verse Reference Accuracy**
- **What it prevents:** Verse citations that are plausible but wrong (e.g., "Ch.14 v.23" when the content is actually from v.25), making the corpus unverifiable.
- **When it matters:** Phase 1 onward; critical for Phase 10 (peer review).
- **Status: PARTIALLY BUILT.** V2ChapterBuilder.build() checks that verse_refs span the declared sloka range. But no check verifies that a specific verse_ref matches its content.
- **Governance rule:** Verse citations are navigation aids for human verification, not independently verified citations. This is explicitly stated in `PHASE1B_RULE_CONTRACT.md`. The corpus documentation must always include this caveat.
- **Recommendation (LATER, Phase 10):** Before publication, hire a Sanskrit/Jyotish scholar to spot-check 5% of rules against physical editions. Record verification results in a new `verse_verified: bool` field.

### 1.3 Interpretive Accuracy (Fidelity to Source Text)

**1.3.1 Translation Fidelity Tracking**
- **What it prevents:** Encoding errors introduced by the translation layer. Santhanam's English can be archaic or ambiguous. A modern encoder may misinterpret 19th-century idiom.
- **When it matters:** Phase 1 onward.
- **Status: NOT BUILT.**
- **Recommendation (FOUNDATION):** Add `translator` field to RuleRecord (default: `"santhanam"` for BPHS). When multiple translations of the same text exist (BPHS has Santhanam and GC Sharma), encoding from different translators should be tracked. This enables Phase 10 inter-translator reliability analysis.

**1.3.2 Sanskrit Verse Preservation**
- **What it prevents:** Loss of the original Sanskrit when translations disagree. The Sanskrit is the ground truth.
- **When it matters:** Phase 1 onward; critical for Phase 10.
- **Status: PARTIALLY BUILT.** The `verse` field exists on RuleRecord but is rarely populated (most Phase 1B rules leave it empty).
- **Recommendation (FOUNDATION):** Do not require Sanskrit for Phase 1 encoding (it would slow encoding 10x). But add a `sanskrit_verified: bool = False` field to RuleRecord. Phase 10 populates it.

**1.3.3 Encoder Interpretive Latitude Boundaries**
- **What it prevents:** Encoders making judgment calls about what a verse "really means" instead of faithfully recording what it says.
- **When it matters:** Phase 1 onward.
- **Governance rule:** The encoder records the text's claim, not their assessment of it. If BPHS says "native will die at age 32", the rule encodes `timing_window={"type": "age", "value": 32}` even if the encoder believes this is metaphorical. Interpretive latitude goes into `commentary_context`, not `predictions`.
- **Recommendation (NOW):** Add this as Protocol G in `ENCODING_PROTOCOL_V2.md`: "The encoder records the text's explicit claim. Interpretive hedging, modernization, or softening goes in `commentary_context`, never in `predictions` or `outcome_direction`."

---

## 2. DATA INTEGRITY CONTROLS (Corpus-Wide Consistency)

### 2.1 Duplicate Detection and Prevention

**2.1.1 Rule ID Uniqueness**
- **What it prevents:** Two rules with the same ID colliding in the registry.
- **Status: BUILT.** `CorpusRegistry.add()` raises `ValueError` on duplicate `rule_id`.
- **Gap:** IDs are namespace-scoped by convention (BPHS, SAV, BVR, LPF, etc.) but not by enforcement. If two builders independently generate ID `BPHS1200`, the collision is caught at build time but the error message does not identify the conflicting file.
- **Recommendation (NOW):** Enhance the ValueError message to include the source file of the existing rule.

**2.1.2 Semantic Duplicate Detection**
- **What it prevents:** Two rules with different IDs encoding the same prediction from the same text. This happens when encoding sessions overlap or when the same verse is encoded under different chapter categorizations.
- **When it matters:** Phase 1 onward. At 25,000 rules, hundreds of semantic duplicates are inevitable.
- **Status: NOT BUILT.**
- **Recommendation (FOUNDATION):** Build a `DuplicateDetector` that compares rules by (`source`, `primary_condition.planet`, `primary_condition.conditions[0].type`, `primary_condition.conditions[0].house` or `sign`). Rules from the SAME source with the SAME condition structure should be flagged as potential duplicates. Cross-source matches are concordance, not duplicates.

**2.1.3 Cross-Session ID Collision Prevention**
- **What it prevents:** Two encoding sessions (S311 and S312) both starting their builder at `id_start=1200`.
- **When it matters:** Phase 1, during parallel encoding of multiple chapters.
- **Status: PARTIALLY BUILT.** ID ranges are convention-based (Ch.12 starts at 1200, Ch.13 at 1300). But this is in builder instantiation code, not in a central registry.
- **Recommendation (NOW):** Create `src/corpus/id_registry.py` with a simple dict mapping chapter to id_start. The V2ChapterBuilder constructor validates against this registry. This prevents the most common collision scenario.

### 2.2 Cross-Text Concordance Integrity

**2.2.1 Bidirectional Concordance Consistency**
- **What it prevents:** Rule A claims concordance with Rule B's source, but Rule B does not claim concordance with Rule A's source. This breaks confidence symmetry.
- **When it matters:** Phase 1 onward; critical for confidence calibration.
- **Status: PARTIALLY BUILT.** `PHASE1B_CONCORDANCE_WORKFLOW.md` requires bidirectional updates, but this is a manual protocol, not an automated check.
- **Recommendation (NOW):** Add an audit check that scans all rules: for every rule R1 with `concordance_texts=["BPHS"]`, find all BPHS rules with matching `primary_condition`. If no BPHS rule lists R1's source in its `concordance_texts`, flag as "orphaned concordance — bidirectional update missing."

**2.2.2 Concordance Overclaim Detection**
- **What it prevents:** Encoding sessions claiming concordance based on memory rather than verified corpus matching. Example: encoder "knows" that Saravali agrees with this BPHS rule, but the Saravali rule was never actually encoded.
- **When it matters:** Phase 1 onward.
- **Status: PARTIALLY BUILT.** Audit warning in `audit_v2_warnings()` checks that claimed concordance texts actually have matching rules in the corpus.
- **Gap:** The check uses planet matching but does not verify condition-type matching (a rule claiming concordance with a BPHS house-placement rule should find a BPHS rule with the same house, not just the same planet).
- **Recommendation (NOW):** Tighten the concordance verification to require matching on both planet AND placement type (house/sign/nakshatra).

**2.2.3 Concordance Map Staleness Prevention**
- **What it prevents:** `concordance_map.py` (auto-generated by `tools/backfill_phase1b.py`) becoming stale as new rules are encoded, causing confidence scores to lag.
- **When it matters:** Phase 1 onward.
- **Status: PARTIALLY BUILT.** The map is regenerated manually.
- **Recommendation (FOUNDATION):** Add concordance map regeneration to the pre-push hook or the session end script. This ensures confidence scores are always current.

### 2.3 Namespace and Taxonomy Consistency

**2.3.1 Source Text Name Canonicalization**
- **What it prevents:** The same text being referenced differently across rules: "BPHS" vs "Brihat Parasara Hora Shastra" vs "BrihatParasaraHoraShastra". This breaks concordance aggregation by source.
- **When it matters:** Phase 1 onward.
- **Status: NOT ENFORCED.** Convention uses short names but there is no canonical lookup.
- **Recommendation (NOW):** Create `src/corpus/source_texts.py` with:
  ```
  CANONICAL_SOURCES = {
      "BPHS": {"full_name": "Brihat Parasara Hora Shastra", "translator": "Santhanam", "school": "parashari"},
      "Saravali": {...}, "Phaladeepika": {...}, ...
  }
  ```
  Validate `source` and `concordance_texts` entries against this canonical list at build time.

**2.3.2 Outcome Domain Drift Prevention**
- **What it prevents:** New encoding sessions introducing domain values that are slight variations of existing ones ("marital_happiness" vs "marriage").
- **When it matters:** Phase 1 onward.
- **Status: NOT ENFORCED AT BUILD TIME.** The taxonomy is in `PHASE1B_OUTCOME_TAXONOMY.md` but not code-enforced.
- **Recommendation (NOW):** Create `src/corpus/taxonomy.py` with `VALID_OUTCOME_DOMAINS = frozenset({...})` and validate in V2ChapterBuilder.add().

### 2.4 Version Control Integrity

**2.4.1 Session Stamping**
- **What it prevents:** Inability to determine when a rule was created or last modified, making error forensics impossible.
- **When it matters:** Phase 1 onward.
- **Status: BUILT.** `last_modified_session` field on RuleRecord. V2ChapterBuilder stamps it automatically.

**2.4.2 Schema Version Tracking**
- **What it prevents:** Rules created under different schema versions being treated identically. Phase 1A rules should not be held to Phase 1B standards; pre-S309 rules should not be held to S309+ standards.
- **When it matters:** Phase 1 onward (already relevant — V2_ENFORCEMENT_START = "S310").
- **Status: PARTIALLY BUILT.** The `phase` field distinguishes 1A from 1B. The `V2_ENFORCEMENT_START` constant in `corpus_audit.py` distinguishes pre/post S310 rules.
- **Recommendation (FOUNDATION):** Add a `schema_version: int = 1` field to RuleRecord. Phase 1A = v1, Phase 1B = v2, S309 = v3. This is more robust than string comparison on session numbers.

---

## 3. DATA LINEAGE AND PROVENANCE

### 3.1 Source Text Chain

**3.1.1 Minimum Provenance Fields (Already on RuleRecord)**
- `source`: canonical text name
- `chapter`: chapter/section reference
- `verse_ref`: chapter + verse citation
- `school`: originating school
- `last_modified_session`: when encoded

**3.1.2 Missing Provenance Fields (FOUNDATION)**

| Field | Purpose | Build When | Foundation Now |
|-------|---------|------------|----------------|
| `translator` | Which English edition | Phase 10 | Add field with default="santhanam" |
| `edition_year` | Publication year of edition used | Phase 10 | Add field with default="" |
| `encoding_conversation_id` | Claude session that produced the rule | Phase 1 | Add field, populated by start_session.py |
| `encoding_model` | Which AI model encoded the rule | Phase 10 | Add field with default="claude-sonnet-4" |
| `human_verified` | Whether a human Jyotish scholar has reviewed | Phase 10 | Add field with default=False |
| `verification_date` | When human verification occurred | Phase 10 | Not needed now |

- **Recommendation (NOW):** Add `translator: str = ""` and `encoding_session_context: str = ""` to RuleRecord. These are the two cheapest-to-add, hardest-to-retrofit provenance fields. The encoding_session_context should store the session number and a brief description of the conversation context (e.g., "S311 BPHS Ch.12 systematic encode from Santhanam Vol 1 pp.126-132").

### 3.2 Prediction-to-Source Tracing

**3.2.1 Rule Firing Audit Trail**
- **What it prevents:** A user asking "why did you say X about my career?" with no way to trace the answer back to a specific BPHS verse.
- **When it matters:** Phase 7 (product). Must be designed by Phase 2 (engine rebuild).
- **Status: NOT BUILT.** The scoring engine produces house scores but does not record which rules contributed.
- **Recommendation (FOUNDATION):** Design the Phase 2 engine to return a `RuleFiringRecord` for every rule that contributed to a prediction, containing: `rule_id`, `source`, `verse_ref`, `weight_contribution`, `confidence`. This is the "show your work" feature.

**3.2.2 Concordance State at Prediction Time**
- **What it prevents:** Inability to distinguish a prediction backed by 3-school concordance from one backed by a single text. This distinction is critical for research validity.
- **When it matters:** Phase 3 (feedback architecture) onward.
- **Status: DESIGNED but not built.** `RESEARCH.md` specifies `layer1_concordance_score`, `convergence_tier` columns in the predictions table.
- **Recommendation (FOUNDATION):** Add these column definitions to the Phase 3 schema design document now. They cannot be retrofitted after predictions are issued.

---

## 4. DATA GOVERNANCE FOR ML PIPELINE

### 4.1 Feature Stability

**4.1.1 Feature Definition Freezing Protocol**
- **What it prevents:** Corpus changes after feature extraction that invalidate the feature definitions used in a pre-registered study.
- **When it matters:** Phase 6 (ML pipeline).
- **Recommendation (FOUNDATION):** Define a `CorpusSnapshot` mechanism: before any SHAP analysis, the corpus is serialized to a versioned JSON file with a SHA-256 hash. The OSF pre-registration includes this hash. Any corpus change after the snapshot requires a new snapshot and an OSF amendment.
- **Implementation:** `src/corpus/snapshot.py` with `create_snapshot() -> (filepath, sha256)` and `verify_snapshot(filepath, sha256) -> bool`. Build in Phase 2, but define the API now.

**4.1.2 Feature Independence Tracking**
- **What it prevents:** Two rules that are NOT independent being treated as independent features in ML. Example: a rule and its contrary mirror are the same signal, not two signals.
- **When it matters:** Phase 6.
- **Status: PARTIALLY BUILT.** `signal_group` groups rules from the same chart signal. `rule_relationship` tracks alternatives/mirrors.
- **Recommendation (FOUNDATION):** When building feature vectors (Phase 2), rules in the same `signal_group` must be reduced to a single feature (the most specific sub-rule that fires). Document this in the feature engineering spec.

**4.1.3 Cross-Validation Contamination Prevention**
- **What it prevents:** Training data leaking into test sets through rules that encode knowledge of specific charts.
- **When it matters:** Phase 6.
- **Status: PARTIALLY BUILT.** `cv_splitter.py` in `src/research/` implements time-split CV (pre-2010 train, 2010+ test).
- **Recommendation (FOUNDATION):** Add a `chart_derived: bool = False` field to RuleRecord. Rules that were formulated based on observation of specific charts (as opposed to classical text principles) must be flagged. These rules must be excluded from training when their source charts appear in the test set.

**4.1.4 Pre-Registration Compatibility**
- **What it prevents:** Running SHAP analysis on features that were not pre-registered, then presenting results as confirmatory.
- **When it matters:** Phase 6.
- **Status: DESIGNED.** `osf_registration.py` in `src/research/` exists. G22 mandates pre-registration.
- **Recommendation (FOUNDATION):** Each RuleRecord should carry a `pre_registered_feature_set: str = ""` field. When an OSF filing is made, the rules included in that filing's feature set are tagged. Only tagged rules can be used in confirmatory analysis.

### 4.2 Model-Corpus Coupling

**4.2.1 Corpus Version Pinning for Models**
- **What it prevents:** A trained model being evaluated against a corpus that has changed since training, producing inconsistent results.
- **When it matters:** Phase 6.
- **Recommendation (LATER, Phase 6):** Every trained model artifact must record the corpus snapshot hash it was trained on. Model evaluation must verify corpus hash match.

**4.2.2 Rule Deprecation Impact on Models**
- **What it prevents:** Deprecating or correcting a rule after a model was trained on it, silently changing the model's feature space.
- **When it matters:** Phase 6 onward.
- **Recommendation (FOUNDATION):** Deprecated rules (`phase="1A_deprecated"`) must never be deleted from the corpus. They are soft-deleted (marked deprecated, excluded from active feature extraction) but retained for model provenance.

---

## 5. DATA GOVERNANCE FOR USER-FACING PRODUCT

### 5.1 Guardrail Compliance (G01-G25)

**5.1.1 Health Content Suppression (G02)**
- **What it prevents:** Rules about illness, death, surgery timing, longevity assessments reaching user-facing output.
- **When it matters:** Phase 7 (product).
- **Status: NOT BUILT. G02 is RED.**
- **Recommendation (FOUNDATION):** Add `health_sensitive: bool` to RuleRecord, derived automatically: `True` if `outcome_domains` includes `longevity`, `physical_health`, or `mental_health`. The Phase 7 API layer filters out all `health_sensitive=True` rules from user-facing output. The field must be populated now, during encoding, because retroactively scanning 25,000 rules is expensive and error-prone.
- **Implementation (NOW):** Add to `_apply_derived_fields()` in `combined_corpus.py`:
  ```python
  HEALTH_DOMAINS = {"longevity", "physical_health", "mental_health"}
  rule.health_sensitive = bool(set(rule.outcome_domains) & HEALTH_DOMAINS)
  ```

**5.1.2 Language Framing (G01, G19)**
- **What it prevents:** User-facing text using "prediction" or presenting output as deterministic.
- **When it matters:** Phase 7.
- **Recommendation (FOUNDATION):** Add `user_facing_framing: str = ""` to RuleRecord. For rules that will generate user-facing text, this field provides the agency-framed version of the prediction. Do not populate now — populate during Phase 4/7 language review sessions.

**5.1.3 Consent Boundary Enforcement (G03)**
- **What it prevents:** Processing user data without explicit consent for each processing purpose.
- **When it matters:** Phase 7.
- **Status: PARTIALLY BUILT.** `src/privacy/consent_engine.py` exists with consent ledger infrastructure.
- **Recommendation (LATER, Phase 3):** The consent engine must be extended to cover corpus-derived predictions. Each prediction category (career, marriage, health-internal-only) requires its own consent flag.

### 5.2 Content Safety Classification

**5.2.1 Rule Safety Tier**
- **What it prevents:** Sensitive content (death timing, disease, mental health, litigation) reaching users without appropriate framing.
- **When it matters:** Phase 7.
- **Recommendation (FOUNDATION):** Add `safety_tier: str = "standard"` to RuleRecord with values:
  - `"standard"` — career, wealth, general personality
  - `"sensitive"` — marriage predictions, family relationships
  - `"restricted"` — death, disease, mental health, longevity
  - `"research_only"` — content that should never reach any user (e.g., Cox survival analysis results)
- Derive automatically from `outcome_domains` at build time. Override manually when needed.

---

## 6. DATA GOVERNANCE FOR FEEDBACK LOOP

### 6.1 Falsifiability Requirements

**6.1.1 Rule Falsifiability Gate**
- **What it prevents:** Rules entering the Bayesian update pipeline that cannot be confirmed or disconfirmed, polluting training data.
- **When it matters:** Phase 3 (feedback architecture).
- **Status: NOT BUILT.**
- **Recommendation (FOUNDATION):** Add `falsifiable: bool` to RuleRecord, derived at build time. A rule is falsifiable if:
  1. `prediction_type` is "event" (not "trait" — traits are harder to falsify)
  2. At least one prediction has a specific `claim` (not generic)
  3. `timing_window.type` is not "unspecified" (untimed predictions can never be closed)
  Only `falsifiable=True` rules are eligible for Bayesian updates.
- **Recommendation (NOW):** Add the field. Do not enforce yet. Phase 3 uses it as a filter.

**6.1.2 Temporal Window Management**
- **What it prevents:** Predictions that remain open forever, never closing for validation.
- **When it matters:** Phase 3.
- **Recommendation (FOUNDATION):** The `timing_window` field already captures timing type. Phase 3 must define a `prediction_expiry` policy:
  - `age` timing: prediction expires when the native passes the stated age + 2 years
  - `dasha_period` timing: prediction expires when the dasha period ends
  - `unspecified` timing: prediction is NOT eligible for feedback collection
  Document this policy now. Build it in Phase 3.

### 6.2 Bayesian Update Eligibility

**6.2.1 Credibility-Weighted Updates (G14)**
- **What it prevents:** Users who confirm everything (or deny everything) having outsized influence on model weights.
- **When it matters:** Phase 3.
- **Status: DESIGNED.** G14 specifies credibility scoring. `src/feedback/feedback_loop.py` has initial structure.
- **Recommendation (LATER, Phase 3):** Build credibility scoring before the first Bayesian update.

**6.2.2 Hindsight Bias Prevention (G04)**
- **What it prevents:** Users adjusting their prior probability after seeing the prediction, corrupting the signal isolation metric.
- **When it matters:** Phase 3.
- **Status: DESIGNED.** G04 mandates `user_prior_prob_pre` captured before prediction shown. API layer must enforce with HTTP 400 if `reveal_prediction` called without `prior_captured_at`.
- **Recommendation (FOUNDATION):** This is a schema and API enforcement issue, not a corpus governance issue. But the corpus must support it: every rule used in a prediction must carry enough metadata to generate a meaningful prior question. Add this to the Phase 3 specification.

---

## 7. DATA GOVERNANCE FOR MULTI-SYSTEM SUPPORT

### 7.1 School Isolation

**7.1.1 School Tag Enforcement**
- **What it prevents:** Parashari rules contaminating KP analysis or Jaimini rules firing in Parashari-only mode.
- **When it matters:** Phase 1 onward; critical for Phase 2 (engine rebuild) and Phase 6 (SHAP).
- **Status: PARTIALLY BUILT.** `school` field on every rule. `school_rules.py` has `SCHOOL_RULE_MAP`, `is_rule_active()`, `filter_rules_by_school()`. `calc_config.py` declares the active school.
- **Gap:** The current `SCHOOL_RULE_MAP` only covers 22 rules (R01-R22). The 25,000+ Phase 1B rules need their school field validated at build time.
- **Recommendation (NOW):** V2ChapterBuilder already sets `school` per chapter. Add an audit check that verifies: no rule with `school="kp"` has `house_system="sign_based"` (KP uses Placidus). No rule with `school="jaimini"` references graha drishti (Jaimini uses rashi drishti). These are domain-specific invariants.

**7.1.2 School-Specific Field Validation**
- **What it prevents:** KP rules without sublord information, Jaimini rules without chara karaka information.
- **When it matters:** Phase 1 onward.
- **Status: PARTIALLY BUILT.** `school_specific` dict field exists.
- **Recommendation (FOUNDATION):** Define school-specific required fields:
  - KP: `school_specific.sublord_level`, `school_specific.significators`
  - Jaimini: `school_specific.chara_karaka`, `school_specific.rashi_drishti`
  - Lal Kitab: `school_specific.remedy_house`, `school_specific.debt_type`
  - Nadi: `school_specific.nadi_sequence`
  Validate these in audit. Not a hard error now (too few non-Parashari rules), but enforce from the session that encodes each school's text.

### 7.2 System Isolation

**7.2.1 System Field Enforcement**
- **What it prevents:** Horary rules being used for natal chart analysis. Muhurtha rules being used for personality prediction.
- **When it matters:** Phase 1 onward; critical for Phase 2.
- **Status: PARTIALLY BUILT.** `system` field on every rule (natal, horary, varshaphala, muhurtha, transit).
- **Recommendation (NOW):** Add audit check: rules from Prasna Marga must have `system="horary"`. Rules from Tajika Neelakanthi must have `system="varshaphala"`. Rules from Muhurtha Chintamani must have `system="muhurtha"`. This is source-text-level validation that prevents the most common system contamination.

**7.2.2 Ayanamsha Sensitivity Tracking**
- **What it prevents:** Sign-placement rules producing different results under different ayanamshas without the user being aware.
- **When it matters:** Phase 1 onward; critical for Phase 7 (product).
- **Status: BUILT.** `ayanamsha_sensitive: bool` is auto-derived at build time (True when `placement_type == "sign_placement"`).
- **Recommendation (FOUNDATION):** Extend to house-system sensitivity: rules with `house_system="sign_based"` give different results from `house_system="bhava_chalita"`. Add `house_system_sensitive: bool` derived similarly.

### 7.3 House System Compatibility

**7.3.1 House System Declaration**
- **What it prevents:** Mixing equal-house (sign-based) and Placidus/Koch house systems within the same analysis, producing contradictions.
- **When it matters:** Phase 2 onward.
- **Status: PARTIALLY BUILT.** `house_system` field exists on RuleRecord (sign_based, bhava_chalita, kp).
- **Recommendation (FOUNDATION):** Ensure Phase 2 engine routes rules to the correct house computation. A rule with `house_system="kp"` must use Placidus cusps, not equal houses.

---

## 8. DATA GOVERNANCE FOR TEMPORAL MODEL

### 8.1 Dasha Scope Completeness

**8.1.1 Dasha-Dependent Rule Enforcement**
- **What it prevents:** Rules claiming `outcome_timing="dasha_dependent"` without specifying which dasha, making them uncomputable by the temporal model.
- **When it matters:** Phase 5 (temporal model).
- **Status: PARTIALLY BUILT.** `_apply_derived_fields()` in `combined_corpus.py` auto-derives `dasha_scope` from planet in primary_condition.
- **Recommendation (NOW):** Add audit check: every rule with `outcome_timing="dasha_dependent"` must have non-empty `dasha_scope`. Currently a gap.

### 8.2 Promise vs Delivery Distinction

**8.2.1 Natal Permanent vs Dasha-Activated Classification**
- **What it prevents:** The temporal model treating a permanent trait rule (e.g., "native has dark complexion") as something that activates in a specific dasha.
- **When it matters:** Phase 5.
- **Status: PARTIALLY BUILT.** `_apply_derived_fields()` fixes `outcome_timing` to "natal_permanent" for traits.
- **Recommendation (FOUNDATION):** Document the classification explicitly: `natal_permanent` = always active (traits, general tendencies); `dasha_dependent` = activates only in specific dasha windows; `early_life`/`middle_life`/`late_life` = time-scoped but not dasha-gated.

### 8.3 Transit Rule Separation

**8.3.1 Transit vs Natal Rule Tagging**
- **What it prevents:** Transit rules (which describe temporary conditions) being weighted identically to natal rules (which describe permanent chart configurations).
- **When it matters:** Phase 5.
- **Status: BUILT.** `system="transit"` tag exists.
- **Recommendation (FOUNDATION):** Ensure the Phase 5 temporal engine treats `system="transit"` rules as having a defined activation window (while transit is active) and an automatic decay (when transit passes).

---

## 9. DATA GOVERNANCE FOR FAMILY/MULTIGENERATIONAL

### 9.1 Entity Completeness

**9.1.1 Entity Target Coverage Audit**
- **What it prevents:** The multigenerational model having blind spots because certain family entities were never tagged during encoding.
- **When it matters:** Phase 8 (multigenerational).
- **Status: PARTIALLY BUILT.** `entity_target` field exists. Audit checks validity.
- **Recommendation (FOUNDATION):** Run a distribution audit at the end of Phase 1: what percentage of rules target each entity? If "father" rules are 2% and "spouse" rules are 15%, the multigenerational model will have uneven coverage. Document the distribution and flag gaps.

### 9.2 Consent Boundaries

**9.2.1 Family Member Consent Enforcement (G03.6)**
- **What it prevents:** Generating predictions about a user's father/spouse/children without their independent consent.
- **When it matters:** Phase 8.
- **Status: PARTIALLY BUILT.** `src/privacy/family_consent.py` exists.
- **Recommendation (LATER, Phase 8):** Every rule with `entity_target != "native"` generates a prediction about someone who is NOT the consenting user. The Phase 8 consent model must require independent consent from the entity (or explicit legal analysis of derived-data processing rights under DPDP/GDPR). Encode the consent boundary at the corpus level now: `requires_entity_consent: bool` derived from `entity_target != "native"`.

### 9.3 Derived House Chain Completeness

**9.3.1 Bhavat Bhavam Auto-Computation**
- **What it prevents:** Rules with house references that do not carry their BB chain implications, weakening the multigenerational model.
- **When it matters:** Phase 8.
- **Status: BUILT.** `bb_reference.py` auto-computes BB chains. V2ChapterBuilder auto-populates `derived_house_chains` via `_auto_bb_chains()`. Slip-through check 4 in `corpus_audit.py` flags empty chains for house-specific rules.

---

## 10. DATA GOVERNANCE FOR RESEARCH AND REPRODUCIBILITY

### 10.1 Corpus Versioning

**10.1.1 Immutable Corpus Snapshots**
- **What it prevents:** Research findings being based on a corpus that has changed since the analysis, making replication impossible.
- **When it matters:** Phase 6 (ML pipeline), Phase 10 (research).
- **Recommendation (FOUNDATION):** Define the snapshot format now (JSON serialization of all rules with SHA-256 hash). Build `src/corpus/snapshot.py`. Every OSF pre-registration includes the corpus hash.

**10.1.2 Corpus Diff Between Snapshots**
- **What it prevents:** Inability to identify what changed between two corpus versions when a model's behavior changes.
- **When it matters:** Phase 6 onward.
- **Recommendation (LATER, Phase 6):** Build `corpus_diff(snapshot_a, snapshot_b) -> ChangeSet` showing added/removed/modified rules.

### 10.2 Pre-Registration Compatibility

**10.2.1 Feature Definition Correspondence**
- **What it prevents:** OSF pre-registration specifying features that do not map cleanly to corpus fields, or corpus changes breaking the feature mapping.
- **When it matters:** Phase 6.
- **Status: DESIGNED.** `osf_registration.py` exists.
- **Recommendation (FOUNDATION):** Each pre-registered feature must map to a specific `evaluation_method` and `primary_condition` pattern. Document the mapping in the OSF filing. This is a documentation discipline, not a code feature.

### 10.3 Cross-Validation Split Integrity

**10.3.1 Temporal Split Enforcement**
- **What it prevents:** Training on post-2010 data that was supposed to be reserved for testing.
- **When it matters:** Phase 6.
- **Status: BUILT.** `cv_splitter.py` implements time-split CV.
- **Recommendation (FOUNDATION):** The corpus itself does not contain chart data — it contains rules. But rules encoded FROM specific charts (if any exist) must be tagged to prevent leakage.

---

## 11. OPERATIONAL GOVERNANCE

### 11.1 Encoding Session Management

**11.1.1 Session Scope Boundaries**
- **What it prevents:** A single encoding session modifying rules from multiple texts or chapters, creating diffuse changes that are hard to audit.
- **When it matters:** Phase 1 (current).
- **Status: ENFORCED BY CONVENTION.** Each session encodes one chapter or one text section.
- **Recommendation (NOW):** Add to `V2ChapterBuilder` a `max_rules_per_build: int = 200` safety limit. If a chapter genuinely has more than 200 rules, it should be split across sessions (as Saravali was). This prevents runaway sessions that encode hastily to meet an artificial count.

**11.1.2 Parallel Encoder Conflict Resolution**
- **What it prevents:** Two encoding agents working on overlapping text sections simultaneously, producing conflicting rules.
- **When it matters:** Not currently relevant (single encoder). Relevant if encoding is parallelized.
- **Recommendation (LATER):** If parallelized, implement chapter-level locking: each builder file declares its chapter range. Two builders cannot claim overlapping ranges.

### 11.2 Error Correction Protocols

**11.2.1 Post-Encoding Rule Correction**
- **What it prevents:** An encoding error discovered weeks later (e.g., wrong entity_target on 50 rules) being silently fixed without audit trail.
- **When it matters:** Phase 1 onward; critical for Phase 6 (model already trained on wrong data).
- **Recommendation (NOW):** Define the correction protocol:
  1. Create a correction session (e.g., S311-FIX)
  2. Update `last_modified_session` on every corrected rule to the correction session
  3. If a model has been trained on the incorrect data (Phase 6+), record the correction in the model's changelog and assess whether retraining is needed
  4. Never delete the original rule — mark as `phase="1A_deprecated"` and create a new corrected rule

**11.2.2 Rule Deprecation Workflow**
- **What it prevents:** Rules being silently removed from the corpus, breaking model feature spaces and audit trails.
- **When it matters:** Phase 1 onward.
- **Status: PARTIALLY BUILT.** `phase="1A_deprecated"` value exists.
- **Recommendation (NOW):** Add `deprecated_reason: str = ""` to RuleRecord. When a rule is deprecated, the reason must be recorded (e.g., "superseded by BPHS1201 with corrected entity_target").

### 11.3 Migration Protocols

**11.3.1 Phase 1A to Phase 1B Migration**
- **What it prevents:** Phase 1A rules being treated as Phase 1B rules or double-counted.
- **When it matters:** Phase 1 (current).
- **Status: BUILT.** Phase 1A rules carry `phase="1A_representative"`. Phase 1B rules carry `phase="1B_*"`. Both coexist in the combined corpus.
- **Governance rule:** Phase 1A rules are NEVER upgraded in place. They are deprecated and replaced by Phase 1B rules. This preserves the audit trail.

---

## 12. SCHEMA EVOLUTION GOVERNANCE

### 12.1 Adding New Fields

**12.1.1 Backward Compatibility Protocol**
- **What it prevents:** New fields breaking existing rules that were created before the field existed.
- **When it matters:** Every schema change (has already happened: S263, S305, S309).
- **Status: WORKING.** All new fields have backward-compatible defaults. RuleRecord uses Python dataclass defaults.
- **Governance rule:** Every new field MUST have a default value that means "not yet populated." The audit enforcement gate (V2_ENFORCEMENT_START) ensures only rules from the relevant session onward are held to the new standard.

**12.1.2 Schema Change Gating**
- **What it prevents:** Mid-encoding schema changes that invalidate rules encoded earlier in the same phase.
- **When it matters:** Phase 1 onward.
- **Status: PARTIALLY ENFORCED.** `PHASE1B_RULE_CONTRACT.md` states it is "Not modifiable during encoding sessions — only in designated schema review sessions."
- **Recommendation (NOW):** Enforce this by convention: schema changes to RuleRecord require a dedicated session (like S309 was), not a side-commit in an encoding session.

**12.1.3 Field Deprecation Protocol**
- **What it prevents:** Old fields lingering in the schema forever, confusing future developers.
- **When it matters:** Phase 2 onward.
- **Recommendation (FOUNDATION):** When a field is no longer used, do not remove it from the dataclass. Instead: (1) add a comment marking it deprecated, (2) add an audit warning if new rules populate it, (3) never remove it from the schema (old rules still have it serialized).

### 12.2 Forward Compatibility

**12.2.1 Anticipatory Fields**
- **What it prevents:** Expensive retrofitting when later phases need metadata that was not captured during encoding.
- **When it matters:** Now — this is the primary motivation for FOUNDATION recommendations throughout this document.
- **Summary of recommended new fields:**

| Field | Type | Default | Purpose | Phase Needed |
|-------|------|---------|---------|-------------|
| `translator` | str | "" | Multi-translator provenance | Phase 10 |
| `encoding_session_context` | str | "" | Conversation context for provenance | Phase 1+ |
| `schema_version` | int | 1 | Robust version discrimination | Phase 2+ |
| `health_sensitive` | bool | False | G02 health content suppression | Phase 7 |
| `safety_tier` | str | "standard" | Content safety classification | Phase 7 |
| `falsifiable` | bool | True | Bayesian update eligibility | Phase 3 |
| `requires_entity_consent` | bool | False | Family member consent boundary | Phase 8 |
| `deprecated_reason` | str | "" | Audit trail for removed rules | Phase 1+ |

---

## IMPLEMENTATION PRIORITY MATRIX

### Tier 1: Build NOW (Phase 1, Current Sessions)

| Control | Ref | Implementation |
|---------|-----|----------------|
| Condition primitive whitelist | 1.1.1 | V2ChapterBuilder validates `conditions[i].type` against 8 primitives |
| Controlled vocabulary enforcement | 1.1.2 | Create `src/corpus/taxonomy.py`; validate domains, direction, intensity, school, system, phase at build time |
| Planet name normalization at build | 1.1.3 | Call `normalize_planet_name()` in `_build_primary_condition()` |
| Confidence recomputation check | 1.1.4 | Audit check that stored confidence matches formula |
| Entity keyword detection | 1.2.2 | Extend audit with keyword scan from v2_scorecard.py |
| Dasha timing extraction | 1.2.4 | Extend regex in slip-through check 2 |
| Interpretive latitude protocol | 1.2.3 | Add Protocol G to ENCODING_PROTOCOL_V2.md |
| Source text canonicalization | 2.3.1 | Create `src/corpus/source_texts.py` |
| ID collision prevention | 2.1.3 | Create `src/corpus/id_registry.py` |
| Bidirectional concordance audit | 2.2.1 | Add audit check for orphaned concordance |
| System-source validation | 7.2.1 | Audit: Prasna Marga=horary, Tajika=varshaphala, Muhurtha=muhurtha |
| Dasha scope completeness | 8.1.1 | Audit: dasha_dependent requires non-empty dasha_scope |
| Health sensitivity derivation | 5.1.1 | Add to `_apply_derived_fields()` |

### Tier 2: Lay FOUNDATION Now (Add Field/Schema, Build Enforcement Later)

| Control | Ref | Foundation Action |
|---------|-----|-------------------|
| Translator tracking | 3.1.2 | Add `translator: str = ""` to RuleRecord |
| Encoding context | 3.1.2 | Add `encoding_session_context: str = ""` to RuleRecord |
| Schema version | 2.4.2 | Add `schema_version: int = 1` to RuleRecord |
| Health sensitive flag | 5.1.1 | Add `health_sensitive: bool = False` to RuleRecord |
| Safety tier | 5.2.1 | Add `safety_tier: str = "standard"` to RuleRecord |
| Falsifiability flag | 6.1.1 | Add `falsifiable: bool = True` to RuleRecord |
| Entity consent flag | 9.2.1 | Add `requires_entity_consent: bool = False` to RuleRecord |
| Deprecated reason | 11.2.2 | Add `deprecated_reason: str = ""` to RuleRecord |
| Corpus snapshot API | 10.1.1 | Define `snapshot.py` interface |
| Concordance map auto-regeneration | 2.2.3 | Add to pre-push hook |
| Per-text commentary thresholds | 1.2.5 | `text_commentary_richness` in builder config |

### Tier 3: Build LATER (When Phase Arrives)

| Control | Phase | Description |
|---------|-------|-------------|
| Rule firing audit trail | 2 | Engine returns RuleFiringRecord per prediction |
| Convergence state recording | 3 | predictions table columns: layer1_concordance, convergence_tier |
| Credibility scoring | 3 | Build before first Bayesian update |
| Temporal window management | 3 | prediction_expiry policy per timing_window.type |
| Corpus diff tool | 6 | corpus_diff(snapshot_a, snapshot_b) |
| Feature definition freezing | 6 | Corpus snapshot hash in OSF filings |
| Model-corpus version pinning | 6 | Model artifact records corpus hash |
| Parallel encoder locking | If parallelized | Chapter-level locking |
| Sanskrit verification | 10 | scholar spot-check, verse_verified field |
| Inter-translator reliability | 10 | Compare Santhanam vs GC Sharma encodings |

---

## EDGE CASE GOVERNANCE (What Happens When Things Go Wrong)

### Edge Case 1: Encoding Error Discovered After Model Training
- **Scenario:** Rule BPHS1205 has entity_target="native" but should be "father". This was discovered in S500 after the Phase 6 model was trained.
- **Protocol:**
  1. Create correction session S500-FIX
  2. Deprecate BPHS1205 with `deprecated_reason="wrong entity_target; native should be father"`
  3. Create BPHS1205v2 with correct entity_target, `last_modified_session="S500-FIX"`
  4. Record the corpus hash of the corrected corpus
  5. Evaluate: did the error affect any trained model? If BPHS1205 contributed to any feature in the trained model, flag the model as `needs_retraining` in MLflow metadata
  6. If retraining, the new model must be trained on the corrected corpus snapshot

### Edge Case 2: User Complaint About Incorrect Prediction
- **Scenario:** User says "you told me my career would improve in 2027 and it didn't."
- **Protocol:**
  1. Look up the prediction in the prediction ledger
  2. The prediction carries `rule_ids_contributing` (from the firing audit trail)
  3. For each contributing rule, examine `confidence`, `concordance_texts`, `convergence_tier`
  4. If convergence_tier was "L1_only" (no empirical calibration), the prediction was issued with appropriate caveats (G25)
  5. The feedback is recorded as a disconfirmation event with the full convergence state
  6. This is a normal Layer III training signal, not a defect

### Edge Case 3: Regulatory Inquiry About Health Predictions
- **Scenario:** Indian regulator asks: "does your system predict disease or death?"
- **Protocol:**
  1. The corpus DOES contain longevity and health rules (because classical texts discuss them)
  2. Every such rule is tagged `health_sensitive=True` and `safety_tier="restricted"` or `"research_only"`
  3. The API layer (Phase 7) filters out all restricted rules from user-facing output
  4. Demonstrate the filtering gate: show that no API response ever contains health predictions
  5. Show the consent ledger: health-adjacent features (if any are internal-research) have separate consent flags
  6. Show the DPIA: completed before any health-adjacent feature was activated

### Edge Case 4: Two Texts Directly Contradict on the Same Configuration
- **Scenario:** BPHS says "Saturn in 7th delays but stabilizes marriage"; CCC says "Saturn in 7th destroys marriage."
- **Protocol:**
  1. Both rules are encoded faithfully (1.2.3 — encoder records the text's claim)
  2. Both carry `divergence_notes` pointing to each other
  3. Confidence for both is reduced by the divergence penalty (-0.05)
  4. If concordance < 0.35 for this configuration across all schools, the anti-prediction zone fires (Layer 4) and no user-facing assessment is issued
  5. This divergence is a Phase 10 research finding: a genuine scholarly disagreement preserved in machine-readable form

### Edge Case 5: Ayanamsha Change Invalidates Sign-Placement Rules
- **Scenario:** A user switches from Lahiri to Krishnamurti ayanamsha. All sign-placement rules shift.
- **Protocol:**
  1. Every sign-placement rule is tagged `ayanamsha_sensitive=True`
  2. The engine re-evaluates all ayanamsha-sensitive rules when ayanamsha changes
  3. The prediction ledger records `ayanamsha_used` per chart (G06)
  4. Historical predictions made under Lahiri are NOT retroactively modified — they are marked with the ayanamsha they were computed under
  5. The user is shown: "Switching ayanamsha changes the following assessments: [list]"

### Edge Case 6: Corpus Grows From 3,000 to 25,000 Rules — Performance at Scale
- **Scenario:** `build_corpus()` in `combined_corpus.py` imports 100+ registries and iterates all rules multiple times.
- **Protocol:**
  1. Current build is import-heavy but runs at module load time. At 25,000 rules, this may take 5-10 seconds.
  2. Pre-compute and cache: the `COMBINED_CORPUS` singleton should be built once and cached. In production, serialize to a binary format (e.g., pickle or msgpack) and load from cache.
  3. Audit and concordance checks should run in CI, not at every import.
  4. Recommendation (Phase 2): Split `build_corpus()` into `build_corpus()` (fast, no auditing) and `audit_corpus()` (slow, thorough). CI runs both. Production loads cached result.

---

## GOVERNANCE REVIEW CADENCE

| Review | Frequency | Scope |
|--------|-----------|-------|
| **Per-session audit** | Every encoding session | V2 scorecard, slip-through checks, concordance verification |
| **Per-text completion audit** | After each text is fully encoded | Coverage map completeness, 10% contract spot check, taxonomy consistency |
| **Phase gate review** | At each phase boundary | Full corpus audit, distribution analysis, gap identification |
| **Schema review session** | As needed (not during encoding) | RuleRecord field additions, taxonomy extensions, protocol changes |
| **Pre-OSF filing review** | Before each OSF registration | Feature definition freeze, corpus snapshot, split integrity |
| **Annual governance review** | Yearly | Full framework review, regulatory compliance check, new risk assessment |

---

### Critical Files for Implementation

- `/Users/harsh/LagnaMaster/src/corpus/rule_record.py` — The 45-field RuleRecord dataclass. All new FOUNDATION fields (translator, schema_version, health_sensitive, safety_tier, falsifiable, requires_entity_consent, deprecated_reason) must be added here with backward-compatible defaults.
- `/Users/harsh/LagnaMaster/src/corpus/corpus_audit.py` — The 8 hard errors + 3 warnings enforcement engine. All NOW-tier validation additions (controlled vocabulary, bidirectional concordance, system-source validation, dasha scope completeness, entity keyword detection, confidence recomputation) are implemented here.
- `/Users/harsh/LagnaMaster/src/corpus/v2_builder.py` — The V2ChapterBuilder that gates all new encoding. Condition primitive whitelist, planet normalization, and domain taxonomy validation are added to the `add()` and `build()` methods here.
- `/Users/harsh/LagnaMaster/src/corpus/combined_corpus.py` — The corpus assembly pipeline where `_apply_derived_fields()` runs. Health sensitivity derivation, safety tier derivation, and falsifiability derivation are added here.
- `/Users/harsh/LagnaMaster/docs/ENCODING_PROTOCOL_V2.md` — The 6 mandatory protocols document. Protocol G (Interpretive Latitude) and the error correction protocol are documented here.