"""
Core diff engine for cross-validating LagnaMaster vs PyJHora.

Compares normalized outputs field-by-field and produces verdicts.
Classification (systematic vs random) is done in a separate pass
after all charts are diffed.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Verdict:
    field_name: str
    status: str = "unclassified_disagreement"
    lm: object = None
    pjh: object = None
    diff: float | None = None
    field_type: str = ""
    tolerance: float | None = None
    normalized: bool = True
    pattern_id: str | None = None
    note: str | None = None


def _circular_diff(a: float, b: float) -> float:
    """Angular difference on a 0-360 circle."""
    d = abs(a - b) % 360
    return min(d, 360 - d)


def diff_field(
    field_name: str,
    lm_value: object,
    pjh_value: object,
    *,
    field_type: str,
    tolerance: float | None = None,
) -> Verdict:
    """Compare a single field between LM and PyJHora outputs."""
    verdict = Verdict(
        field_name=field_name,
        lm=lm_value,
        pjh=pjh_value,
        field_type=field_type,
        tolerance=tolerance,
    )

    # Handle missing/NaN
    if lm_value is None or pjh_value is None:
        verdict.status = "unclassified_disagreement"
        verdict.note = "missing value"
        return verdict

    if field_type in ("longitude", "degree"):
        try:
            lm_f = float(lm_value)
            pjh_f = float(pjh_value)
        except (TypeError, ValueError):
            verdict.status = "unclassified_disagreement"
            verdict.note = "non-numeric value"
            return verdict

        if math.isnan(lm_f) or math.isnan(pjh_f):
            verdict.status = "unclassified_disagreement"
            verdict.note = "NaN value"
            return verdict

        verdict.diff = _circular_diff(lm_f, pjh_f)
        if verdict.diff <= (tolerance or 0.0):
            verdict.status = "agreement"
        else:
            verdict.status = "unclassified_disagreement"

    elif field_type == "integer":
        if int(lm_value) == int(pjh_value):
            verdict.status = "agreement"
            verdict.diff = 0.0
        else:
            verdict.status = "unclassified_disagreement"
            verdict.diff = float(abs(int(lm_value) - int(pjh_value)))

    elif field_type == "categorical":
        if str(lm_value) == str(pjh_value):
            verdict.status = "agreement"
        else:
            verdict.status = "unclassified_disagreement"

    elif field_type == "dasha_period":
        try:
            verdict.diff = abs(float(lm_value) - float(pjh_value))
        except (TypeError, ValueError):
            verdict.status = "unclassified_disagreement"
            verdict.note = "non-numeric dasha boundary"
            return verdict
        if verdict.diff <= (tolerance or 1.0):
            verdict.status = "agreement"
        else:
            verdict.status = "unclassified_disagreement"

    else:
        if str(lm_value) == str(pjh_value):
            verdict.status = "agreement"
        else:
            verdict.status = "unclassified_disagreement"

    return verdict


def validate_schema(schema: dict[str, dict]) -> None:
    """Enforce schema correctness — prevents silent misconfiguration."""
    for field_name, spec in schema.items():
        if "field_type" not in spec:
            raise ValueError(f"Schema field '{field_name}' missing field_type")
        if spec["field_type"] in ("longitude", "degree") and "tolerance" not in spec:
            raise ValueError(
                f"Schema field '{field_name}' (type={spec['field_type']}) "
                f"requires tolerance"
            )


def diff_charts(
    lm_data: dict,
    pjh_data: dict,
    schema: dict[str, dict],
) -> dict[str, Verdict]:
    """Diff all fields between two chart outputs.

    Args:
        lm_data: Normalized LagnaMaster output (flat dict).
        pjh_data: Normalized PyJHora output (flat dict).
        schema: Field definitions: {field_name: {field_type, tolerance?}}

    Returns:
        Dict of field_name → Verdict.
    """
    validate_schema(schema)
    verdicts = {}
    for field_name, field_def in schema.items():
        lm_val = lm_data.get(field_name)
        pjh_val = pjh_data.get(field_name)
        verdicts[field_name] = diff_field(
            field_name,
            lm_val,
            pjh_val,
            field_type=field_def["field_type"],
            tolerance=field_def.get("tolerance"),
        )
    return verdicts
