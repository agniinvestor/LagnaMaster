# Coverage Map — Laghu Parashari
> **Status: ENCODING NOT STARTED** (target: S264–S266)
> Update status and actual counts as each section is encoded.
> A section is complete when actual count ≥ minimum count.

---

## Text Overview

| Property | Value |
|----------|-------|
| Full name | Laghu Parashari (also: Parashari Light, Jataka Chandrika) |
| Attribution | Devadatta (medieval, commentary on Parashari tradition) |
| Language | Sanskrit (~42 core sutras + commentaries) |
| School | parashari |
| System | natal |
| Phase 1B type | 1B_matrix (Section A, B, C) + 1B_conditional (Section D, E) |
| Priority | HIGHEST — foundational for all Parashari yoga rules |
| Why first | The functional nature table (9×12) is the master lookup for yogakaraka, maraka, and benefic/malefic classification by lagna. All other Parashari rules' weights depend on it. |

---

## Coverage Map

### Section A — Functional Nature Table (9 planets × 12 lagnas = 108 rules)

**What it encodes:** For each of 12 lagnas, for each of 9 planets, what is the
planet's functional status? The Laghu Parashari framework classifies each cell as:
- `yogakaraka`: owns both a kendra AND a trikona simultaneously
- `functional_benefic`: primarily owns trines (5, 9) or lagna (1)
- `kendradhipati_issue`: natural benefic that owns a kendra (loses beneficence per
  Kendradhipati doctrine) — but retains some beneficence
- `functional_malefic`: primarily owns dusthanas (6, 8, 12) or neutral ownership
- `maraka`: owns 2nd or 7th house (death-inflicting potential)
- `neutral`: mixed ownership, no clear benefic or malefic designation
- `badhaka`: obstructing planet (for movable lagnas: 11th lord; fixed: 9th; dual: 7th)

**Minimum rule count:** 108 (one per cell, no exceptions)

**Coverage status:**
| Lagna | Status | Actual Count | Minimum |
|-------|--------|-------------|---------|
| Aries | 🔲 Not started | 0 | 9 |
| Taurus | 🔲 Not started | 0 | 9 |
| Gemini | 🔲 Not started | 0 | 9 |
| Cancer | 🔲 Not started | 0 | 9 |
| Leo | 🔲 Not started | 0 | 9 |
| Virgo | 🔲 Not started | 0 | 9 |
| Libra | 🔲 Not started | 0 | 9 |
| Scorpio | 🔲 Not started | 0 | 9 |
| Sagittarius | 🔲 Not started | 0 | 9 |
| Capricorn | 🔲 Not started | 0 | 9 |
| Aquarius | 🔲 Not started | 0 | 9 |
| Pisces | 🔲 Not started | 0 | 9 |
| **TOTAL** | | **0** | **108** |

**Rule ID prefix:** `LPF001–LPF108` (LP Functional)
**Tags all rules:** `functional_nature`, `lagna_conditional`, `laghu_parashari`
**Phase:** `1B_conditional` (lagna_scope will be populated for each rule)
**Source verse range:** Ch.1–2

---

### Section B — Yogakaraka Designations (12 lagnas × 0–2 yogakarakas = ~15 rules)

**What it encodes:** Which planet(s) are yogakaraka (lord of both kendra AND trikona
simultaneously) for each lagna. Not all lagnas have a yogakaraka — only those where
a single planet owns one kendra and one trikona.

**Yogakaraka by lagna (expected):**
- Aries: Saturn (owns H10 kendra + H11... no — Saturn owns H10+H11; not yogakaraka. Actually: Mars owns H1+H8, Jupiter owns H9+H12... Aries has no yogakaraka from single planet owning kendra+trikona simultaneously. Wait — let me think again. For Aries: H1(kendra+trikona), H4(kendra), H7(kendra), H10(kendra); H1(trikona), H5(trikona), H9(trikona). Mars owns H1(kendra+trikona) — Mars is lagnesh and thus important but the yogakaraka concept usually requires owning SEPARATE kendra+trikona. For Aries, no planet owns both a kendra and a trikona separately — so typically no yogakaraka.)
- Taurus: Saturn (owns H9 trikona + H10 kendra = yogakaraka)
- Gemini: Venus (owns H5 trikona + H12... no. Venus owns H5+H12 for Gemini. H5 is trikona, H12 is not kendra. Actually Saturn owns H9+H10 for Gemini — yogakaraka Saturn)
- Cancer: Mars (owns H5 trikona + H10 kendra = yogakaraka)
- Leo: Mars (owns H4 kendra + H9 trikona = yogakaraka)
- Virgo: Venus (owns H2... no. For Virgo: Venus owns H2+H9. H9 is trikona but H2 is not kendra. Mercury owns H1+H10 — lagnesh + kendra lord. Saturn owns H5+H6 — trikona but also dusthana. So Virgo may also have no single yogakaraka, or Mercury as lagnesh.)
- Libra: Saturn (owns H4 kendra + H5 trikona = yogakaraka)
- Scorpio: No yogakaraka (Jupiter owns H2+H5 — H5 trikona but H2 not kendra)
- Sagittarius: Mars (owns H5 trikona + H12... H5 is trikona; Mars owns H5+H12 for Sag — H12 not kendra. Actually Sun owns H9 for Sag. Venus owns H6+H11. Mercury owns H7+H10 — both kendra but neither trikona. So Sag has no yogakaraka.)
- Capricorn: Venus (owns H5 trikona + H10 kendra = yogakaraka); also Mercury (owns H6+H9 — H9 trikona but H6 dusthana, not yogakaraka)
- Aquarius: Venus (owns H4 kendra + H9 trikona = yogakaraka)
- Pisces: Mars (owns H2+H9 — H9 trikona but H2 not kendra. Actually Mars owns H2+H9 for Pisces. Saturn owns H11+H12. Jupiter owns H1+H10 — both important but H10 is kendra and H1 is trikona+kendra. So Jupiter could be considered for Pisces — owns H1 (kendra+trikona) and H10 (kendra). But by the principle of owning separate kendra+trikona: Jupiter owns H1 (which is both), so that's not "separate" ownership of kendra AND trikona. The rule requires owning one kendra AND one trikona where they are DIFFERENT houses.)

Actually, I'm getting into the actual astrological content here which is better addressed during the encoding session itself, not in the coverage map. The coverage map just needs to know the expected structure.

**Minimum rule count:** 12 (one per lagna, stating whether a yogakaraka exists and if so, which planet)
**Coverage status:** 🔲 Not started (0/12)
**Rule ID prefix:** `LPY001–LPY012` (LP Yogakaraka)
**Tags:** `yogakaraka`, `lagna_conditional`, `laghu_parashari`
**Phase:** `1B_conditional`
**Source verse range:** Ch.1–2

---

### Section C — Kendradhipati Dosha (12 lagnas × ~2 affected planets = ~24 rules)

**What it encodes:** Laghu Parashari's doctrine that natural benefics (Jupiter, Venus,
Mercury, Moon) lose their beneficence when they own kendra houses (1, 4, 7, 10) for
a given lagna. One rule per planet-lagna combination where this applies.

**Minimum rule count:** 20 (some lagnas have 2–3 affected planets; some have 1)
**Coverage status:** 🔲 Not started (0/20)
**Rule ID prefix:** `LPK001–LPK024` (LP Kendradhipati)
**Tags:** `kendradhipati`, `lagna_conditional`, `laghu_parashari`
**Phase:** `1B_conditional`
**Source verse range:** Ch.2–3

---

### Section D — Dasha Results by Lordship Type (~45 rules)

**What it encodes:** During the dasha of a planet that owns houses of type X, the
results of that dasha follow pattern Y. This is lordship-category-based, not
planet-specific. Categories:

- Lagna lord dasha (H1): generally favorable, self-activation
- 2nd lord dasha: wealth and family matters activated
- 3rd lord dasha: siblings, courage, efforts
- 4th lord dasha: mother, property, happiness
- 5th lord dasha: children, intelligence, purva punya
- 6th lord dasha: enemies, disease, debts activated (generally unfavorable)
- 7th lord dasha: marriage, partnership, also maraka potential
- 8th lord dasha: longevity matters, obstacles, sudden events
- 9th lord dasha: fortune, father, dharma — highly favorable
- 10th lord dasha: career, status activated
- 11th lord dasha: gains, desires fulfilled
- 12th lord dasha: expenditure, foreign, losses
- Yogakaraka dasha: exceptional results across multiple domains
- Maraka dasha: health concerns, danger to life

**Minimum rule count:** 42 (one per house-lord-type, plus yogakaraka and maraka)
**Coverage status:** 🔲 Not started (0/42)
**Rule ID prefix:** `LPD001–LPD045` (LP Dasha)
**Tags:** `dasha`, `lordship_type`, `laghu_parashari`
**Phase:** `1B_matrix`
**Source verse range:** Ch.4–5

---

### Section E — Key Antardasha Combinations (~70 rules)

**What it encodes:** When dasha lord A runs sub-period of lord B, the result depends
on the nature of A's and B's lordship. Laghu Parashari states results for key
combinations, particularly:

- Trikona lord + trikona lord antardasha: highly auspicious
- Trikona lord + kendra lord antardasha: raja yoga fructification
- Kendra lord + kendra lord: mixed (kendradhipati issue)
- Dusthana lord as antardasha: obstructs regardless of main dasha
- Maraka planet in antardasha: health concerns
- Yogakaraka dasha + yogakaraka antardasha: exceptional results
- Badhaka planet involvement: specific obstruction patterns

Not all 81 combinations (9×9) are explicitly stated — LP gives the key operative
combinations. Encode all stated; do not invent unstated ones.

**Minimum rule count:** 60
**Coverage status:** 🔲 Not started (0/60)
**Rule ID prefix:** `LPA001–LPA081` (LP Antardasha)
**Tags:** `antardasha`, `dasha_conditional`, `laghu_parashari`
**Phase:** `1B_conditional`
**Source verse range:** Ch.5–6

---

### Section F — Maraka Planets by Lagna (~30 rules)

**What it encodes:** For each lagna, which planets are primary maraka (death-inflicting)
and secondary maraka. The 2nd and 7th lords are primary marakas; Saturn and natural
malefics may serve as secondary marakas in specific configurations.

**Minimum rule count:** 24 (12 lagnas × 2 primary marakas each)
**Coverage status:** 🔲 Not started (0/24)
**Rule ID prefix:** `LPM001–LPM030` (LP Maraka)
**Tags:** `maraka`, `lagna_conditional`, `laghu_parashari`
**Phase:** `1B_conditional`
**Source verse range:** Ch.6–7

---

## Section Totals

| Section | Description | Min Rules | Status |
|---------|-------------|-----------|--------|
| A | Functional Nature Table (9×12) | 108 | 🔲 |
| B | Yogakaraka Designations | 12 | 🔲 |
| C | Kendradhipati Dosha | 20 | 🔲 |
| D | Dasha Results by Lordship | 42 | 🔲 |
| E | Antardasha Combinations | 60 | 🔲 |
| F | Maraka by Lagna | 24 | 🔲 |
| **TOTAL** | | **266** | **0/266** |

*Actual encoding will likely produce 290–320 rules as sub-distinctions within sections
are encoded. The minimum count is the floor; going above it is expected and correct.*

---

## Completion Gate

Laghu Parashari encoding is complete when:
1. All 6 sections are at or above minimum count
2. All rules have `verse_ref` populated (chapter + verse)
3. Section A (108 rules) has `lagna_scope` correctly populated on every rule
4. Concordance check has been run against existing corpus for all rules
5. Verification session (S267 or earlier) confirms compliance

---

## Session Assignment

| Session | Sections | Expected Rules |
|---------|----------|----------------|
| S264 | A (all 12 lagnas) | ~108 |
| S265 | B, C, D | ~74 |
| S266 | E, F + verification of full set | ~84 |
