"""src/MODULE_REGISTRY.py — Canonical module ownership and layer classification.

Each entry maps a module to:
  - layer: architectural layer (1=data, 2=ephemeris, 3=calculations, 4=corpus, 5=scoring, 6=api/ui)
  - tier: importance (1=canonical source, 2=consumer, 3=utility)
  - canonical_for: list of concepts this module is the single source of truth for
  - verification: how the module's correctness was verified

Layer rules:
  - Layer N must NOT import from Layer N+1 or higher
  - Layer 1 (data) imports nothing from src/
  - Layer 2 (ephemeris) imports only Layer 1
  - Layer 3 (calculations) imports Layers 1-2
  - Layer 4 (corpus) imports Layers 1-3
  - Layer 5 (scoring) imports Layers 1-4
  - Layer 6 (api/ui) imports anything

Tier rules:
  - Tier 1 modules own a concept — no other module may define it
  - Tier 2 modules consume Tier 1 concepts via imports
  - Tier 3 modules are utilities with no canonical ownership
"""

from __future__ import annotations

REGISTRY: dict[str, dict] = {
    # ── Layer 1: Data (canonical constants) ─────────────────────────────
    "src.data.constants": {
        "layer": 1,
        "tier": 1,
        "canonical_for": [
            "sign_lords", "natural_benefics", "natural_malefics",
            "exaltation_signs", "debilitation_signs", "sign_names",
            "kendra_houses", "trikona_houses", "dusthana_houses", "upachaya_houses",
            "gentle_signs", "dig_bala", "sthira_karaka",
            "mooltrikona_signs", "own_signs",
            "seven_planets", "weekday_lords",
            "vimshottari_periods", "naisargika_bala",
            "cardinal_signs", "fixed_signs", "mutable_signs",
            "fire_signs", "earth_signs", "air_signs", "water_signs",
        ],
        "verification": "bphs_pdf",
    },

    # ── Layer 2: Ephemeris ──────────────────────────────────────────────
    "src.ephemeris": {
        "layer": 2,
        "tier": 1,
        "canonical_for": ["planet_positions", "birth_chart", "lagna_computation"],
        "verification": "cross_validated_pyjhora",
    },

    # ── Layer 3: Calculations (canonical primitives) ────────────────────
    "src.calculations.house_lord": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["house_map", "house_classification"],
        "verification": "bphs_pdf",
    },
    "src.calculations.dignity": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["exaltation", "debilitation", "mooltrikona", "own_signs", "dignity_score"],
        "verification": "bphs_pdf",
    },
    "src.calculations.sputa_drishti": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["planetary_aspects", "special_aspects"],
        "verification": "bphs_pdf",
    },
    "src.calculations.panchanga": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["tithi", "nakshatra", "yoga", "karana", "vara", "navamsha_chart"],
        "verification": "bphs_pdf",
    },
    "src.calculations.divisional_charts": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["varga_signs", "vimshopaka_bala", "d60_chart"],
        "verification": "bphs_pdf",
    },
    "src.calculations.varga": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["varga_chart_computation"],
        "verification": "cross_validated_divisional_charts",
    },
    "src.calculations.shadbala": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["shadbala_computation", "sthana_bala", "kala_bala", "drig_bala"],
        "verification": "bphs_pdf",
    },
    "src.calculations.ashtakavarga": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["bav_computation", "sav_computation", "shodhana"],
        "verification": "bphs_pdf",
    },
    "src.calculations.functional_dignity": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["functional_benefic", "functional_malefic", "yogakaraka_classification"],
        "verification": "bphs_pdf",
    },
    "src.calculations.functional_roles": {
        "layer": 3,
        "tier": 2,
        "canonical_for": ["functional_role_computation"],
        "verification": "algorithmic",
    },
    "src.calculations.argala": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["argala_computation", "arudha_pada"],
        "verification": "bphs_pdf",
    },
    "src.calculations.multi_lagna": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["special_lagnas", "all_arudha_padas"],
        "verification": "bphs_pdf",
    },
    "src.calculations.dasha": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["vimshottari_dasha"],
        "verification": "bphs_pdf",
    },
    "src.calculations.yogas": {
        "layer": 3,
        "tier": 1,
        "canonical_for": ["pancha_mahapurusha", "raja_yoga", "dhana_yoga"],
        "verification": "bphs_pdf",
    },
    "src.calculations.rule_firing": {
        "layer": 3,
        "tier": 2,
        "canonical_for": ["condition_evaluation", "rule_engine"],
        "verification": "algorithmic",
    },
    "src.calculations.derived_house": {
        "layer": 3,
        "tier": 2,
        "canonical_for": ["derived_house_resolution"],
        "verification": "algorithmic",
    },

    # ── Layer 4: Corpus ─────────────────────────────────────────────────
    "src.corpus.combined_corpus": {
        "layer": 4,
        "tier": 1,
        "canonical_for": ["rule_corpus", "combined_rules"],
        "verification": "verse_audit",
    },
    "src.corpus.v2_builder": {
        "layer": 4,
        "tier": 2,
        "canonical_for": ["rule_building", "rule_validation"],
        "verification": "algorithmic",
    },
    "src.corpus.taxonomy": {
        "layer": 4,
        "tier": 1,
        "canonical_for": ["condition_taxonomy", "modifier_taxonomy"],
        "verification": "bphs_pdf",
    },

    # ── Layer 5: Scoring ────────────────────────────────────────────────
    "src.scoring": {
        "layer": 5,
        "tier": 1,
        "canonical_for": ["house_scoring", "22_rule_engine"],
        "verification": "cross_validated_workbook",
    },
    "src.calculations.multi_axis_scoring": {
        "layer": 5,
        "tier": 2,
        "canonical_for": ["multi_axis_scoring"],
        "verification": "cross_validated_workbook",
    },

    # ── Layer 6: API/UI ─────────────────────────────────────────────────
    "src.api.main": {
        "layer": 6,
        "tier": 3,
        "canonical_for": [],
        "verification": "integration_test",
    },
    "src.ui.app": {
        "layer": 6,
        "tier": 3,
        "canonical_for": [],
        "verification": "manual_test",
    },
}


def get_layer(module_path: str) -> int:
    """Return the layer for a module, inferring from path if not in registry."""
    if module_path in REGISTRY:
        return REGISTRY[module_path]["layer"]
    # Infer from path prefix
    if module_path.startswith("src.data."):
        return 1
    if module_path == "src.ephemeris":
        return 2
    if module_path.startswith("src.calculations."):
        return 3
    if module_path.startswith("src.corpus."):
        return 4
    if module_path.startswith("src.scoring"):
        return 5
    if module_path.startswith("src.api.") or module_path.startswith("src.ui."):
        return 6
    return 3  # default to calculations layer
