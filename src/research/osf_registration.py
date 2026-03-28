"""
src/research/osf_registration.py — OSF Pre-Registration Schema (S201)

Provides machine-readable pre-registration schema for empirical analyses.
Every SHAP analysis or statistical inference must be filed on OSF BEFORE
execution using an OSFRegistration record (GUARDRAIL G22).

The JSON output from to_json() is the canonical filing document.

Public API
----------
  HypothesisSpec    — one hypothesis in a filing
  CVStrategy        — cross-validation plan
  OSFRegistration   — complete pre-registration record

Usage
-----
  reg = OSFRegistration(study_id="OB-3", ...)
  reg.to_json()  # → file on OSF, store in docs/research/
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Literal


@dataclass
class HypothesisSpec:
    """One testable hypothesis in a pre-registration."""
    hypothesis_id: str          # e.g. "H1", "H2"
    description: str            # plain-English statement of the hypothesis
    type: Literal["primary", "secondary", "exploratory"]
    feature_set: list[str]      # feature names that are tested
    metric: str = "brier_score_improvement"
    notes: str = ""


@dataclass
class CVStrategy:
    """Cross-validation strategy specification."""
    train_cutoff_year: int      # last year (inclusive) in training set
    test_from_year: int         # first year in held-out test set
    description: str
    stratify_by: list[str] = field(default_factory=list)  # e.g. ["outcome_domain"]


@dataclass
class OSFRegistration:
    """
    Complete OSF pre-registration record for one study.

    G22 compliance: instantiate and call to_json() to produce the filing.
    Store the JSON in docs/research/ before running any analysis.

    Fields
    ------
    study_id            Short identifier, e.g. "OB-3"
    title               Full study title
    hypotheses          List of HypothesisSpec (at least one primary)
    cv_strategy         Cross-validation plan
    significance_threshold  Alpha level (typically 0.05)
    correction_method   Multiple-comparison correction, e.g. "BH-FDR"
    minimum_sample      Stopping rule: do not analyse until this many
                        confirmed training events are available
    stopping_rule       Plain-language stopping rule description
    feature_definitions Dict mapping feature name → calculation description
    planned_analyses    List of analysis names in execution order
    filed_date          ISO date when filed on OSF (None = draft)
    osf_url             OSF registration URL (None until filed)
    """
    study_id: str
    title: str
    hypotheses: list[HypothesisSpec]
    cv_strategy: CVStrategy
    significance_threshold: float
    correction_method: str
    minimum_sample: int
    stopping_rule: str = (
        "No analysis is run before minimum_sample confirmed training events exist, "
        "regardless of project schedule."
    )
    feature_definitions: dict[str, str] = field(default_factory=dict)
    planned_analyses: list[str] = field(default_factory=list)
    filed_date: str | None = None
    osf_url: str | None = None
    schema_version: str = "1.0"

    def to_dict(self) -> dict:
        """Return plain dict suitable for JSON serialization."""
        d = asdict(self)
        return d

    def to_json(self, indent: int = 2) -> str:
        """Return JSON string of the pre-registration record."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
