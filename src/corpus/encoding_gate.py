"""src/corpus/encoding_gate.py — Pre-encoding gates (closes L009, L012, L013).

Mechanical checks that must pass BEFORE encoding work begins.
These prevent the patterns that caused the most rework in project history.

Usage:
    from src.corpus.encoding_gate import pre_encoding_check, post_batch_audit

    # Before starting a new text or chapter batch:
    pre_encoding_check(
        text="BPHS",
        chapters=[24],
        estimated_slokas=148,
        estimated_rules=130,
        source_pages="pp.189-210",
    )

    # After every 10 encoding sessions:
    post_batch_audit(start_session="S312", end_session="S321")
"""
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, UTC

GATE_LOG = Path("data/encoding_gates.json")


def _load_gate_log() -> list[dict]:
    if GATE_LOG.exists():
        return json.loads(GATE_LOG.read_text())
    return []


def _save_gate_log(entries: list[dict]) -> None:
    GATE_LOG.parent.mkdir(parents=True, exist_ok=True)
    GATE_LOG.write_text(json.dumps(entries, indent=2, default=str))


def pre_encoding_check(
    *,
    text: str,
    chapters: list[int],
    estimated_slokas: int,
    estimated_rules: int,
    source_pages: str,
    density_sample: str = "",
) -> None:
    """L009: Pre-encoding density audit gate.

    Must be called before encoding any new chapter or text batch.
    Records the estimate so it can be compared against actuals.

    Args:
        text: Canonical source text name
        chapters: Chapter numbers to encode
        estimated_slokas: Total predictive slokas (from reading, not TOC)
        estimated_rules: Expected rules (slokas × density factor)
        source_pages: Page range in the source text
        density_sample: How the estimate was derived (e.g., "sampled Ch.24 v.1-10: 1.2 rules/sloka")

    Raises:
        ValueError if estimate seems unreasonable or missing.
    """
    errors = []

    # Validate source text
    try:
        from src.corpus.source_texts import validate_source_name
        if not validate_source_name(text):
            errors.append(f"Text '{text}' not in canonical registry")
    except ImportError:
        pass

    # Validate estimate ratio
    if estimated_slokas > 0:
        ratio = estimated_rules / estimated_slokas
        if ratio < 0.3:
            errors.append(
                f"Estimated ratio {ratio:.1f} rules/sloka is suspiciously low. "
                f"Did you read the text or estimate from TOC? (L009, L016)"
            )
        if ratio > 3.0:
            errors.append(
                f"Estimated ratio {ratio:.1f} rules/sloka is suspiciously high. "
                f"Are you counting sub-claims that should be separate rules?"
            )
    else:
        errors.append("estimated_slokas must be > 0 — count them from the text")

    if not source_pages:
        errors.append("source_pages required — specify the page range you'll read")

    if not density_sample:
        errors.append(
            "density_sample required — describe how you estimated. "
            "E.g., 'sampled Ch.24 v.1-10: 1.2 rules/sloka × 148 slokas'"
        )

    if errors:
        raise ValueError(
            "PRE-ENCODING GATE FAILED:\n" +
            "\n".join(f"  ✗ {e}" for e in errors) +
            "\n\nRead lessons_learned.md L009, L016: Never estimate from TOC."
        )

    # Record the gate pass
    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "text": text,
        "chapters": chapters,
        "estimated_slokas": estimated_slokas,
        "estimated_rules": estimated_rules,
        "source_pages": source_pages,
        "density_sample": density_sample,
        "status": "gate_passed",
    }
    log = _load_gate_log()
    log.append(entry)
    _save_gate_log(log)


def post_batch_audit(
    start_session: str,
    end_session: str,
) -> dict:
    """L013: Intermediate corpus audit gate.

    Must be run after every 10 encoding sessions.
    Compares actual rules produced against estimates from pre_encoding_check.

    Returns audit results dict.
    """
    from src.corpus.combined_corpus import build_corpus
    from src.corpus.corpus_audit import CorpusAudit

    corpus = build_corpus()

    # Filter rules from the session range
    batch_rules = [
        r for r in corpus.all()
        if r.last_modified_session
        and start_session <= r.last_modified_session <= end_session
    ]

    audit = CorpusAudit(corpus)
    report = audit.run()

    result = {
        "session_range": f"{start_session}-{end_session}",
        "rules_produced": len(batch_rules),
        "v2_errors": len(report["v2_errors"]),
        "v2_warnings": len(report["v2_warnings"]),
        "timestamp": datetime.now(UTC).isoformat(),
    }

    if batch_rules:
        with_commentary = sum(1 for r in batch_rules if r.commentary_context)
        with_concordance = sum(1 for r in batch_rules if r.concordance_texts)
        with_timing = sum(1 for r in batch_rules
                         if r.timing_window.get("type") not in ("unspecified", None))
        result["commentary_coverage"] = with_commentary / len(batch_rules)
        result["concordance_coverage"] = with_concordance / len(batch_rules)
        result["timing_coverage"] = with_timing / len(batch_rules)

    # Check against estimates
    log = _load_gate_log()
    for entry in log:
        if entry.get("status") == "gate_passed":
            est = entry.get("estimated_rules", 0)
            if est > 0 and len(batch_rules) > 0:
                actual_ratio = len(batch_rules) / est
                if actual_ratio < 0.5:
                    result["warning"] = (
                        f"Produced {len(batch_rules)} rules vs estimated {est} "
                        f"({actual_ratio:.0%}) — significant underproduction"
                    )

    # Record
    log.append({"type": "batch_audit", **result})
    _save_gate_log(log)

    return result


def session_capacity_check(
    session: str,
    rules_produced: int,
    hours_spent: float = 0,
) -> dict:
    """L012: Session capacity tracking.

    Records rules produced per session. Flags if pace drops below historical average.
    """
    log = _load_gate_log()

    # Calculate historical average from prior entries
    prior = [e for e in log if e.get("type") == "session_capacity"]
    if prior:
        avg_rules = sum(e["rules_produced"] for e in prior) / len(prior)
        if rules_produced < avg_rules * 0.5 and rules_produced > 0:
            return {
                "warning": f"Session {session} produced {rules_produced} rules "
                          f"vs historical avg {avg_rules:.0f} — pace dropped >50%. "
                          f"Check if depth is being maintained (L003).",
                "rules_produced": rules_produced,
                "historical_avg": avg_rules,
            }

    entry = {
        "type": "session_capacity",
        "session": session,
        "rules_produced": rules_produced,
        "hours_spent": hours_spent,
        "timestamp": datetime.now(UTC).isoformat(),
    }
    log.append(entry)
    _save_gate_log(log)

    return {"status": "ok", "rules_produced": rules_produced}
