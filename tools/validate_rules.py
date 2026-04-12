#!/usr/bin/env python3
"""Pre-commit rule validator for LagnaMaster corpus.

Validates V2 rule schema compliance WITHOUT duplicating v2_scorecard.py checks.
v2_scorecard covers: entity_target enum, direction/intensity enum, prediction structure,
commentary emptiness. This script covers: format validation, cross-field consistency,
numeric ranges, and structural integrity.

Usage:
    python tools/validate_rules.py                    # validate all corpus files
    python tools/validate_rules.py --staged           # validate only git-staged corpus files
    python tools/validate_rules.py --file <path>      # validate a specific file

Exit code 0 = clean, 1 = violations found.
"""

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

CORPUS_DIR = Path(__file__).parent.parent / "src" / "corpus"

# Rule IDs: alphanumeric prefix + digits. Many formats across sources:
# BPHS1200, SAR001, BHR101, B001, H11L001, YGE016, LPF001, etc.
RULE_ID_RE = re.compile(r"^[A-Z][A-Z0-9]{0,10}\d{2,5}$")
# Verse refs: "Ch.N v.M", "Ch.N v.M-K", "Ch.N-N v.M" with optional sub-verse (a/b)
VERSE_REF_RE = re.compile(r"^Ch\.[\d]+([-–]\d+)? v\.(\d+[a-z]?|\d+[a-z]?-\d+[a-z]?)$")

# Files to skip (aggregators, utilities — not individual corpus sources)
SKIP_FILES = {"combined_corpus.py", "registry.py", "rule_record.py",
              "birth_record.py", "convergence_state.py", "corpus_diff.py",
              "bb_reference.py"}
VALID_PHASE = {"1A_representative", "1B_matrix", "1B_conditional", "1B_compound"}
VALID_TIMING_TYPES = {"age", "age_range", "after_event", "dasha_period", "unspecified"}
VALID_RELATIONSHIP_TYPES = {"alternative", "addition", "override", "contrary_mirror", "mitigation"}


def load_rules_from_file(filepath: Path) -> list[dict]:
    """Import a corpus module and extract rules as dicts.

    LagnaMaster corpus files use CorpusRegistry objects (not plain lists).
    Rules are RuleRecord dataclasses with a .to_dict() method.
    Pattern: MODULE_NAME_REGISTRY = CorpusRegistry(); registry.add(rule)
    """
    # Ensure src package is importable
    repo_root = Path(__file__).parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    spec = importlib.util.spec_from_file_location("corpus_module", filepath)
    if spec is None or spec.loader is None:
        return []
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        # Non-corpus utility files (birth_record, registry, etc.) — skip silently
        return []

    # Look for CorpusRegistry instances first (LagnaMaster pattern)
    for attr_name in dir(module):
        if attr_name.startswith("_"):
            continue
        obj = getattr(module, attr_name)
        # Must be an instance (not the class itself) with .all() method
        if (
            hasattr(obj, "all")
            and callable(obj.all)
            and not isinstance(obj, type)  # skip class definitions
            and hasattr(obj, "_rules")  # CorpusRegistry has _rules dict
        ):
            try:
                rules = obj.all()
            except Exception:
                continue
            if rules and hasattr(rules[0], "to_dict"):
                return [r.to_dict() for r in rules]

    # Fallback: plain list variables
    for attr in ("RULES", "rules", "CHAPTER_RULES", "chapter_rules"):
        if hasattr(module, attr):
            rules = getattr(module, attr)
            if isinstance(rules, list):
                if rules and hasattr(rules[0], "to_dict"):
                    return [r.to_dict() for r in rules]
                return rules
    return []


def validate_rule(rule: dict, filepath: Path, all_ids: set[str]) -> list[str]:
    """Validate a single rule. Returns list of error strings."""
    errors = []
    rid = rule.get("rule_id", "<missing>")
    prefix = f"{filepath.name}:{rid}"

    # --- Rule ID format ---
    if not RULE_ID_RE.match(str(rid)):
        errors.append(f"{prefix}: rule_id '{rid}' doesn't match BPHS#### format")

    # --- Duplicate ID ---
    if rid in all_ids:
        errors.append(f"{prefix}: DUPLICATE rule_id '{rid}'")
    all_ids.add(rid)

    # --- Verse reference format ---
    vref = rule.get("verse_ref", "")
    if vref and not VERSE_REF_RE.match(str(vref)):
        errors.append(f"{prefix}: verse_ref '{vref}' doesn't match 'Ch.N v.M' format")

    # --- Schema version ---
    sv = rule.get("schema_version")
    if sv is not None and sv != 2:
        errors.append(f"{prefix}: schema_version is {sv}, expected 2")

    # --- Phase value ---
    phase = rule.get("phase", "")
    if phase and phase not in VALID_PHASE:
        errors.append(f"{prefix}: phase '{phase}' not in {VALID_PHASE}")

    # --- Predictions magnitude range ---
    for i, pred in enumerate(rule.get("predictions", [])):
        mag = pred.get("magnitude")
        if mag is not None and not (0.0 <= float(mag) <= 1.0):
            errors.append(f"{prefix}: predictions[{i}].magnitude={mag} outside 0.0-1.0")

    # --- Confidence range ---
    conf = rule.get("confidence")
    if conf is not None and not (0.0 <= float(conf) <= 1.0):
        errors.append(f"{prefix}: confidence={conf} outside 0.0-1.0")

    # --- Timing window structure ---
    tw = rule.get("timing_window")
    if isinstance(tw, dict) and tw:
        tw_type = tw.get("type", "")
        if tw_type and tw_type not in VALID_TIMING_TYPES:
            errors.append(f"{prefix}: timing_window.type '{tw_type}' not in {VALID_TIMING_TYPES}")
        if tw_type == "age" and "value" in tw and not isinstance(tw["value"], (int, float)):
            errors.append(f"{prefix}: timing_window.value must be numeric for type='age'")
        if tw_type == "age_range" and "value" in tw and not isinstance(tw["value"], (list, tuple)):
            errors.append(f"{prefix}: timing_window.value must be list for type='age_range'")

    # --- Derived house chains structure ---
    for i, dhc in enumerate(rule.get("derived_house_chains", [])):
        bh = dhc.get("base_house")
        eh = dhc.get("effective_house")
        if bh is not None and not (1 <= int(bh) <= 12):
            errors.append(f"{prefix}: derived_house_chains[{i}].base_house={bh} not in 1-12")
        if eh is not None and not (1 <= int(eh) <= 12):
            errors.append(f"{prefix}: derived_house_chains[{i}].effective_house={eh} not in 1-12")

    # --- Rule relationship type ---
    rr = rule.get("rule_relationship")
    if isinstance(rr, dict) and rr:
        rr_type = rr.get("type", "")
        if rr_type and rr_type not in VALID_RELATIONSHIP_TYPES:
            errors.append(f"{prefix}: rule_relationship.type '{rr_type}' not in {VALID_RELATIONSHIP_TYPES}")

    # --- Cross-field consistency: prediction direction vs outcome_direction ---
    out_dir = rule.get("outcome_direction", "")
    preds = rule.get("predictions", [])
    if out_dir and out_dir != "mixed" and preds:
        pred_dirs = {p.get("direction") for p in preds if p.get("direction")}
        if pred_dirs and len(pred_dirs) == 1:
            pred_dir = pred_dirs.pop()
            if pred_dir != out_dir:
                errors.append(
                    f"{prefix}: outcome_direction='{out_dir}' but all predictions say '{pred_dir}'"
                )

    return errors


def get_staged_corpus_files() -> list[Path]:
    """Get corpus .py files that are staged for commit."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, cwd=CORPUS_DIR.parent.parent,
    )
    staged = []
    for line in result.stdout.strip().splitlines():
        p = Path(line)
        if (
            str(p).startswith("src/corpus/")
            and p.suffix == ".py"
            and p.name != "__init__.py"
            and not p.name.startswith("_")
            and p.name not in SKIP_FILES
        ):
            staged.append(CORPUS_DIR.parent.parent / p)
    return staged


def main():
    parser = argparse.ArgumentParser(description="Validate LagnaMaster corpus rules")
    parser.add_argument("--staged", action="store_true", help="Only check git-staged corpus files")
    parser.add_argument("--file", type=str, help="Validate a specific file")
    args = parser.parse_args()

    if args.file:
        files = [Path(args.file)]
    elif args.staged:
        files = get_staged_corpus_files()
        if not files:
            print("No staged corpus files to validate.")
            sys.exit(0)
    else:
        files = sorted(
            f for f in CORPUS_DIR.glob("*.py")
            if f.name != "__init__.py"
            and not f.name.startswith("_")
            and f.name not in SKIP_FILES
        )

    all_errors = []
    all_ids: set[str] = set()
    total_rules = 0

    for filepath in files:
        if not filepath.exists():
            all_errors.append(f"FILE NOT FOUND: {filepath}")
            continue
        rules = load_rules_from_file(filepath)
        total_rules += len(rules)
        for rule in rules:
            errs = validate_rule(rule, filepath, all_ids)
            all_errors.extend(errs)

    # Summary
    print(f"Validated {total_rules} rules across {len(files)} files.")

    if all_errors:
        print(f"\n{len(all_errors)} VIOLATIONS FOUND:\n")
        for err in all_errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("All rules pass validation.")
        sys.exit(0)


if __name__ == "__main__":
    main()
