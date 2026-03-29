"""
src/ml/mlflow_config.py — MLflow Experiment Configuration (S211)

Defines MLflow experiment names, tags, and tracking configuration
for Phase 6 empirical analysis. All experiments are pre-registered
in docs/research/osf_draft_ob3.json before any runs are executed.

GUARDRAIL G22: OSF pre-registration must precede any MLflow run.
Do not create MLflow runs for hypothesis testing without a filed OSF registration.

Public API
----------
  EXPERIMENT_NAMES        Dict of study_id → experiment name
  DEFAULT_TRACKING_URI    Default MLflow tracking server URI
  get_experiment_config   Return config dict for a given study_id
"""

from __future__ import annotations

DEFAULT_TRACKING_URI: str = "mlruns"  # local filesystem; override with env MLFLOW_TRACKING_URI

EXPERIMENT_NAMES: dict[str, str] = {
    "OB-3": "OB-3-CrossSchoolConcordance",
    "OB-3-SHAP": "OB-3-SHAPAnalysis",
    "OB-3-FEATURES": "OB-3-FeatureImportance",
    "EXPLORATORY": "EXPLORATORY-NoInference",  # labeled exploratory per G22
}

# Tags applied to all LagnaMaster MLflow runs
BASE_TAGS: dict[str, str] = {
    "project": "LagnaMaster",
    "guardrail": "G22",
    "osf_required": "true",
}

# Per-experiment configuration
_EXPERIMENT_CONFIGS: dict[str, dict] = {
    "OB-3": {
        "name": EXPERIMENT_NAMES["OB-3"],
        "description": "Primary study: cross-school concordance vs single-school baseline",
        "osf_study_id": "OB-3",
        "osf_draft": "docs/research/osf_draft_ob3.json",
        "cv_train_cutoff": 2009,
        "cv_test_from": 2010,
        "significance_threshold": 0.05,
        "correction_method": "BH-FDR",
        "minimum_sample": 1000,
        "tags": {**BASE_TAGS, "study": "OB-3", "type": "confirmatory"},
    },
    "OB-3-SHAP": {
        "name": EXPERIMENT_NAMES["OB-3-SHAP"],
        "description": "SHAP feature importance analysis (requires OSF filing first)",
        "osf_study_id": "OB-3",
        "osf_draft": "docs/research/osf_draft_ob3.json",
        "tags": {**BASE_TAGS, "study": "OB-3", "type": "shap_analysis",
                 "g22_note": "MUST have filed OSF registration before running"},
    },
    "EXPLORATORY": {
        "name": EXPERIMENT_NAMES["EXPLORATORY"],
        "description": "Exploratory analyses — labeled as non-confirmatory per G22",
        "osf_study_id": None,
        "tags": {**BASE_TAGS, "type": "exploratory",
                 "inference_allowed": "false",
                 "g22_note": "Cannot promote rules to engine without OSF registration"},
    },
}


def get_experiment_config(study_id: str) -> dict:
    """
    Return the MLflow experiment configuration for a given study ID.

    Args:
        study_id: Key in _EXPERIMENT_CONFIGS (e.g. "OB-3")

    Returns:
        Config dict with name, description, tags, and CV parameters.

    Raises:
        KeyError: if study_id is not configured
    """
    if study_id not in _EXPERIMENT_CONFIGS:
        raise KeyError(
            f"Experiment '{study_id}' not configured. "
            f"Known: {sorted(_EXPERIMENT_CONFIGS)}"
        )
    return _EXPERIMENT_CONFIGS[study_id]
