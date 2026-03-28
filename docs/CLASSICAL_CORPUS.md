# CLASSICAL_CORPUS.md — Classical Knowledge Status
> **Update this file as texts are encoded and corpus grows.**
> Phase 1 (S216–S410) is the most critical phase in the project.

---

## Core Insight (from GPT Corpus Analysis)

> "The 42 Laghu Parashari sutras represent ~25-35% of full Parashari Jyotish.
> Our current 23 rules represent perhaps **1-2%** of the classical predictive system."

23 rules cannot capture 1,500+ needed. Every downstream feature (feature vectors, temporal model, SHAP analysis) changes accordingly once Phase 1 closes the gap.

---

## Current State (Post-S188)
### Modules Built vs Rules Encoded

Having a module is not the same as having the rules within it encoded correctly or completely.
This distinction matters for sessions building on top of existing modules.

| Domain | Module | Module Status | Rules Encoded | Known Gap |
|--------|--------|---------------|---------------|-----------|
| Shadbala | `shadbala.py` | ✅ Built | Partial | Kala Bala 8 sub-components unverified (SK-1) |
| Yogas | `yogas.py` + `extended_yogas.py` + `yogas_graha.py` + `yogas_pvrnr.py` | ✅ Built | ~35 of 300+ | 265+ named yogas missing |
| Varga | `divisional_charts.py` + `varga.py` | ✅ Built | D1–D60 formulas | Drekkana variants (Jagannatha, Somanatha) missing |
| Ashtakavarga | `ashtakavarga.py` | ✅ Built | SAV correct (fixed totals verified) | Full Prastarashtakavarga missing |
| Dasha | `vimshottari_dasa.py` + `narayana_dasa.py` | ✅ Built | 2 of 44 systems | 42 additional systems (Ashtottari, Yogini, Kalachakra, Chara, Shoola...) |
| Jaimini | `jaimini_full.py` | ✅ Built | Brahma/Maheshvara/Rudra, Pada | Chara dashas, full karakamsha system incomplete |
| KP | `kp.py` + `kp_full.py` | ✅ Built | Sub-lord table (249 entries) | Cusps are whole-sign, not Placidus; Krishnamurti ayanamsha not used (G06) |
| Classical strength | `orb_strength.py` | ✅ Built | PVRNR orb decay | Full Bala framework not yet driving concordance weights |
| Avastha | `avastha_v2.py` + `sayanadi_full.py` | ✅ Built | 12-state Sayanadi | Jagradadi, Deeptadi partial |
| Longevity | `longevity.py` + `ayurdaya.py` | ✅ Built | 3 methods | Never user-facing (G02) |

**Reading this table:** A session that touches `shadbala.py` cannot assume Kala Bala
sub-components are correct. A session using yoga output cannot assume 265+ missing yogas
don't affect the result. The module existing does not mean the domain is done.

---

### Corpus Encoding Priorities by Convergence Layer

Not all corpus work has equal impact on the convergence model. Encoding priorities
should be weighted by which convergence layer they strengthen and how:

**Highest priority — directly strengthens Layer I concordance:**
- BPHS Chapters that apply to ALL three schools (Parashari/KP/Jaimini) — encoding
  these creates rules that can fire independently from multiple schools, raising the
  maximum achievable concordance score
- Rules that distinguish yogakaraka behavior by lagna — these address the root cause
  of OB-3's low axis-specific r (~0.02) because Saturn in H7 from Cancer ≠ Saturn in H7
  from Capricorn, and the corpus needs to encode this distinction explicitly

**High priority — strengthens Layer II capacity/delivery:**
- Dasha interpretation rules (BPHS Ch.46, Uttara Kalamrita timing sutras) — these
  directly govern the Capacity check in `promise_engine.py`
- Argala and virodha argala rules — these affect the activation weight in `narayana_argala.py`
- Transit interaction rules (Gochar chapter BPHS) — these govern the Delivery gate

**Medium priority — deepens Layer I but doesn't increase school count:**
- Additional yoga rules within Parashari only — these add rules to a school already
  present, raising rule depth but not concordance potential
- Nabhasa Sankhya expansion — structural yogas that describe chart patterns, not
  cross-school signals

**Lower priority (research layer, Phase 6+):**
- Medical/longevity texts (Ayurveda-adjacent) — governed by G02, internal research only
- Lal Kitab — requires separate schema, doesn't contribute to main concordance model
- Nadi texts — Chandra Kala Nadi schema is fundamentally different, separate pipeline

---



| Component | Status | Gap |
|-----------|--------|-----|
| Classical rules active | 23 (R01–R23, all wired as of S188) | ~1,477+ rules missing from 1,500+ target |
| BPHS chapters encoded | ~15 of 97 | 82 chapters unencoded |
| Named yogas | 13 types (detect_yogas) | VedAstro has 1,000+; target 310+ at Phase 1 |
| Dasha systems | 2 (Vimshottari + Narayana) | 42 more systems (target 44) |
| Divisional charts | D1–D9 confirmed, D10 partial | D12 (ancestral) + D16-D60 missing |
| Shadbala | 6 components present | Kala Bala sub-components unverified (SK-1) |
| Ashtakavarga | SAV implemented, fixed totals verified | Full Prastarashtakavarga missing |
| Ayanamsha | Lahiri only | Krishnamurti for KP (G06 violation), True Chitrapaksha missing |
| Jaimini calculations | Chara Karakas (7) in chara_karak.py | Pada lagnas, Jaimini aspects incomplete |
| Functional dignity | Wired to R02/R09 as of S162 | Schema in place, yogakaraka weight variant active |

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

### Check Online

| Text | Source | Est. Rules |
|------|--------|-----------|
| Saravali | pdfcoffee.com / scribd | ~150 |
| Phala Deepika | archive.org | ~120 |
| Bhavartha Ratnakara | archive.org | ~100 |

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

## Phase 1 Encoding Plan (S216–S410)

| Sessions | Text | Target Rules | Priority |
|----------|------|-------------|---------|
| S216–S250 | BPHS all 97 chapters | 800+ | Ch.36-45 (Yogas) → Ch.16-25 (Dashas) → Ch.26-35 (House results) |
| S251–S290 | Brihat Jataka + Uttara Kalamrita + Jataka Parijata + Sarwarthachintamani | 630+ | Uttara Kalamrita Bindu 2 (timing) = highest priority |
| S291–S325 | Jaimini Sutras + Lal Kitab + Chandra Kala Nadi | 370+ | Separate schemas; Jaimini first |
| S326–S360 | Yoga expansion: 13 → 310+ | 310 yogas | Pancha Mahapurusha (5), Rajayogas (50+), Nabhasa (32), Arishta (30+) |
| S361–S380 | Complete Shadbala + 10 Dasha Systems + D12–D60 + Full Ashtakavarga | 4 major gaps | Shadbala first (unblocks full concordance in HouseScore) |
| S381–S410 | Corpus finalization + Jaimini + Special Lagnas + V1.0 lock | 1,500+ total | Lock before OSF pre-registration |

**AI-assisted extraction prompt template:**
```
Extract astrological rules from this BPHS chapter as JSON with fields:
rule_id, source_text, chapter, verse, planet, condition, effect_domain,
effect_direction, effect_magnitude, classical_weight, school, notes.
```
**⚠️ Human review required for EVERY extracted rule before commit. Never commit without verification.**

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
