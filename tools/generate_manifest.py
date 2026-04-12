#!/usr/bin/env python3
"""Generate docs/CORPUS_MANIFEST.json from live corpus data.

Run after encoding sessions to keep the manifest current:
    PYTHONPATH=. .venv/bin/python tools/generate_manifest.py

Output: docs/CORPUS_MANIFEST.json with per-file metadata.
"""

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
CORPUS_DIR = ROOT / "src" / "corpus"
OUTPUT = ROOT / "docs" / "CORPUS_MANIFEST.json"

SKIP_FILES = {
    "__init__.py", "registry.py", "rule_record.py", "birth_record.py",
    "convergence_state.py", "corpus_diff.py", "bb_reference.py",
    "combined_corpus.py",
}


def scan_corpus() -> dict:
    sys.path.insert(0, str(ROOT))

    files = sorted(
        f.name for f in CORPUS_DIR.glob("*.py")
        if f.name not in SKIP_FILES and not f.name.startswith("_")
    )

    manifest_entries = []
    errors = []

    for filename in files:
        mod_path = f"src.corpus.{filename[:-3]}"
        try:
            mod = importlib.import_module(mod_path)
        except Exception as e:
            errors.append({"file": filename, "error": str(e)})
            continue

        # Find CorpusRegistry instance
        rules = []
        for attr_name in dir(mod):
            if attr_name.startswith("_"):
                continue
            obj = getattr(mod, attr_name)
            if (
                hasattr(obj, "all") and hasattr(obj, "_rules")
                and not isinstance(obj, type)
            ):
                try:
                    rules = obj.all()
                except Exception:
                    continue
                if rules:
                    break

        if not rules:
            manifest_entries.append({
                "file": filename,
                "rule_count": 0,
                "source": "",
                "version": "utility",
                "chapters": [],
                "has_v2_schema": False,
            })
            continue

        # Extract metadata
        source = getattr(rules[0], "source", "") if rules else ""
        chapters = sorted({
            getattr(r, "chapter", "") for r in rules
            if getattr(r, "chapter", "")
        })
        has_v2 = any(getattr(r, "schema_version", 0) == 2 for r in rules)
        phase = getattr(rules[0], "phase", "") if rules else ""

        if has_v2:
            version = "1B_V2"
        elif phase and phase.startswith("1A"):
            version = "1A"
        else:
            version = "mixed"

        # Detect entity targets used
        entities = sorted({
            getattr(r, "entity_target", "native") for r in rules
            if getattr(r, "entity_target", "")
        })

        manifest_entries.append({
            "file": filename,
            "rule_count": len(rules),
            "source": source,
            "version": version,
            "chapters": chapters,
            "has_v2_schema": has_v2,
            "entity_targets": entities,
        })

    # Summary
    total_rules = sum(e["rule_count"] for e in manifest_entries)
    v2_rules = sum(
        e["rule_count"] for e in manifest_entries if e["version"] == "1B_V2"
    )
    v1a_rules = sum(
        e["rule_count"] for e in manifest_entries if e["version"] == "1A"
    )
    sources = sorted({
        e["source"] for e in manifest_entries if e["source"]
    })

    manifest = {
        "generated_by": "tools/generate_manifest.py",
        "summary": {
            "total_files": len(manifest_entries),
            "total_rules": total_rules,
            "v2_rules": v2_rules,
            "v1a_rules": v1a_rules,
            "sources": sources,
        },
        "files": manifest_entries,
    }

    if errors:
        manifest["import_errors"] = errors

    return manifest


def main():
    manifest = scan_corpus()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(manifest, f, indent=2)

    s = manifest["summary"]
    print(f"Manifest written to {OUTPUT}")
    print(f"  Files: {s['total_files']}")
    print(f"  Rules: {s['total_rules']} (V2: {s['v2_rules']}, V1A: {s['v1a_rules']})")
    print(f"  Sources: {', '.join(s['sources'])}")


if __name__ == "__main__":
    main()
