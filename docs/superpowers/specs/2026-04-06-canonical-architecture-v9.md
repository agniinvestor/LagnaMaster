# LagnaMaster Canonical Architecture — v9 (Clean Rewrite)

**Date:** 2026-04-06 (S317)
**Status:** Final architecture, pending implementation plan
**Supersedes:** v1-v8 (iterative patches consolidated)

## What LagnaMaster Is

A multi-text Jyotish reasoning engine that evaluates how multiple classical knowledge systems (BPHS, Phaladeepika, Saravali, Brihat Jataka, etc.) interpret the same birth chart. Simultaneously a knowledge base (6,500+ rules), computation engine (Shadbala, aspects, avasthas), and prediction system (scores, yogas, timing).

## Pipeline (6 Layers)

```
Birth Data (date, time, location)
  ↓
[Layer 1] Physical Astronomy — immutable positions from Swiss Ephemeris
  ↓
[Layer 2] Structural Conventions — configurable (house system, ayanamsha, MT ranges, combustion orbs)
  ↓
[Layer 3] Graph Construction — entities + relationships + lazy evaluative attributes
  Tier 1: Structural (positions, signs, houses, lordships)
  Tier 2: Derived (aspects, kendra, combustion, friendship)
  Tier 3: Interpretive (dignity classification, avastha state)
  Tier 4: Evaluative — LAZY (Shadbala components, functional roles, Bhava Bala)
  Per-lagna: Tier 2-4 recomputed from shared positions
  Per-varga: separate graph with different sign placements
  All registered schools built simultaneously (graph-neutral)
  ↓
[Layer 4] Rule Engine — queries complete graph (sole input)
  Phase 1: procedural conditions on graph
  Phase 2: declarative Rule IR (DSL) patterns
  Auto-filtered to rule's declared school
  ↓
[Layer 5] Aggregation — hierarchy / school / concordance modes
  ↓
[Layer 6] Output — layered truth (summary + school breakdown + confidence + citations)
```

## Data Contracts

**Layer 1 → Layer 2:** `AstronomicalChart` — `{planets: {name → (lon, lat, speed, distance)}, jd_ut, location}`

**Layer 2 → Layer 3:** `ConventionedChart` — `{planets: {name → (sign, house, degree, is_rx)}, houses, ayanamsha, conventions: ConventionSet}`

**`ConventionSet`:** `{house_system, ayanamsha_name, ayanamsha_value, mt_ranges, combustion_orbs, exalt_degrees}` — populated from code defaults, overridable via config. Values cite BPHS verses.

**Layer 3 output:** `ChartGraph` — `{nodes, edges (4 tiers), schema_version, conventions_version, evaluation_schema_version, registered_schools}`

**Layer 4 → Layer 5:** `RuleResult` — `{rule_id, source_text, chapter, verse, school, lagna, matched_pattern: {nodes, edges, bindings}, prediction: {domain, direction, intensity, entity_target}, confidence, grouping_key, context: {schema_version, conventions_version, computation_school}, trace}`

## Graph Schema

### Nodes
- `PlanetNode`: name, longitude, latitude, speed, is_natural_malefic (chart-aware: Moon phase, Mercury conjunction)
- `HouseNode`: number (1-12), sign, cusp_longitude
- `SignNode`: index (0-11), name
- `UpagrahaNode`: name, longitude, sign_index (no speed/retrograde — subset of planet attributes). Gets IN_SIGN, IN_HOUSE, receives ASPECTS. No DIGNITY, AVASTHA, FRIENDSHIP.

### Edge Tiers

**Tier 1 — Structural (eager, no computation)**

| Edge | Source → Target | Schema |
|------|----------------|--------|
| `IN_SIGN` | Planet/Upagraha → Sign | — |
| `IN_HOUSE` | Planet/Upagraha → House | — (lagna-dependent) |
| `LORDS` | Planet → Sign | — |
| `LORDS_HOUSE` | Planet → House | — (lagna-dependent) |

**Tier 2 — Derived (eager, computed from Tier 1)**

| Edge | Source → Target | Schema | Depends On | School? |
|------|----------------|--------|-----------|---------|
| `ASPECTS_PLANET` | Planet → Planet | `{strength_virupas, type}` | positions | **Yes** |
| `ASPECTS_HOUSE` | Planet → House | `{strength_virupas, type}` | positions | **Yes** |
| `CONJUNCT` | Planet → Planet | `{orb_degrees}` | positions | No |
| `IN_KENDRA_FROM` | Planet → Planet | `{houses_apart, method}` | IN_HOUSE or IN_SIGN | **Yes** |
| `IN_TRIKONA_FROM` | Planet → Planet | `{houses_apart, method}` | IN_HOUSE or IN_SIGN | **Yes** |
| `COMBUSTION` | Planet → Sun | `{orb_degrees, is_cazimi}` | positions | Partially |
| `FRIENDSHIP` | Planet → Planet | `{naisargika, tatkalik, compound}` | IN_SIGN + static | Partially |

**Tier 3 — Interpretive-Factual (eager, classification only)**

| Edge | Node | Schema | Depends On |
|------|------|--------|-----------|
| `DIGNITY` | Planet (self) | `{level: str}` | IN_SIGN + conventions |
| `AVASTHA` | Planet (self) | `{system: str, state: str}` | IN_SIGN + positions |

**Tier 4 — Evaluative (LAZY, component-level, school-specific)**

Computed on first access per (lagna, school). Memoized within one evaluation. Stores component dataclasses, NOT aggregates.

| Attribute | Node | Schema | Depends On |
|-----------|------|--------|-----------|
| `SHADBALA` | Planet | `ShadbalResult{sthana, dig, kala, chesta, naisargika, drik}` | Tier 1-3 |
| `DIGNITY_SCORE` | Planet | `{score: float}` | DIGNITY |
| `AVASTHA_EFFECT` | Planet | `{baaladi: float, jagradadi: float, combined: float}` | AVASTHA |
| `FUNCTIONAL_ROLE` | Planet | `{is_func_malefic, is_func_benefic, is_yogakaraka}` | LORDS_HOUSE + lagna |
| `BHAVA_BALA` | House | `BhavaBalaResult{bhavadhipati, dig, drishti, specials}` | Planet SHADBALA + Tier 2 |

Layer 4 internal ordering: planet-level Tier 4 first (Shadbala, dignity scores), then house-level (Bhava Bala depends on planet Shadbala).

### Edge Semantics (formal)
- `IN_SIGN(Planet, Sign)`: "Planet occupies Sign"
- `IN_HOUSE(Planet, House)`: "Planet occupies House"
- `LORDS(Planet, Sign)`: "Planet rules Sign"
- `LORDS_HOUSE(Planet, House)`: "Planet rules House"
- `ASPECTS_PLANET(A, B)`: "A casts aspect on B" (directional)
- `ASPECTS_HOUSE(A, House)`: "A casts aspect on House"
- `CONJUNCT(A, B)`: symmetric — both A→B and B→A edges created
- `IN_KENDRA_FROM(A, B)`: "A is in kendra from B" ⇔ `(house(A) - house(B)) % 12 ∈ {0, 3, 6, 9}`
- `FRIENDSHIP(A, B)`: "A's relationship toward B" (asymmetric)

Direction is never implicit. Enforced by typed constructors.

### Edge Identity
Canonical identity tuple: `(type, source, target, school, method)`. Two edges between the same nodes with different school or method are DISTINCT.

### Edge Dependencies
```
Tier 1: IN_SIGN ← positions + conventions
        IN_HOUSE ← positions + conventions + lagna
        LORDS ← sign data (universal)
        LORDS_HOUSE ← LORDS + lagna (school-variant for KP)
Tier 2: ASPECTS ← positions + school
        CONJUNCT ← positions
        IN_KENDRA_FROM ← IN_HOUSE (house-based) OR IN_SIGN (sign-based)
        COMBUSTION ← positions + conventions
        FRIENDSHIP ← IN_SIGN (tatkalik) + static (naisargika)
Tier 3: DIGNITY ← IN_SIGN + conventions
        AVASTHA ← IN_SIGN + positions + DIGNITY
Tier 4: SHADBALA ← Tier 1-3 (lazy)
        FUNCTIONAL_ROLE ← LORDS_HOUSE + lagna (lazy)
        BHAVA_BALA ← SHADBALA + Tier 2 (lazy, depends on planet Tier 4)
```
Tier N depends only on Tier <N. Enforced via topological build order in code.

### Graph Invariants
1. Every planet has exactly 1 IN_SIGN and 1 IN_HOUSE edge (per lagna)
2. Every house has exactly 1 LORDS_HOUSE incoming edge (per lagna)
3. Every sign has exactly 1 LORDS incoming edge
4. No duplicate edges with same identity tuple
5. All edge attributes typed and validated
6. Graph construction is pure — same input + same conventions + same schools → same graph
7. No predictions, rule outputs, or yoga results in the graph

### Multi-Lagna Model
`graph.with_lagna(lagna_type)` → new graph sharing positions + IN_SIGN + LORDS (universal). Recomputes: IN_HOUSE, LORDS_HOUSE, ALL Tier 2-4 (everything house-dependent). Lagna types: natal, chandra, surya, bhava, hora, ghatika.

### Divisional Charts
`VargaGraphSet = {varga_n: ChartGraph}`. Each varga has its own IN_SIGN edges. Default vargas from config: `[1, 2, 3, 7, 9, 12, 30]` (Saptavarga). Optional: `[10, 16, 60]`.

### Graph Query API
```
graph.has_edge(type, source, target, school=None) → bool
graph.edges_from(node, type=None, school=None) → list[Edge]
graph.edges_to(node, type=None, school=None) → list[Edge]
graph.node(name) → Node
graph.follow(node, edge_type, school=None) → Node  # single-hop traversal
graph.tier4(node, lagna, school) → Tier4Attributes  # lazy, memoized
```

## Multi-Text / Multi-School

### Texts as First-Class
`Text: {name, full_title, school, authority_rank}`

### Rules Carry Provenance
`Rule: {source_text, chapter, verse, school, requires: [edge_types], specificity: int, cancelled_by: [tag]}`

Specificity: encoding-time decision (0=principle, 1=house, 2=planet+house, 3=exact config).
Cancellation tags: encoding-time decision. Existing 6,500 rules default to no tags — cancellation bootstraps by tagging rules AS they're migrated/touched. Critical cancellations (Neecha Bhanga) tagged first.

### Contradictions
Absence of edge = school's position (no aspect). NOT a zero-strength edge. Silence = no opinion. Rule engine auto-filters to rule's declared school.

### Configuration
```python
REGISTERED_SCHOOLS = ["parashari", "jaimini", "kp"]  # all with implemented modules
RULE_SCHOOL = "all"                                    # or specific school
AGGREGATION_MODE = "concordance"                       # hierarchy | school | concordance
DEFAULT_VARGAS = [1, 2, 3, 7, 9, 12, 30]
```
All config explicit, never hardcoded in computation modules.

### Aggregation
**Hierarchy:** highest authority_rank wins. Ties broken by concordance.
**School:** only matching school's rules evaluated.
**Concordance:** all rules fire. Grouped by (grouping_key, domain, direction). Score = `Σ(text_authority × rule_confidence × direction)` normalized per text (mean per text, not sum — prevents rule-density flooding). Higher specificity overrides lower within same text.

House score = `Σ(rule_weight × direction × confidence)` per house, preserving existing school weight tables (_WEIGHTS dicts).

Aggregation invariants: deterministic, no domain computation (statistical/meta operations allowed), full traceability.

## Execution Sequence

```
1. Build AstronomicalChart (Layer 1)
2. Apply conventions → ConventionedChart (Layer 2)
3. Build base ChartGraph + VargaGraphSet (Layer 3, Tier 1-3 eager, Tier 4 lazy)
   — all registered schools, all configured vargas
4. For each lagna (natal, chandra, surya...):
   a. Derive lagna graph (shared positions, recomputed Tier 2-4)
   b. Evaluate rules against lagna graph (Layer 4)
      — Tier 4 computes lazily on first query, memoizes
      — rules auto-filtered to declared school
   c. Apply cancellations within (lagna, school) scope
5. Aggregate across lagnas and schools (Layer 5)
6. Format output (Layer 6)
```

## Migration

### Phase 1: Graph-as-Chart
1. NEW files: `src/graph/chart_graph.py`, `src/graph/builders/`, `src/graph/query.py`
2. Existing files UNCHANGED — thin adapters delegate to graph
3. `score_all_axes(chart)` continues working, internally builds graph
4. `evaluate_chart_graph(graph)` exposed alongside for new consumers
5. Rollback: feature flag toggles old vs graph engine. Both run during migration, assert identical outputs.

**Exit criteria:** 100% rules evaluate via graph. Zero duplicated relationship logic. Snapshot parity (zero deviation). 14,740+ tests passing. Graph construction < 10ms (benchmarked, not assumed — validated after session 2 checkpoint).

### Phase 2: Rule IR
1. Declarative DSL for new rules (yogas as pattern templates)
2. New encoding uses IR. Old rules migrate when touched.
3. Physical code restructuring (dignity.py split across layers, avastha modules consolidated)

## Enforcement
- Graph invariants validated at construction (runtime)
- CI: no inline lordship tables, no direct chart.planets in rule evaluation, no unnamed constants, no new edge types without registry
- Import boundaries enforced after Phase 2 restructuring
- `GRAPH_SCHEMA_VERSION`, `CONVENTIONS_VERSION`, `EVALUATION_SCHEMA_VERSION` on every output
- Trace levels: minimal (matched edges) / standard (+ bindings) / full (all queried edges)
- Architecture compliance: new files in src/calculations/ must register in ARCHITECTURE_REGISTRY.md

## Worked Example: "Lord of 5th in 9th gives fortune"

### Chart (purpose-built, NOT a pre-existing fixture)
```
Lagna: Aries (sign 0)
Sun: 250° → Sagittarius (sign 8)
Saturn: 70° → Gemini (sign 2)
Moon: 45° → Taurus (sign 1)
Jupiter: 100° → Cancer (sign 3) — debilitated
```

### Layer 1 → Layer 2
Sun at 250° sidereal. Aries lagna. Whole-sign houses.
House 5 = Leo (sign 4). House 9 = Sagittarius (sign 8).

### Layer 3 — Graph Construction

**Tier 1:**
```
(Sun)--IN_SIGN-->(Sagittarius)
(Sun)--IN_HOUSE-->(House9)
(Sun)--LORDS-->(Leo)
(Sun)--LORDS_HOUSE-->(House5)    ← Sun lords House 5
```

**Tier 2:**
```
(Saturn)--ASPECTS_HOUSE {school=parashari, strength=60}-->(House9)
  [Saturn in House 3, aspects 7th = House 9]
(Saturn)--ASPECTS_PLANET {school=parashari, strength=60}-->(Sun)
  [Sun is in House 9, Saturn aspects it]
(Sun)--IN_KENDRA_FROM {houses_apart=0, method=house-based}-->(Sun)
  [trivial self — excluded by query]
```

**Tier 3:**
```
(Sun)--DIGNITY {level=NEUTRAL}    [Sagittarius is Jupiter's sign, Sun-Jupiter = Friend → Friendly sign... actually neutral by Naisargika]
(Jupiter)--DIGNITY {level=DEBIL}  [Jupiter in Cancer = debilitated... wait, Jupiter is EXALTED in Cancer]
```

Actually let me fix the chart — Jupiter exalted in Cancer, not debilitated. Let me use Jupiter at 280° (Capricorn) for debilitation.

```
Jupiter: 280° → Capricorn (sign 9) — DEBILITATED
Moon: 15° → Aries (sign 0) — in lagna
```

Now Neecha Bhanga check: Moon (lord of Cancer = Jupiter's debil sign) is in Kendra from lagna (House 1 = kendra). NB condition 1 satisfied. If another condition is also met → NBRY.

**Tier 3 (corrected):**
```
(Jupiter)--DIGNITY {level=DEBIL}
(Jupiter)--AVASTHA {system=baaladi, state=Vriddha}  [280° in Capricorn, deg=10° in even sign → reversed: 6-12° = Vriddha]
```

**Tier 4 (lazy — not computed yet):**
Nothing computed until a rule queries it.

### Layer 4 — Rule Evaluation

**Rule R-CH24-5-9:** "Lord of 5th in 9th gives fortune" (BPHS Ch.24 sloka 21)
```
source_text: BPHS, chapter: 24, verse: 21, school: parashari
conditions:
  1. follow(LORDS_HOUSE, House5) → get planet P    [Sun]
  2. has_edge(IN_HOUSE, P, House9)                  [Sun in House 9 ✓]
prediction: {domain=fortune, direction=positive, intensity=medium, entity_target=native}
```

**Step 1:** `graph.follow(House5, LORDS_HOUSE)` → follows LORDS_HOUSE edge TO House5, finds Sun. ✓
**Step 2:** `graph.has_edge(IN_HOUSE, Sun, House9)` → True. ✓
**Rule fires.**

Now a strength-dependent variant: "If lord of 5th is strong in 9th, great fortune."
```
conditions:
  3. graph.tier4(Sun, lagna=natal, school=parashari).shadbala.total > 390
```

**This triggers lazy Tier 4 computation.** Shadbala for Sun computed now (not at graph build time). Returns ShadbalResult with components. Rule checks `total > 390` (Sun's BPHS threshold).

**RuleResult:**
```
rule_id: R-CH24-5-9
source_text: BPHS, chapter: 24, verse: 21
school: parashari
lagna: natal
matched_pattern:
  nodes: [Sun, House5, House9]
  edges: [LORDS_HOUSE(Sun→House5), IN_HOUSE(Sun→House9)]
  bindings: {P=Sun, source_house=5, target_house=9}
prediction: {domain=fortune, direction=positive, intensity=medium}
grouping_key: "H9"
confidence: 0.9
```

### Cancellation check

Jupiter is debilitated. Rule R-DEBIL fires:
```
rule_id: R-DEBIL-JUPITER
prediction: {domain=fortune, direction=negative, entity_target=native}
grouping_key: "H9" (Jupiter lords House 9 from Aries = Sagittarius... wait, Jupiter lords House 9? No — House 9 = Sagittarius, lord = Jupiter. Yes.)
cancelled_by: ["neecha_bhanga"]
```

NB check: Moon (lord of Cancer) in House 1 (kendra from lagna) → NB condition 1. Need ≥2 conditions for NBRY. Check others... Saturn lords Capricorn (debil sign), Saturn is in House 3 (not kendra from lagna). Only 1 NB condition → Neecha Bhanga (not Raja). Debilitation is mitigated but not cancelled.

**Cancellation result:** R-DEBIL-JUPITER tagged `cancelled_by: ["neecha_bhanga"]` but NB doesn't fully cancel (only 1 condition). Rule result KEPT but with attenuated confidence.

Wait — I said cancellation is binary (YAGNI on continuous modulation). So: 1 NB condition = Neecha Bhanga (cancelled, confidence reduced). 2+ NB conditions = NBRY (fully cancelled, rule removed). Let me be precise:

**Cancellation:** 1 NB condition → NEECHA_BHANGA → R-DEBIL-JUPITER confidence reduced by 50%. 2+ conditions → NBRY → R-DEBIL-JUPITER removed entirely. (This matches the existing DignityLevel: NEECHA_BHANGA vs NEECHA_BHANGA_RAJA.)

### Layer 5 — Aggregation (concordance mode)

For House 9 (grouping_key = "H9"):
```
R-CH24-5-9:     +0.9 (fortune, positive, BPHS)
R-DEBIL-JUPITER: -0.45 (fortune, negative, BPHS, NB-attenuated)
```

House 9 score = Σ(rule_weight × direction × confidence) = (1.0 × +1 × 0.9) + (1.0 × -1 × 0.45) = +0.45

### Layer 6 — Output
```
House 9 (Fortune/Religion):
  Score: +0.45 (mildly positive)
  Key factors:
    + Lord of 5th (Sun) in 9th — BPHS Ch.24 v.21
    - Jupiter debilitated (lord of 9th) — partially mitigated by Neecha Bhanga
  Confidence: medium
  School: Parashari
```

### What this example exercises
- ✅ Multi-hop traversal (LORDS_HOUSE → IN_HOUSE)
- ✅ Lazy Tier 4 (Shadbala computed on demand)
- ✅ Cancellation with partial mitigation
- ✅ Aggregation with signed weights
- ✅ Full traceability (every output → edges → nodes → positions)
- ✅ School-scoped evaluation
- ✅ Lagna-specific graph (House 5/9 depend on Aries lagna)
