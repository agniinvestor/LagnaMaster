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
  Rule execution scope: edge queries auto-filter to rule's declared school
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
edges: [typed edge instances per schema below]
schema_version: str
conventions_version: str
```
Canonical representation. All downstream layers query this.

### Layer 4: Feature Access
**Graph-derived computation only.** Feature access computes derived values (Shadbala, dignity scores, avastha effects) but ALL inputs must come from graph edges — never from raw chart data. Input is the `VargaGraphSet` (D1 + requested divisional graphs), not a single graph. Saptavargaja Bala explicitly requires 7 varga graphs. Functional malefic classification requires lagna context + LORDS_HOUSE edges. This is the defined computation layer — not "hidden" computation, but the designed aggregation point for multi-graph, multi-lagna derived values. Existing domain taxonomy (`outcome_domains`) and concordance infrastructure (`concordance_count`, `concordance_texts`) on V2 rules are preserved and used by the aggregation layer.

### Layer 5 → Layer 6: `RuleResult`
```
rule_id, source_text, chapter, verse, school
matched_pattern:
  nodes: list[NodeRef]     # which nodes participated
  edges: list[EdgeRef]     # which edges matched
  bindings: dict[str, Any] # variable bindings (e.g., planet=Jupiter, house=4)
prediction: {domain, direction, intensity, entity_target}
confidence: float
lagna: str                    # which lagna context produced this result (natal/chandra/surya/etc.)
context:
  graph_schema_version: str
  conventions_version: str    # which conventions produced the graph this rule queried
  computation_school: str     # which school's edges were available
trace: {edges_queried, conditions_checked, why_fired, convention_dependencies}
grouping_key: str             # for aggregation: "H4" (house-specific) or "Jupiter-Moon" (relational)
```
Provenance-complete. Every result traces to source, graph pattern, AND reasoning.

## Graph Schema

### Node Types
- `PlanetNode`: name, longitude, latitude, speed, is_natural_malefic (computed at construction via chart-aware classification — Moon phase, Mercury conjunction)
- `HouseNode`: number (1-12), sign, cusp_longitude
- `SignNode`: index (0-11), name, lord

### Edge Tiers
Edges are organized into tiers based on their derivation level. Higher tiers depend on lower tiers. This ordering governs construction sequence and recomputation.

**Tier 1: Structural (from Layer 1-2, no computation)**
These are direct facts from astronomy + conventions.

| Edge Type | Source → Target | Schema | School-Specific? |
|-----------|----------------|--------|-----------------|
| `IN_SIGN` | Planet → Sign | — | No |
| `IN_HOUSE` | Planet → House | — | Convention-dependent |
| `LORDS` | Planet → Sign | — | No |
| `LORDS_HOUSE` | Planet → House | — | No |

**Tier 2: Derived (computed from Tier 1, deterministic)**
These require position-based computation.

| Edge Type | Source → Target | Schema | Depends On | School-Specific? |
|-----------|----------------|--------|-----------|-----------------|
| `ASPECTS` | Planet → Planet/House | `{strength_virupas: float, aspect_type: str}` | positions | **Yes** (Parashari graha / Jaimini rasi) |
| `CONJUNCT` | Planet → Planet | `{orb_degrees: float}` | positions | No |
| `IN_KENDRA_FROM` | Planet → Planet | `{houses_apart: int, method: str}` | `IN_HOUSE` | **Yes** (house-based=Parashari, sign-based=Jaimini) |
| `IN_TRIKONA_FROM` | Planet → Planet | `{houses_apart: int, method: str}` | `IN_HOUSE` | **Yes** (same as above) |
| `COMBUSTION` | Planet → Sun | `{orb_degrees: float, is_cazimi: bool}` | positions | Partially (orbs vary) |
| `FRIENDSHIP` | Planet → Planet | `{naisargika: str, tatkalik: str, compound: str}` | `IN_SIGN` (for tatkalik) | Partially |

**Tier 3: Interpretive-Factual (computed from Tier 1-2, factual classification only)**
These classify state but do NOT evaluate or score.

| Edge Type | Source → Target | Schema | Depends On | School-Specific? |
|-----------|----------------|--------|-----------|-----------------|
| `DIGNITY` | Planet → — (self-attribute) | `{level: str}` | `IN_SIGN`, conventions | Partially (MT ranges) |
| `AVASTHA` | Planet → — (self-attribute) | `{system: str, state: str}` | `IN_SIGN`, positions | Partially (Baaladi = positional, Lajjitadi = associational) |

**NOT in graph (moved to Feature Access Layer 4):**
- `STRENGTH` (Shadbala, KP strength) — school-dependent evaluation, not a relationship
- Dignity SCORE — the classification (exalted/debilitated) is factual, the numeric score is evaluative
- Avastha EFFECT multiplier — the state (Yuva/Mrita) is factual, the effect (1.0/0.0) is evaluative
- Any computation that answers "how strong" rather than "what is"

**The graph answers: "what is the state?" The Feature Layer answers: "how strong/weak is it?"**

**Yogas are NOT graph edges.** Yoga detection belongs to the Rule Engine (Layer 5) as pattern matching over the graph.

**New edge types must justify why they cannot be an attribute of an existing edge type.** This prevents edge explosion.

### Edge Direction Semantics (formal)
Every directed edge `(A)--[TYPE]-->(B)` has a fixed reading:
- `IN_SIGN(Planet, Sign)`: "Planet occupies Sign"
- `IN_HOUSE(Planet, House)`: "Planet occupies House"
- `LORDS(Planet, Sign)`: "Planet rules Sign"
- `LORDS_HOUSE(Planet, House)`: "Planet rules House"
- `ASPECTS(A, B)`: "A casts aspect on B" (A is aspector, B is aspected)
- `CONJUNCT(A, B)`: "A is conjunct B" (symmetric — both edges created)
- `IN_KENDRA_FROM(A, B)`: "A is in kendra from B" ⇔ `(house(A) - house(B)) % 12 ∈ {0, 3, 6, 9}`
- `IN_TRIKONA_FROM(A, B)`: "A is in trikona from B" ⇔ `(house(A) - house(B)) % 12 ∈ {0, 4, 8}`
- `FRIENDSHIP(A, B)`: "A's relationship toward B" (asymmetric — A→B may differ from B→A)
- `COMBUSTION(Planet, Sun)`: "Planet is combust by Sun"

Direction is **never implicit**. Flipping source/target changes the meaning. Enforced by typed constructors that accept (source_type, target_type).

### Edge Dependency Graph
```
Tier 1 (structural):
  IN_SIGN ← positions + conventions
  IN_HOUSE ← positions + conventions
  LORDS ← sign data
  LORDS_HOUSE ← LORDS + IN_HOUSE

Tier 2 (derived):
  ASPECTS ← positions (+ school for method)
  CONJUNCT ← positions
  IN_KENDRA_FROM ← IN_HOUSE (if method=house-based) OR IN_SIGN (if method=sign-based)
  IN_TRIKONA_FROM ← IN_HOUSE (if method=house-based) OR IN_SIGN (if method=sign-based)
  COMBUSTION ← positions + conventions (orbs)
  FRIENDSHIP ← IN_SIGN (tatkalik) + static tables (naisargika)

Tier 3 (interpretive):
  DIGNITY ← IN_SIGN + conventions (MT ranges)
  AVASTHA ← IN_SIGN + positions + DIGNITY
  STRENGTH ← multiple Tier 1-2 edges + conventions
```
Construction follows tier order. Tier N depends only on Tier <N. **Enforced in code via topological build order** — edge constructors declare their dependencies, graph builder resolves order automatically. No edge can be computed outside this ordering.

New edge types require: (1) tier assignment, (2) dependency declaration, (3) typed schema, (4) justification for why not an attribute of existing edge, (5) explicit addition to this registry.

### Graph Invariants (enforced at construction)
1. Every planet has exactly 1 `IN_SIGN` and 1 `IN_HOUSE` edge
2. Every house has exactly 1 `LORDS_HOUSE` incoming edge
3. Every sign has exactly 1 `LORDS` incoming edge
4. No duplicate edges of same identity tuple `(type, school, method)` between same nodes. This is the canonical edge identity — two edges between the same nodes with different method or school are DISTINCT edges, not duplicates.
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
Saturn aspecting Moon:
  Parashari: (Saturn)--[ASPECTS {school=parashari, strength_virupas=60}]-->(Moon)
  Jaimini:   [no ASPECTS edge exists between Saturn and Moon]
```
Absence of edge IS the position — Jaimini says no aspect exists. Do NOT create zero-strength edges to represent "no relationship." Absence = no opinion/no relationship in that school. Presence = relationship exists with its attributes. Aggregation sees: Parashari fired a rule (aspect exists), Jaimini didn't fire (no edge to match). Silence = no opinion, not disagreement.

### Default School (explicit config, never implicit)
```python
# In config, never hardcoded in computation modules
COMPUTATION_SCHOOL = "parashari"  # affects Layer 3 derived edges
RULE_SCHOOL = "all"               # "all" | "parashari" | "jaimini" | "kp"
AGGREGATION_MODE = "concordance"  # "hierarchy" | "school" | "concordance"
```
BPHS/Parashari is the recommended default. This is declared in config and passed explicitly to graph construction and rule evaluation. No module assumes a school — it receives one.

**Graph neutrality (future-ready):** Graph construction builds edges for ALL registered schools simultaneously. Config determines which edges are QUERIED by the rule engine, not which are BUILT. This allows multi-school comparison without graph reconstruction. Cost: more edges in graph. Benefit: true school-neutral substrate.

### Aggregation Layer (formal definition)

**Hierarchy mode:**
- Rules ranked by `source_text.authority_rank`
- When rules from different texts fire for the same configuration, highest-rank wins
- Ties broken by concordance count

**School mode:**
- Only rules matching `RULE_SCHOOL` are evaluated
- No contradictions possible (scope is filtered)

**Concordance mode (recommended):**
- All rules fire regardless of school
- Results grouped by (grouping_key, domain, direction) — grouping_key is house-number for house-specific rules, planet-pair for relational rules, "global" for chart-wide rules
- Weighted concordance: `score = Σ(text_authority_weight × rule_confidence × agreement_sign)`
- Text authority weights configurable (default: BPHS=1.0, others=0.8)
- Rule confidence from corpus metadata (concordance_count, verse specificity)
- Contradictions surfaced in output with per-text breakdown, not suppressed

**Aggregation invariants:**
- Deterministic: same rules + same graph + same config → same output, always
- No domain computation at aggregation — but statistical/meta operations allowed (normalization, confidence scaling, weighting)
- Every output traces to specific RuleResults which trace to specific graph edges

## Multi-Lagna and Divisional Chart Model

### graph.with_lagna(lagna_type) → DerivedGraph
A derived graph shares Tier 1 structural edges (positions, sign lordships — these don't change with lagna) and recomputes Tier 2+ edges (IN_HOUSE changes, so IN_KENDRA_FROM, IN_TRIKONA_FROM, and all house-dependent edges recompute). Not a view (shared state risk), not a full copy (wasteful). Lagna types: `natal`, `chandra`, `surya`, `bhava`, `hora`, `ghatika`.

### VargaGraphSet
Each divisional chart (D1, D9, D10, etc.) produces a separate ChartGraph with its own IN_SIGN edges. `VargaGraphSet = {varga_number: ChartGraph}`. Layer 4 (Feature Access) takes the full VargaGraphSet as input.

### LORDS_HOUSE school variant
Default: universal Parashari sign-based lordship. KP system adds `LORDS_HOUSE {school=kp}` edges where sub-lord logic changes the effective lord. Most rules use default; KP-specific rules declare `requires: ["lords_kp"]`.

## Execution Sequence (explicit)

```
1. Build AstronomicalChart (Layer 1 — immutable positions)
2. Apply conventions → ConventionedChart (Layer 2)
3. Construct ChartGraph + VargaGraphSet (Layer 3 — all schools, all vargas)
4. For each lagna (natal, chandra, surya...):
   a. Derive lagna-specific graph (recompute Tier 2+ edges)
   b. Compute features from VargaGraphSet + lagna graph (Layer 4)
   c. Evaluate rules against graph + features (Layer 5)
   d. Apply cancellations within this lagna scope (Pass 2)
5. Aggregate across lagnas and schools (Layer 6)
6. Format output (Layer 7)
```
Cancellation in step 4d is scoped to `(lagna, school)` — Neecha Bhanga from D1 natal cannot cancel debilitation rules from Chandra lagna.

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
- **Target: graph construction < 10ms, validated via benchmark suite** (not assumed)
- Benchmark suite runs in CI on every push touching graph construction code

### Debugging & Observability
- Every edge carries: which tier created it, which inputs were used, which school
- Rule trace: which edges were queried, what matched, why rule fired/didn't fire
- `explain(rule_id, chart)` → returns full trace from graph edges to prediction
- "Why did this rule fire?" answerable for any rule in any chart
- **Trace levels:** `minimal` (matched edges only), `standard` (edges + bindings), `full` (all queried edges including non-matches). Default: `minimal`. Full trace opt-in per query to control size.

### Migration Safety Net
- Snapshot comparison: old system vs graph system outputs for full regression suite
- Acceptable deviation: **zero** (correctness, not performance)
- Phase 1 does not ship until snapshot parity achieved
- **Rollback mechanism:** feature flag to switch between old evaluation engine and graph-based engine. Both coexist during migration. Flag removed only after Phase 1 exit criteria are met.
- Comparison mode: run BOTH engines on every test chart during migration, assert identical outputs

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
