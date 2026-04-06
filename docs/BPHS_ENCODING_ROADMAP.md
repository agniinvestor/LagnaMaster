# BPHS Complete Encoding Roadmap — All 97 Chapters

**Created:** S316 (2026-04-06)
**Source:** BPHS Santhanam Vol 1 (Ch.1-45) + Vol 2 (Ch.46-97)
**Purpose:** Master plan for encoding the complete BPHS. Every chapter classified, prioritized, and dependency-mapped.

## Classification Key

| Type | Meaning | Encoding approach |
|------|---------|-------------------|
| **DEF** | Definitional — defines terms, entities, categories | Engine constants + taxonomy |
| **COMP** | Computational — defines HOW to calculate something | Engine computation modules |
| **PRED** | Predictive — makes claims about life outcomes | V2 structured rules |
| **TIMING** | Timing system — defines dasha periods and effects | Dasha engine modules |
| **REMEDY** | Remedial measures | Lower priority, non-predictive |

## Status Key

| Status | Meaning |
|--------|---------|
| ✅ ENCODED | V2 rules or engine code exists |
| ⚙️ PARTIAL | Some computation exists, incomplete |
| ❌ NOT DONE | Not encoded |

---

## Vol 1: Chapters 1-45

### FOUNDATIONAL LAYER (Ch.1-11)

These chapters define the system. Everything downstream depends on them.

| Ch | Title | Type | Status | Depends On | Blocks | Priority | Est. Rules/Components |
|----|-------|------|--------|------------|--------|----------|----------------------|
| 1 | The Creation | DEF | ❌ | None | — | LOW | 0 rules — cosmological context only |
| 2 | Great Incarnations of the Lord | DEF | ❌ | None | — | LOW | 0 rules — avatara descriptions |
| 3 | Planetary Characters and Description | DEF+COMP | ⚙️ PARTIAL | None | Ch.7, 26, 27, 34 | **CRITICAL** | Benefics/malefics, dignities, exaltation/debilitation, planetary relationships (friend/enemy/neutral), upagraha calculations, Gulika position. **Engine has hardcoded tables. Need to verify against text and encode missing: planetary relationships (temporary + compound), Dhatu/Moola/Jeeva divisions.** |
| 4 | Zodiacal Signs Described | DEF | ⚙️ PARTIAL | None | Ch.6, 11, 34 | **HIGH** | Sign characteristics, limbs of Kalapurusha, 12 sign descriptions, Nisheka Lagna calculation. **Engine has sign data but Nisheka Lagna not implemented.** |
| 5 | Special Ascendants | COMP | ⚙️ PARTIAL | Ch.3, 4 | Ch.29, 30 | **HIGH** | Bhava Lagna, Ghatika Lagna, Hora Lagna, Varnada Dasa. **Some special lagnas implemented, Varnada Dasa not.** |
| 6 | The Sixteen Divisions of a Sign | COMP | ⚙️ PARTIAL | Ch.4 | Ch.7, 27, 34 | **CRITICAL** | All 16 vargas (D1-D60): Hora, Drekkana, Chaturthamsa, Sapthamsa, Navamsa, Dasamsa, Dvadasamsa, Shodasamsa, Vimsamsa, Chaturvimsamsa, Saptavimsamsa, Trimsamsa, Khavedamsa, Akshavedamsa, Shashtiamsa, Varga classification. **D1-D10 partial, D12-D60 mostly missing.** |
| 7 | Divisional Consideration | COMP | ⚙️ PARTIAL | Ch.6 | Ch.27, 34 | **CRITICAL** | Vimshopaka strength (strength from divisional placement), how to use divisional charts for prediction. **Vimshopaka partially implemented.** |
| 8 | Aspects of the Signs | COMP | ⚙️ PARTIAL | Ch.4 | Ch.26, 33 | **HIGH** | Jaimini rasi aspects (different from graha aspects in Ch.26), sign-to-sign aspectual relationships. **Graha aspects implemented, Jaimini rasi aspects not.** |
| 9 | Evils at Birth | PRED | ❌ | Ch.3, 4, 8 | Ch.10 | **HIGH** | Short life combinations, evils to mother/father/parents. Arishta yoga — critical for longevity assessment. **Not encoded. Contains predictive rules about infant mortality indicators.** |
| 10 | Antidotes for Evils | PRED+REMEDY | ❌ | Ch.9 | — | MEDIUM | Planetary combinations that cancel evils of Ch.9. Contains Balarishta cancellation yogas. **Not encoded.** |
| 11 | Judgement of Houses | COMP+PRED | ⚙️ PARTIAL | Ch.3, 4, 8 | Ch.12-24 | **CRITICAL** | Indications of houses 1-12, prosperity or annihilation of a house. **THIS IS THE METHODOLOGY CHAPTER. Defines HOW to evaluate a house — lord placement, occupants, aspects, strength. The 23-rule engine (R01-R23) is based on this chapter. But encoded as workbook rules, not from the text directly.** |

### HOUSE EFFECTS (Ch.12-24) — ENCODED ✅

| Ch | Title | Type | Status | Rules |
|----|-------|------|--------|-------|
| 12 | Effects of 1st House | PRED | ✅ | 22 |
| 13 | Effects of 2nd House | PRED | ✅ | 26 |
| 14 | Effects of 3rd House | PRED | ✅ | 22 |
| 15 | Effects of 4th House | PRED | ✅ | 14 |
| 16 | Effects of 5th House | PRED | ✅ | 32 |
| 17 | Effects of 6th House | PRED | ✅ | 20 |
| 18 | Effects of 7th House | PRED | ✅ | 42 |
| 19 | Effects of 8th House | PRED | ✅ | 6 |
| 20 | Effects of 9th House | PRED | ✅ | 30 |
| 21 | Effects of 10th House | PRED | ✅ | 20 |
| 22 | Effects of 11th House | PRED | ✅ | 10 |
| 23 | Effects of 12th House | PRED | ✅ | 10 |
| 24 | Effects of Bhava Lords | PRED | ✅ | 158 |

### SPECIAL EFFECTS (Ch.25-31) — PARTIALLY ENCODED

| Ch | Title | Type | Status | Depends On | Priority | Notes |
|----|-------|------|--------|------------|----------|-------|
| 25 | Effects of Non-Luminous Planets | PRED | ✅ | Ch.3 (upagraha calc) | — | 85 rules. Dhuma, Vyatipata, etc. |
| 26 | Evaluation of Planetary Aspects | COMP | ❌ | Ch.3, 8 | **CRITICAL** | Defines planetary aspects quantitatively — aspectual strength percentages. Special aspects of Saturn, Mars, Jupiter with exact values. **Engine hardcodes aspects. This chapter provides the classical calculation method.** |
| 27 | Evaluation of Strengths (SHADBALA) | COMP | ⚙️ PARTIAL | Ch.3, 4, 6, 7 | **CRITICAL** | The 6-fold strength system: Sthana Bala, Dig Bala, Kaala Bala, Cheshta Bala, Naisargika Bala, Drig Bala. Also: Bhava Bala (house strength), Bhava effects eligibility based on Shadbala. **shadbala.py exists but gaps vs PyJHora confirmed. Bhava Bala incomplete. This is THE computational foundation — every scoring decision depends on Shadbala.** |
| 28 | Ishta and Kashta Balas | COMP | ⚙️ PARTIAL | Ch.27 | **HIGH** | Exaltation rays, Cheshta Rasmi, benefic and malefic potency. Determines net auspicious vs inauspicious strength. **Partially computed.** |
| 29 | Bhava Padas | PRED | ✅ | Ch.5 | — | 40 rules. Arudha Pada effects. |
| 30 | Upa Pada | PRED | ✅ | Ch.5 | — | 46 rules. Marriage/spouse via Upa Pada. |
| 31 | Argala or Planetary Intervention | PRED+COMP | ✅ | Ch.29 | — | 17 rules. Argala formation and effects. |

### KARAKAS AND YOGAS (Ch.32-42) — NOT ENCODED

These are the MOST PREDICTIVELY IMPORTANT chapters. Yogas are the specific combinations practitioners rely on most heavily.

| Ch | Title | Type | Status | Depends On | Priority | Notes |
|----|-------|------|--------|------------|----------|-------|
| 32 | Planetary Karatwas (Significators) | COMP+PRED | ❌ | Ch.3 | **CRITICAL** | Atmakaraka, other Chara Karakas, Yogakarakas, mutual coworkers, house significance. **Defines the karaka system that the scorer needs. dynamic_karaka primitive exists but the full system isn't encoded.** |
| 33 | Effects of Karakamsa | PRED | ❌ | Ch.32 | **HIGH** | Effects of planets in Karakamsa and houses from Karakamsa. 12 houses × planet combinations. **~100+ predictive rules.** |
| 34 | Yoga Karakas | COMP+PRED | ❌ | Ch.3, 4, 11 | **CRITICAL** | Nature due to lordships of planets, natural benefics and malefics, angular and trinal lordships, angular lordship for each ascendant (Aries through Pisces). **THIS defines yogakaraka/functional benefic/malefic for each lagna. functional_dignity.py is based on this chapter but encoded from secondary sources, not from the text. General principles here.** |
| 35 | Nabhasa Yogas | PRED | ❌ | Ch.3, 4 | **HIGH** | 32 Nabhasa Yogas: Rajju, Musala, Nala, Maala, Sarpa, Gada, Sakata, Vihaga, Sringataka, Hala, Vajra, Yava, Kamala, Vapi, Yupa, Sara, Sakthi, Danda, Nauka, Koota, Chatra, Chapa, Chakra, Samudra, Gola, Yuga, Soola, Kedara, Pasa, Dama, Veena. **Pattern-based yogas from planetary spread across houses.** |
| 36 | Many Other Yogas | PRED | ❌ | Ch.3, 4, 34 | **HIGH** | Subha, Asubha, Gajakesari, Amala, Parvatha, Kahala, Chamara, Sankha, Bheri, Mridanga, Srinatha, Sarada, Matsya, Koorma, Khadga, Lakshmi, Kusuma, Kalanidhi, Kalpadruma, Trimurthi, Lagnadhi. **Named yogas with specific formation rules and predicted effects.** |
| 37 | Lunar Yogas | PRED | ❌ | Ch.3 | **HIGH** | Adhiyoga from Moon, Dhana Yoga, Sunapha, Anapha, Duradhura, Kemadruma. **Moon-based yogas. Kemadruma especially important for mental/emotional assessment.** |
| 38 | Solar Yogas | PRED | ❌ | Ch.3 | MEDIUM | Vesi, Vosi, Ubhayachari. **Sun-based yogas.** |
| 39 | Raja Yogas | PRED | ❌ | Ch.34 | **CRITICAL** | Kingly yogas forming in various manners. **The most sought-after yoga category. Kendra-trikona lord combinations producing power/authority.** |
| 40 | Yogas for Royal Association | PRED | ❌ | Ch.39 | **HIGH** | Association with royalty/government. |
| 41 | Yogas for Wealth | PRED | ❌ | Ch.34 | **HIGH** | Yogas for affluence, effects of angular lord's divisional dignities, effects of 5th lord's divisional dignities, effects of 9th lord's divisional dignities. **Wealth prediction — commercially important.** |
| 42 | Combinations for Penury | PRED | ❌ | Ch.41 | **HIGH** | Poverty combinations. Contrary mirrors to Ch.41. |

### LONGEVITY AND DEATH (Ch.43-45)

| Ch | Title | Type | Status | Depends On | Priority | Notes |
|----|-------|------|--------|------------|----------|-------|
| 43 | Longevity | COMP+PRED | ❌ | Ch.27, 34 | **HIGH** | Pindayu, Nisargayu, Amsayu calculations. Full life span computation. Fixed/movable/common sign longevity pairs. **Multiple computational methods for longevity assessment.** |
| 44 | Maraka (Killer) Planets | PRED | ❌ | Ch.43 | **HIGH** | Marakas based on lordship, maraka dasa, star groups related to death, 3rd house and 8th house occupants. **Death timing — sensitive content (G02 guardrail).** |
| 45 | Avasthas of Planets | COMP+PRED | ❌ | Ch.3 | **HIGH** | Baaladi avasthas (infant/young/adult/old/dead states), Lajjitadi avasthas, Sayanadi avasthas (12 states), Deepta and other avasthas. Effects of each avastha for Sun through Ketu. **Planetary states that modify ALL predictions. A planet in "dead" avastha gives completely different results than one in "adult" avastha.** |

---

## Vol 2: Chapters 46-97

### DASHA SYSTEMS (Ch.46-63)

| Ch | Title | Type | Status | Depends On | Priority | Notes |
|----|-------|------|--------|------------|----------|-------|
| 46 | Dasas (Periods) of Planets | TIMING+COMP | ⚙️ PARTIAL | Ch.3, 27 | **CRITICAL** | Vimshottari (primary system), Ashtottari, Shodasottari, Panchottari, Satabdika, Chaturshitisama, Dwisaptatisama, Shashtihayani, Shatvimsatisama, Kalachakra, Chara, Sthira, Kendra, Brahma Graha Mandook, Yogardha, Shoola, Drig, Rasi, Panchswara, Yogini, Naisargik, Pinda, Sandhya, Ashtavarga, Pachaka, Tara Dasas. **~30 dasha systems listed. Only Vimshottari fully implemented.** |
| 47 | Effects of Dasas | PRED | ❌ | Ch.46 | **CRITICAL** | General principles of dasha effects, effects of each planet's dasha. Auspiciousness based on dignities, placements. **THIS is where timing predictions come from. Not encoded.** |
| 48 | Distinctive Effects of Nakshatra Dasa Lords | PRED | ❌ | Ch.46, 47 | **HIGH** | Effects of dasas of lords of houses 1-12, special comments on inauspiciousness. **House-lord-based dasha effects.** |
| 49 | Effects of Kalachakra Dasa | TIMING+PRED | ⚙️ PARTIAL | Ch.46 | MEDIUM | Kalachakra dasa computation exists. Effects not encoded. |
| 50 | Effects of Chara etc. Dasas | TIMING+PRED | ⚙️ PARTIAL | Ch.46 | MEDIUM | Chara dasa computation exists. Effects not encoded. |
| 51 | Working out Antardasas | COMP | ⚙️ PARTIAL | Ch.46 | **HIGH** | Antardasa calculation methods for Vimshottari, Chara, Kendra systems. **Partially implemented.** |
| 52-60 | Effects of Antardasas (Sun through Venus) | PRED | ❌ | Ch.51 | **HIGH** | 9 chapters, one per planet. Each describes antardasa effects for all sub-periods. **~500+ predictive rules total across 9 chapters.** |
| 61 | Pratyantar Dasas | COMP+PRED | ⚙️ PARTIAL | Ch.51 | MEDIUM | Sub-sub-period calculations and effects. |
| 62 | Sookshmantar Dasas | COMP+PRED | ❌ | Ch.61 | LOW | Sub-sub-sub-period. Very fine timing. |
| 63 | Prana Dasas | COMP+PRED | ❌ | Ch.62 | LOW | Finest timing level. |

### ASHTAKAVARGA SYSTEM (Ch.64-69)

| Ch | Title | Type | Status | Depends On | Priority | Notes |
|----|-------|------|--------|------------|----------|-------|
| 64 | Ashtakavarga introduction | COMP | ⚙️ PARTIAL | Ch.3 | **CRITICAL** | Basic Ashtakavarga computation exists. |
| 65 | Prastarashtakavarga | COMP | ❌ | Ch.64 | **HIGH** | Detailed Ashtakavarga computation. **Full Prastarashtakavarga not implemented — only Sarvashtakavarga (sum).** |
| 66 | Effects of Ashtakavarga | PRED | ⚙️ PARTIAL | Ch.64, 65 | **HIGH** | Predictive effects based on AV bindus. **R23 uses SAV bindus but the full effect system from this chapter is not encoded.** |
| 67-69 | Additional AV effects | PRED | ❌ | Ch.66 | MEDIUM | Extended Ashtakavarga applications. |

### TRANSITS AND ADDITIONAL TOPICS (Ch.70-97)

| Ch | Title | Type | Status | Depends On | Priority | Notes |
|----|-------|------|--------|------------|----------|-------|
| 70-74 | Transit effects | COMP+PRED | ❌ | Ch.3, 64 | **HIGH** | Gochar (transit) system. How current planetary positions modify natal promise. **Critical for timing — not encoded.** |
| 75-80 | Additional predictive methods | PRED | ❌ | Various | MEDIUM | Various predictive techniques. |
| 81-85 | Female horoscopy, marriage | PRED | ❌ | Ch.18, 30 | MEDIUM | Stri Jataka (female chart reading). |
| 86-90 | Muhurta (electional) | COMP+PRED | ❌ | Ch.3, 46 | MEDIUM | Auspicious timing selection. |
| 91-97 | Remedies and miscellaneous | REMEDY | ❌ | Various | LOW | Planetary remedies, gem prescriptions. |

---

## Dependency Graph (Critical Path)

```
Ch.3 (Planetary Characters) ──→ Ch.26 (Aspects) ──→ Ch.27 (Shadbala) ──→ Ch.11 (House Judgement)
       │                                                    │
       ├──→ Ch.4 (Signs) ──→ Ch.6 (Vargas) ──→ Ch.7 (Divisional Use)
       │                                            │
       ├──→ Ch.32 (Karakas) ──→ Ch.33 (Karakamsa Effects)
       │
       ├──→ Ch.34 (Yoga Karakas) ──→ Ch.35-42 (Specific Yogas)
       │                                    │
       │                                    ├──→ Ch.39 (Raja Yogas)
       │                                    └──→ Ch.41 (Wealth Yogas)
       │
       ├──→ Ch.45 (Avasthas) ──→ modifies ALL predictions
       │
       └──→ Ch.46 (Dasha Systems) ──→ Ch.47-48 (Dasha Effects)
                                           │
                                           └──→ Ch.52-60 (Antardasa Effects)

Ch.64 (AV intro) ──→ Ch.65 (Prastarashtakavarga) ──→ Ch.66 (AV Effects)

Ch.9 (Evils at Birth) ──→ Ch.10 (Antidotes)
Ch.43 (Longevity) ──→ Ch.44 (Maraka Planets)
```

---

## Encoding Priority Tiers

### Tier 0: IMMEDIATE (scoring engine prerequisites)
These must be encoded/verified before ANY scoring engine work:

| Ch | What it provides to the engine |
|----|-------------------------------|
| **3** | Planetary relationships (friend/enemy/neutral tables — currently hardcoded, need verification against text). Compound relationships. This feeds the 9-level dignity scale the scorer needs. |
| **11** | House judgement methodology — HOW to evaluate a bhava. The R01-R23 rules are based on this but were encoded from the workbook, not from the text. Need to verify and extend. |
| **27** | Shadbala — 6-fold strength computation. Engine has partial implementation. Gaps vs PyJHora confirmed. This is THE strength assessment that replaces the 5-level dignity lookup. |
| **26** | Aspectual strength — quantitative aspect values. Currently hardcoded as binary (aspects or doesn't). This chapter provides percentage-based aspect strengths. |

### Tier 1: CRITICAL (core predictive system)
Must be encoded before meaningful prediction testing:

| Ch | What it provides |
|----|-----------------|
| **34** | Yoga Karakas — functional benefic/malefic definitions per lagna. Currently from secondary sources. |
| **45** | Avasthas — planetary states that modify all predictions. Not encoded at all. |
| **32** | Karaka system — significator assignments. Primitive exists, full system missing. |
| **39** | Raja Yogas — the highest-impact predictive combinations. Not encoded. |
| **46-47** | Dasha system + effects — timing layer. Computation partial, effects not encoded. |

### Tier 2: HIGH VALUE (major predictive content)
Adds significant predictive power:

| Ch | What it provides |
|----|-----------------|
| **35-36** | Nabhasa + named yogas — 50+ specific pattern-based predictions |
| **37-38** | Lunar + Solar yogas — Moon/Sun based combinations |
| **41-42** | Wealth + Penury yogas — commercially important |
| **43-44** | Longevity + Maraka — life span assessment |
| **9-10** | Birth evils + antidotes — infant/childhood indicators |
| **33** | Karakamsa effects — predictions from significator placement |
| **48, 52-60** | Dasha effects detail — timing-specific predictions (~500+ rules) |
| **64-66** | Full Ashtakavarga system |

### Tier 3: EXTENSION (additional depth)
Adds refinement and edge cases:

| Ch | What it provides |
|----|-----------------|
| **4-8** | Signs, special lagnas, vargas, aspects in full detail |
| **28** | Ishta/Kashta Bala — benefic/malefic potency |
| **40** | Royal association yogas |
| **49-50** | Non-Vimshottari dasha effects |
| **67-69** | Extended AV effects |
| **70-74** | Transit system |

### Tier 4: COMPLETENESS (full corpus)
For academic completeness and specialized features:

| Ch | What it provides |
|----|-----------------|
| **1-2** | Cosmological context |
| **51, 61-63** | Sub-period calculations (very fine timing) |
| **75-80** | Additional predictive methods |
| **81-85** | Female horoscopy |
| **86-90** | Muhurta (electional astrology) |
| **91-97** | Remedies |

---

## Current State vs Required State

| Component | Current | Required (for real scoring) | Gap |
|-----------|---------|---------------------------|-----|
| Dignity scale | 5-level (exalt/MT/own/neutral/debil) | 9-level with friend/enemy from Ch.3 | **Missing 4 levels** |
| Aspect strength | Binary (aspects or doesn't) | Percentage-based from Ch.26 | **Missing gradients** |
| Planetary strength | Partial Shadbala | Full 6-fold Shadbala from Ch.27 | **Incomplete** |
| House evaluation | 23 workbook rules from Ch.11 | Full methodology from Ch.11 text | **Unverified** |
| Yogas detected | ~35 of 300+ | Full yoga set from Ch.34-42 | **Missing 265+** |
| Karaka assessment | Dynamic karaka primitive | Full karaka system from Ch.32-33 | **Incomplete** |
| Avasthas | Not implemented | Full avastha system from Ch.45 | **Missing entirely** |
| Dasha effects | Computation partial, effects = 0 | Full effects from Ch.47-48, 52-60 | **Missing entirely** |
| Ashtakavarga | SAV only | Full Prastarashtakavarga from Ch.65 | **Missing detail** |
| Transit system | Not implemented | Full system from Ch.70-74 | **Missing entirely** |

---

## Estimated Encoding Effort

| Tier | Chapters | Est. Sessions | Est. Rules/Components |
|------|----------|---------------|----------------------|
| Tier 0 | Ch.3, 11, 26, 27 | 8-12 | ~50 computational components |
| Tier 1 | Ch.32, 34, 39, 45, 46-47 | 10-15 | ~200 rules + computational |
| Tier 2 | Ch.9-10, 33, 35-38, 41-44, 48, 52-60, 64-66 | 25-35 | ~800 rules |
| Tier 3 | Ch.4-8, 28, 40, 49-50, 67-74 | 15-20 | ~300 rules + computational |
| Tier 4 | Ch.1-2, 51, 61-63, 75-97 | 20-30 | ~400 rules + computational |
| **Total** | **97 chapters** | **~80-110 sessions** | **~1,750 rules + components** |

This aligns with v4's estimate of 850+ sessions through full maturity, with corpus encoding being ~80-110 of those.
