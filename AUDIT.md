# LagnaMaster — Classical Audit

> Completed: March 2026
> Full document: `LagnaMaster_Classical_Audit_v2.docx` (repo root)
> Scope: Every calculation module audited against primary Sanskrit authorities.
> The Excel workbook is retired as a reference. Classical texts are authoritative.

---

## Preamble — The Fundamental Architectural Challenge

The scoring engine assigns fixed decimal weights to heuristic rules and sums them to produce
a house score in `[−10, +10]`. **This design has no precedent in any classical Jyotish text.**
BPHS, Phaladeepika, Saravali describe principles qualitatively and contextually — never as
additive numeric weights.

> *"In Jyotish, principles do not add like algebraic quantities. Context, dasha, and karma
> all modulate."* — BV Raman, How to Judge a Horoscope Vol.1

> *"Mechanical point-scoring is seductive but misleading."*
> — Hart de Fouw & Robert Svoboda, Light on Life Ch.1

**Consequence:** The scoring engine is a useful exploratory heuristic. All output ratings
must be presented as relative estimates, not authoritative classical verdicts.

---

## Severity Legend

| Tag | Meaning |
|-----|---------|
| 🔴 CRIT | Produces demonstrably wrong output vs classical authority |
| 🟠 HIGH | Missing a system practitioners consider mandatory |
| 🟡 MED | Reduces classical depth significantly |
| 🟢 LOW | Advanced, school-specific, or stretch goal |

---

## Critical Issues (Phase 0 — Sessions 101+)

| ID | Sev | Module | Issue | Fix | Source |
|----|-----|--------|-------|-----|--------|
| C-01 | 🔴 | `dignity.py` | MT degree ranges approximate; Mercury MT is only 16°–20° Virgo (4°) | Hard-code exact BPHS ranges for all 7 planets | BPHS Ch.3 v.2–9 |
| C-02 | 🔴 | `dignity.py` | Exaltation is binary EXALT flag; should be Paramotcha degree gradient | Add Paramotcha degrees; `Uchcha = 60×(1−\|deg−param\|/30)` | Phaladeepika Ch.2 v.4–7 |
| C-03 | 🔴 | `dignity.py` | Rahu/Ketu assigned NEUTRAL; wrong under all classical schools | Implement exaltation per BPHS: Rahu=Taurus, Ketu=Scorpio; configurable | BPHS Ch.3 |
| C-04 | 🔴 | `dignity.py` | Only 1 of 6 Neecha Bhanga conditions implemented | Add all 6 as separate booleans; NEECHA_BHANGA_RAJA when ≥2 | BPHS Ch.49 v.12–18; Phaladeepika Ch.6 |
| C-05 | 🔴 | `scoring.py` | WC-halving (0.5×) applied uniformly; has no śhloka basis | Replace with BPHS ¾-strength for Mars/Jupiter/Saturn special aspects only | BPHS Ch.26 v.3–5 |
| C-06 | 🔴 | `vimshottari_dasa.py` | `int(lon/13.333)` — float truncation error at nakshatra boundaries | Use `int(lon*3/40)` — exact integer arithmetic | Swiss Ephem. precision |
| C-07 | 🔴 | `ashtakavarga.py` | Trikona Shodhana reduction missing; raw bindus are meaningless for prediction | Implement before all AV display | PVRNR, Ashtakavarga System Ch.4 |
| C-08 | 🔴 | `ashtakavarga.py` | Ekadhipatya Shodhana reduction missing | Implement dual-lordship reduction | PVRNR, Ashtakavarga System Ch.5 |
| I-A | 🔴 | `scoring.py` | Additive numeric weights are non-classical; no śhloka basis | Label scores as heuristic; do not imply classical authority in UI | BV Raman HJH Vol.1 |

---

## High Priority (Phase 0–1)

| ID | Sev | Module | Issue | Fix | Source |
|----|-----|--------|-------|-----|--------|
| C-09 | 🟠 | `shadbala.py` | 7 of 8 Kala Bala sub-components missing (Vara, Hora, Tribhaga, Abda, Masa, Nathonnata, Ayana) | Add all from birth datetime | BPHS Ch.27 v.30–62 |
| C-10 | 🟠 | `shadbala.py` | Drik Bala = 0 in all charts | Implement aspect-sum across all planet pairs | BPHS Ch.27 v.22–29 |
| C-11 | 🟠 | `dignity.py` | Vargottama not detected (D1 sign = D9 sign) | `is_vargottama(lon)`; +0.75 Shadbala bonus | PVRNR, Vedic Astrology Ch.9 |
| C-12 | 🟠 | `ephemeris.py` | Planetary latitudes available in pyswisseph but discarded | Add `latitude: float` to PlanetPosition | Graha Yuddha requires this |
| C-13 | 🟠 | `ashtakavarga.py` | Sarvashtakavarga uses raw (unreduced) tables | Apply Shodhana reductions before summing | PVRNR, AV System Ch.5 |
| C-14 | 🟠 | `yogas.py` | Kemadruma: only 1 of 3 conditions; 4 cancellation conditions missing | Implement all 3 + 4 cancellations | Phaladeepika Ch.6 v.56–60 |
| C-15 | 🟠 | `yogas.py` | Raj Yoga: conjunction only; Parivartana and mutual aspect forms missing | Add exchange and aspect-based forms | BPHS Ch.36 v.1–15 |
| C-16 | 🟠 | `dignity.py` | Combustion orbs: school differences undocumented | Add COMBUSTION_ORBS_BY_SCHOOL dict | Saravali Ch.3; BV Raman HPA Ch.4 |
| C-17 | 🟠 | `scoring.py` | Score clamped [−10,+10] destroys gradient | Store raw unclamped; display `tanh(raw/8)×10` normalized | — |
| C-18 | 🟠 | `tests/` | Single regression fixture (India 1947) — extreme outlier; many rules untested | Add 8 fixtures: Neecha Bhanga, Graha Yuddha, nakshatra cusp, Parivartana, female chart, high-latitude, year-boundary, celebrity | BV Raman Notable Horoscopes |

---

## Mooltrikona Degree Ranges (BPHS Ch.3 — Must Match Exactly)

| Planet | MT Sign | MT Degrees | Own Sign (Non-MT) |
|--------|---------|------------|-------------------|
| Sun | Leo | 0°–20° | 20°–30° Leo |
| Moon | Taurus | 4°–30° | 0°–3°59' Taurus; also Cancer |
| Mars | Aries | 0°–12° | 12°–30° Aries; also Scorpio |
| Mercury | Virgo | **16°–20°** | 0°–15°59' Virgo; 20°–30° Virgo; also Gemini |
| Jupiter | Sagittarius | 0°–10° | 10°–30° Sagittarius; also Pisces |
| Venus | Libra | 0°–15° | 15°–30° Libra; also Taurus |
| Saturn | Aquarius | 0°–20° | 20°–30° Aquarius; also Capricorn |

**Mercury warning:** MT range is only 4 degrees wide. Any approximation ("first half of Virgo") will be wrong for ~87% of Mercury positions in Virgo.

---

## Paramotcha (Exaltation Peak) Degrees

| Planet | Exaltation Sign | Paramotcha Degree | Debilitation Sign | Neecha Degree |
|--------|----------------|-------------------|-------------------|---------------|
| Sun | Aries | 10° | Libra | 10° |
| Moon | Taurus | 3° | Scorpio | 3° |
| Mars | Capricorn | 28° | Cancer | 28° |
| Mercury | Virgo | 15° | Pisces | 15° |
| Jupiter | Cancer | 5° | Capricorn | 5° |
| Venus | Pisces | 27° | Virgo | 27° |
| Saturn | Libra | 20° | Aries | 20° |

---

## 6 Neecha Bhanga Conditions (BPHS Ch.49)

Currently only condition 1 is implemented:

1. ✅ Lord of debilitation sign in Kendra from Lagna
2. ❌ Lord of debilitation sign in Kendra from Moon
3. ❌ Planet that exalts in the debilitation sign in Kendra from Lagna
4. ❌ Planet that exalts in the debilitation sign in Kendra from Moon
5. ❌ Debilitated planet aspected by its debilitation sign lord
6. ❌ Debilitated planet in Parivartana with the sign lord

When ≥2 conditions are met: **Neecha Bhanga Raja Yoga** (Uttarakalamrita Ch.4) — not simply neutral dignity.

---

## BPHS Aspect Strengths (Ch.26 v.3–5)

| Planet | 7th Aspect | Special Aspects | BPHS Strength | Current |
|--------|-----------|-----------------|---------------|---------|
| All | Full (100%) | — | — | ✅ |
| Mars | Full | 4th and 8th | **75%** | ❌ 100% |
| Jupiter | Full | 5th and 9th | **75%** | ❌ 100% |
| Saturn | Full | 3rd and 10th | **75%** | ❌ 100% |

The WC-halving (50%) applied to rules R03/R07/R10/R14 systematically overstates Mars/Jupiter/Saturn aspects by 33%.

---

## AV Shodhana — Both Steps Required

Per PVRNR, *Ashtakavarga System of Prediction* Ch.4–5:
> *"Raw bindus are meaningless for prediction. The reductions are non-negotiable."*

**Step 1 — Trikona Shodhana:** For each trine group {1,5,9}, {2,6,10}, {3,7,11}, {4,8,12}: find minimum bindu value, subtract from all three.

**Step 2 — Ekadhipatya Shodhana:** For dual-ruled signs (Mars: Aries/Scorpio etc.): reduce lower-bindu sign by higher when planet is in neither of its own signs.

All transit quality scores in the current system are based on unreduced (wrong) bindus.

---

## Retired References

The following are no longer authoritative:

- `Lagna_Master5_clean.xlsx` — prototype; superseded by classical text references from S57
- `LagnaMaster_Audit_v5_PVRNR.docx` — Excel-era audit; superseded by this document
- `LagnaMaster_ProgrammePlan_v1.docx` — original 39-week plan; superseded by PLAN.md

---

## Classical Authority Reference

| Text | Author | Translation | Key Chapters |
|------|--------|-------------|-------------|
| BPHS | Parasara | PVRNR, Sagar Publications (2 vols.) | Ch.3, 6, 26, 27, 32, 36, 49 |
| Phaladeepika | Mantreswara | G.S. Kapoor, Ranjan | Ch.2, 4, 5, 6, 26 |
| Saravali | Kalyanarma | R. Santhanam, Ranjan | Ch.3, 4 |
| Brihat Jataka | Varahamihira | B.S. Rao, Ranjan | Ch.3, 12 |
| Jaimini Sutras | Jaimini | Sanjay Rath, Sagittarius | Adhyaya 1–2 |
| Uttarakalamrita | Kalidasa | P.S. Sastri | Ch.4 |

**Modern:** BV Raman · K.N. Rao · Sanjay Rath · Hart de Fouw & Robert Svoboda · Gayatri Devi Vasudev · P.S. Sastri · Komilla Sutton · Dennis Harness

**Validation software:** Jagannatha Hora 8.0 (free, gold standard) · Kala Vedic Astrology (best Shadbala) · Astro-Vision LifeSign 14 (Panchanga)
