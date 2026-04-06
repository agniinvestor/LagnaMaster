# LagnaMaster Canonical Architecture Spec

**Date:** 2026-04-06 (S317)
**Status:** Design approved, pending implementation plan
**Problem:** 300+ sessions of organic growth produced 10 duplication clusters across ~150 files with no formal pipeline, no data contracts, and no layer boundaries. Root cause: no system architecture — only module-level decisions.

## Core Identity

LagnaMaster is a **multi-text Jyotish reasoning engine** that evaluates how multiple classical knowledge systems interpret the same birth chart. It is simultaneously:
- A **knowledge base** (6,500+ encoded rules from BPHS, Phaladeepika, Saravali, etc.)
- A **computation engine** (Shadbala, aspects, avasthas, dignities)
- A **prediction system** (house-level scores, yoga detection, timing)

These three are inseparable layers. None is primary.

## Computation Pipeline

```
Birth Data (date, time, location)
  ↓
[Layer 1] Physical Astronomy (immutable)
  Planet longitudes, speeds, latitudes from Swiss Ephemeris
  ↓
[Layer 2] Structural Conventions (configurable, explicit)
  House system, ayanamsha, MT ranges, combustion orbs, exaltation degrees
  ↓
[Layer 3] Graph Construction (KEY ARCHITECTURAL SHIFT)
  Entities: planets, houses, signs
  Relationships: aspects, lordships, conjunctions, dignities, avasthas
  Multi-school: parallel edges with provenance (Parashari aspect vs Jaimini aspect)
  ↓
[Layer 4] Feature Access (structured view over graph)
  moon.derived.parashari.shadbala — computed from graph relationships
  ↓
[Layer 5] Rule Engine (pattern matching on graph)
  Phase 1: procedural conditions querying graph
  Phase 2: declarative Rule IR (DSL) as pattern templates
  Multi-text: rules carry provenance (source, chapter, verse, school)
  ↓
[Layer 6] Aggregation (mode-dependent)
  Hierarchy: BPHS overrides others for computation
  School-based: user selects Parashari/KP/Jaimini, only that school's rules apply
  Concordance: all texts contribute, weight by agreement count
  ↓
[Layer 7] Output (layered truth)
  Clean summary + school breakdown + confidence + citations
```

## Data Contracts

### Layer 1 → Layer 2: `AstronomicalChart`
```
planets: {name → (longitude, latitude, speed, distance)}
julian_day: float
location: (lat, lon, alt)
```
Immutable. No astrological interpretation.

### Layer 2 → Layer 3: `ConventionedChart`
```
planets: {name → (sign, house, degree_in_sign, is_retrograde)}
houses: {1-12 → sign_index}
ayanamsha: (name, value)
conventions: {mt_ranges, combustion_orbs, exaltation_degrees, ...}
```
Configurable. Explicit about which conventions are applied.

### Layer 3 output: `ChartGraph`
```
nodes: [PlanetNode, HouseNode, SignNode]
edges: [TypedEdge(source, target, type, attributes, school)]
```
Canonical representation. All downstream layers query this.

### Layer 5 → Layer 6: `RuleResult`
```
rule_id, source_text, chapter, verse
matched_pattern: list[Edge]
prediction: {domain, direction, intensity, entity_target}
confidence: float
```
Provenance-complete. Every result traces to a source and a graph pattern.

## Graph Schema

### Node Types
- `PlanetNode`: name, longitude, latitude, speed (Layer 1 data attached)
- `HouseNode`: number (1-12), sign, cusp_longitude
- `SignNode`: index (0-11), name, lord

### Edge Types (Controlled Vocabulary)
| Edge Type | Source → Target | Attributes | School-Specific? |
|-----------|----------------|------------|-----------------|
| `IN_SIGN` | Planet → Sign | — | No |
| `IN_HOUSE` | Planet → House | — | No (convention-dependent) |
| `LORDS` | Planet → Sign | — | No |
| `LORDS_HOUSE` | Planet → House | — | No |
| `ASPECTS` | Planet → Planet/House | strength (virupas), type | **Yes** (Parashari vs Jaimini) |
| `CONJUNCT` | Planet → Planet | orb (degrees) | No |
| `DIGNITY` | Planet → DignityLevel | level, score | Partially (MT ranges vary) |
| `AVASTHA` | Planet → AvasthaState | system, state, effect | **Yes** (Baaladi/Lajjitadi/etc.) |
| `FRIENDSHIP` | Planet → Planet | naisargika, tatkalik, compound | No (naisargika) / Yes (compound) |
| `COMBUSTION` | Planet → Sun | orb, is_cazimi | Partially (orbs vary) |
| `IN_KENDRA_FROM` | Planet → Planet | houses_apart | No |
| `IN_TRIKONA_FROM` | Planet → Planet | houses_apart | No |
| `YOGA_COMPONENT` | Planet → YogaPattern | yoga_name, role | **Yes** (different texts define differently) |

New edge types require explicit addition to this registry.

### Graph Invariants (enforced at construction)
1. Every planet has exactly 1 `IN_SIGN` and 1 `IN_HOUSE` edge
2. Every house has exactly 1 `LORDS_HOUSE` incoming edge
3. Every sign has exactly 1 `LORDS` incoming edge
4. No duplicate edges of same (type + school) between same nodes
5. All edge attributes are typed and validated at construction
6. Graph construction is **pure** — same input always produces same graph
7. No predictions, scores, or rule outputs in the graph — state + relationships only

## Multi-Text / Multi-School

### Texts as First-Class
```
Text:
  name: "BPHS"
  full_title: "Brihat Parasara Hora Sastra (Santhanam)"
  school: "Parashari"
  authority_rank: 1 (for hierarchy mode)
```

### Rules Carry Provenance
```
Rule:
  source_text: "Saravali"
  chapter: 12
  verse: 34
  school: "Parashari"
  requires: ["aspects_parashari", "shadbala"]  # explicit dependencies
```

### Contradictions Are Data
```
Moon in 1st house:
  (Moon)--[ASPECTS {school=parashari, strength=60}]-->(House1)
  (Moon)--[ASPECTS {school=jaimini, strength=0}]-->(House1)
```
Both edges exist simultaneously. Aggregation layer resolves per mode.

### Default School
BPHS/Parashari is the default for computation (Layer 2-3). This is explicit, not hidden. Users can override. Rules from other schools still fire but are tagged with their school for aggregation.

## Migration Strategy (Two Phases)

### Phase 1: Graph-as-Chart (substrate)
1. Build `ChartGraph` construction from `ConventionedChart`
2. Rewrite `rule_firing.py` evaluation to query graph, not raw chart
3. Existing 6,500 rules keep procedural conditions, execute against graph
4. All lookup table duplication eliminated (lordship = graph edge, not inline dict)
5. Performance: graph construction O(n), rule evaluation no recomputation

**Exit Criteria:**
- 100% rules evaluate against graph (zero direct `chart.planets` access in rule evaluation)
- Zero duplicated relationship logic in codebase
- Test parity with pre-graph system (snapshot comparison)
- Graph construction < 10ms per chart
- 14,740+ tests passing

### Phase 2: Rule IR (knowledge layer)
1. Define declarative Rule IR (DSL) for new rules
2. New Tier 1-2 encoding uses IR (yogas as pattern templates)
3. Gradually convert high-value procedural rules when touched
4. Pattern-based yoga detection replaces custom functions
5. Multi-text concordance native in aggregation layer

**Exit Criteria:**
- All new rules (post-Phase 2 start) are declarative IR
- Top 100 most-fired rules converted to IR
- Yoga detection via pattern matching for all encoded yogas

## Enforcement & Invariants

### Graph Invariants (runtime)
- Schema validation on every graph construction
- Reject graphs that violate the 7 invariants above
- Deterministic: same input → same graph → same output, always

### Versioning
```
GRAPH_SCHEMA_VERSION = "v1"
CONVENTIONS_VERSION = "lahiri_v1"
```
Every graph output carries its schema + conventions version. Historical outputs reproducible.

### CI / Pre-commit Controls
- No inline lordship/sign-lord tables (grep check)
- No direct `chart.planets` access in rule evaluation code (after Phase 1)
- No new computation modules outside registered graph layers
- No unnamed magic numbers for astrological constants
- No new edge types without registry addition
- No new avastha/scoring/aspect modules without architecture review

### Performance Bounds
- Graph construction: O(planets × relationships) — no nested recomputation
- Rule evaluation: queries pre-computed graph — no trigger of recomputation
- Memoization on graph edges for repeated queries within same evaluation

### Debugging & Observability
- Every edge carries: which layer created it, which inputs were used
- Rule trace: which edges were queried, what matched, why rule fired/didn't
- "Why did this rule fire?" answerable for any rule in any chart

### Migration Safety Net
- Snapshot comparison: old system vs graph system outputs for regression suite
- Acceptable deviation: zero (correctness, not performance)
- Phase 1 does not ship until snapshot parity achieved

## What This Architecture Prevents

| Previous Problem | How This Prevents It |
|-----------------|---------------------|
| 30 sign lord tables | Lordship = graph edge. One source of truth. |
| 5 avastha modules | Avastha = graph edge attribute. One computation, one edge type. |
| 5 aspect sources | Aspect = graph edge. One construction, school-tagged. |
| Inline malefic checks | `is_malefic` = node attribute query on graph. One computation. |
| Magic numbers | Named constants in conventions layer. Configurable, explicit. |
| Stale import chains | All queries go to graph. No transitive stale copies. |
| v1/v2/v3 chains | One graph, one evaluation engine. Evolution via edge types, not file duplication. |
| Behavioral lessons failing | CI hooks enforce graph-only access. System enforces, not person. |
