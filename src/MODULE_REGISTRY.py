"""src/MODULE_REGISTRY.py — Module registry for all src/calculations/ modules.

Architecture quality criterion Q5.

Each entry maps a module to its:
  - layer: which pipeline layer (1=astronomy, 2=context, 3=evaluation, 4=convergence, 5=temporal)
  - tier: within Layer 2, which computation tier (1-5 per Q1)
  - purpose: one-sentence description
  - canonical_for: what concept(s) this is the canonical source for
  - line_count: approximate size (flag for review if >500)

New modules MUST be registered before merge.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ModuleEntry:
    path: str
    layer: int
    tier: Optional[int]
    purpose: str
    canonical_for: str = ""


# ---------------------------------------------------------------------------
# Registry — canonical and pipeline modules
# ---------------------------------------------------------------------------

REGISTRY: dict[str, ModuleEntry] = {
    # ── Layer 1: Astronomy ────────────────────────────────────────────────
    "ephemeris": ModuleEntry(
        "src/ephemeris.py", layer=1, tier=None,
        purpose="Swiss Ephemeris computation → BirthChart",
        canonical_for="BirthChart, PlanetPosition",
    ),

    # ── Layer 2: Context (G1) ─────────────────────────────────────────────
    "chart_context": ModuleEntry(
        "src/calculations/chart_context.py", layer=2, tier=None,
        purpose="Build ChartContext with 5-tier derived facts (G1)",
        canonical_for="ChartContext, build_chart_context",
    ),
    "house_lord": ModuleEntry(
        "src/calculations/house_lord.py", layer=2, tier=2,
        purpose="Whole-sign house map: house→sign→lord",
        canonical_for="HouseMap, compute_house_map",
    ),
    "dignity": ModuleEntry(
        "src/calculations/dignity.py", layer=2, tier=4,
        purpose="Dignity, combustion, neecha bhanga, uchcha bala",
        canonical_for="DignityResult, compute_all_dignities",
    ),
    "functional_roles": ModuleEntry(
        "src/calculations/functional_roles.py", layer=2, tier=5,
        purpose="Functional benefic/malefic/yogakaraka classification",
        canonical_for="FunctionalRoles, compute_functional_roles",
    ),
    "functional_dignity": ModuleEntry(
        "src/calculations/functional_dignity.py", layer=2, tier=5,
        purpose="BPHS Ch.34 functional classifications + KNOWN_FUNCTIONAL_MALEFICS",
        canonical_for="compute_functional_classifications, KNOWN_FUNCTIONAL_MALEFICS",
    ),
    "ashtakavarga": ModuleEntry(
        "src/calculations/ashtakavarga.py", layer=2, tier=5,
        purpose="Ashtakavarga: planet AV + Sarvashtakavarga",
        canonical_for="AshtakavargaChart, compute_ashtakavarga",
    ),
    "shadbala": ModuleEntry(
        "src/calculations/shadbala.py", layer=2, tier=5,
        purpose="Six-fold strength: sthana, dig, kala, chesta, naisargika, drik",
        canonical_for="ShadbalResult, compute_all_shadbala",
    ),
    "avastha_v2": ModuleEntry(
        "src/calculations/avastha_v2.py", layer=2, tier=4,
        purpose="Baaladi + Sayanadi avasthas (V2 model)",
        canonical_for="AvasthaReportV2, compute_avasthas_v2",
    ),
    "varga": ModuleEntry(
        "src/calculations/varga.py", layer=2, tier=5,
        purpose="All varga computations: D2-D60",
        canonical_for="VargaChart, compute_varga",
    ),
    "panchadha_maitri": ModuleEntry(
        "src/calculations/panchadha_maitri.py", layer=2, tier=3,
        purpose="Panchadha Maitri (5-fold friendship) matrix",
        canonical_for="PanchadhaMatrix, compute_panchadha_matrix",
    ),
    "sputa_drishti": ModuleEntry(
        "src/calculations/sputa_drishti.py", layer=2, tier=3,
        purpose="Graded aspect strength (Sputa Drishti)",
        canonical_for="sputa_drishti_strength",
    ),
    "vimshottari_dasa": ModuleEntry(
        "src/calculations/vimshottari_dasa.py", layer=2, tier=5,
        purpose="Vimshottari dasha: 9 MD × 9 AD with dates",
        canonical_for="MahaDasha, compute_vimshottari_dasa",
    ),

    # ── Layer 3: Evaluation (G2+G3) ───────────────────────────────────────
    "scoring_rules": ModuleEntry(
        "src/corpus/scoring_rules.py", layer=3, tier=None,
        purpose="26 house-scoring rules as data (G2)",
        canonical_for="ScoringRule, SCORING_RULES, SCHOOL_WEIGHTS",
    ),
    "scoring_rule_eval": ModuleEntry(
        "src/calculations/scoring_rule_eval.py", layer=3, tier=None,
        purpose="Data-driven scoring rule evaluator (G2)",
        canonical_for="evaluate_rule, evaluate_all_scoring_rules",
    ),
    "multi_axis_scoring": ModuleEntry(
        "src/calculations/multi_axis_scoring.py", layer=3, tier=None,
        purpose="House scoring engine: evaluate_house_detailed (delegates to scoring_rule_eval)",
        canonical_for="evaluate_house_detailed, score_axis",
    ),
    "rule_firing": ModuleEntry(
        "src/calculations/rule_firing.py", layer=3, tier=None,
        purpose="Corpus rule evaluation: fire V2 rules against chart",
        canonical_for="evaluate_chart, FiredRule, RuleFiringResult",
    ),
    "unified_engine": ModuleEntry(
        "src/calculations/unified_engine.py", layer=3, tier=None,
        purpose="Unified evaluation: both scoring + corpus → EvalResult (G3)",
        canonical_for="evaluate_all_rules, EvalResult, UnifiedResult",
    ),
    "weight_store": ModuleEntry(
        "src/calculations/weight_store.py", layer=3, tier=None,
        purpose="Versioned weight store with 3 version axes (G4+Q6)",
        canonical_for="WeightStore, WeightEntry, VersionInfo",
    ),

    # ── Layer 4: Convergence (G5) ─────────────────────────────────────────
    "convergence": ModuleEntry(
        "src/calculations/convergence.py", layer=4, tier=None,
        purpose="Multi-signal convergence: independent channel counting (G5)",
        canonical_for="converge, ConvergedPrediction",
    ),

    # ── Layer 5: Temporal (G6) ────────────────────────────────────────────
    "temporal_projection": ModuleEntry(
        "src/calculations/temporal_projection.py", layer=5, tier=None,
        purpose="Temporal probability: 7 timing systems → P(event|year) (G6)",
        canonical_for="time_project, TimedPrediction",
    ),

    # ── Pipeline entry point ──────────────────────────────────────────────
    "pipeline": ModuleEntry(
        "src/pipeline.py", layer=0, tier=None,
        purpose="Full pipeline entry point: chart → context → rules → convergence → timing",
        canonical_for="run_pipeline, PipelineResult",
    ),

    # ── Other canonical modules ───────────────────────────────────────────
    "derived_house": ModuleEntry(
        "src/calculations/derived_house.py", layer=2, tier=2,
        purpose="Derived house arithmetic (bhavat-bhavam)",
        canonical_for="resolve_house",
    ),
    "nabhasa_yogas": ModuleEntry(
        "src/calculations/nabhasa_yogas.py", layer=2, tier=5,
        purpose="32 Nabhasa yogas per BPHS Ch.35",
        canonical_for="detect_nabhasa_yogas",
    ),
    "longevity": ModuleEntry(
        "src/calculations/longevity.py", layer=2, tier=5,
        purpose="Pindayu/Nisargayu/Amsayu longevity computation",
        canonical_for="compute_longevity",
    ),
    "graha_yuddha": ModuleEntry(
        "src/calculations/graha_yuddha.py", layer=2, tier=3,
        purpose="Planetary war detection",
        canonical_for="compute_graha_yuddha",
    ),
    "chara_karaka_config": ModuleEntry(
        "src/calculations/chara_karaka_config.py", layer=2, tier=5,
        purpose="Chara Karaka (7/8 planet ranking)",
        canonical_for="compute_chara_karakas",
    ),
    "yogini_dasha": ModuleEntry(
        "src/calculations/yogini_dasha.py", layer=2, tier=5,
        purpose="Yogini dasha: 8-period cycle from Moon nakshatra",
        canonical_for="compute_yogini_dasha",
    ),
    "chara_dasha": ModuleEntry(
        "src/calculations/chara_dasha.py", layer=2, tier=5,
        purpose="Chara dasha: sign-based Jaimini periods",
        canonical_for="compute_chara_dasha",
    ),
    "gochara": ModuleEntry(
        "src/calculations/gochara.py", layer=2, tier=5,
        purpose="Transit analysis: planet positions relative to natal",
        canonical_for="compute_gochara, GocharaReport",
    ),
    "varshaphala": ModuleEntry(
        "src/calculations/varshaphala.py", layer=2, tier=5,
        purpose="Solar return (Varshaphala) annual chart",
        canonical_for="compute_varshaphala, VarshaphalaResult",
    ),
    "invariants": ModuleEntry(
        "src/invariants.py", layer=2, tier=None,
        purpose="Runtime invariant checker for chart correctness (Q7)",
        canonical_for="check_invariants",
    ),
}


def get_module(name: str) -> ModuleEntry | None:
    return REGISTRY.get(name)


def modules_by_layer(layer: int) -> list[ModuleEntry]:
    return [m for m in REGISTRY.values() if m.layer == layer]
