"""
tools/download_classical_texts.py — S191

Downloads classical Jyotish texts from archive.org to data/classical_texts/.
These texts form the basis for Phase 1 corpus encoding (S216–S410).

Usage:
    python tools/download_classical_texts.py [--dry-run] [--text BPHS]

IMPORTANT: Human review required for EVERY extracted rule before commit.
See CLASSICAL_CORPUS.md for encoding schema and priority ordering.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "data" / "classical_texts"

# ─────────────────────────────────────────────────────────────────────────────
# TEXTS manifest — archive.org identifiers + expected filename
# Priority ordering follows CLASSICAL_CORPUS.md:
#   1. BPHS — 800+ rules, all three schools (highest Layer I concordance impact)
#   2. Brihat Jataka — 150+ rules, Nabhasa yogas
#   3. Uttara Kalamrita — timing-focused, Layer II Capacity gate
#   4. Jataka Parijata — Avasthas + special rules
# ─────────────────────────────────────────────────────────────────────────────

TEXTS: list[dict] = [
    {
        "id": "BPHS",
        "name": "Brihat Parasara Hora Sastra (BPHS) — Santhanam translation",
        "url": "https://archive.org/download/BrihatParasaraHoraSastra/BrihatParasaraHoraSastra.pdf",
        "filename": "BPHS_Santhanam.pdf",
        "priority": 1,
        "est_rules": 800,
        "phase": "S216",
        "notes": "97 chapters. Ch.36-45 (Yogas) → Ch.16-25 (Dashas) → Ch.26-35 (House results).",
    },
    {
        "id": "BPHS_GCS",
        "name": "Brihat Parasara Hora Sastra — Girish Chand Sharma translation",
        "url": "https://archive.org/download/BPHSGirishChandSharma/BPHS_Girish_Chand_Sharma.pdf",
        "filename": "BPHS_Girish_Chand_Sharma.pdf",
        "priority": 1,
        "est_rules": 800,
        "phase": "S216",
        "notes": "Second translation — cross-reference with Santhanam for disputed verses.",
    },
    {
        "id": "BRIHAT_JATAKA",
        "name": "Brihat Jataka — Varahamihira (V. Subrahmanya Sastri translation)",
        "url": "https://archive.org/download/BrihatJatakaVSubrahmanyaSastri/BrihatJataka.pdf",
        "filename": "Brihat_Jataka_Sastri.pdf",
        "priority": 2,
        "est_rules": 150,
        "phase": "S251",
        "notes": "28 chapters. Ch.12 = Nabhasa Yogas (36 types). Key for yoga expansion.",
    },
    {
        "id": "UTTARA_KALAMRITA",
        "name": "Uttara Kalamrita — Kalidasa (P.S. Sastri translation)",
        "url": "https://archive.org/download/UttaraKalamrita/UttaraKalamrita.pdf",
        "filename": "Uttara_Kalamrita_Sastri.pdf",
        "priority": 2,
        "est_rules": 80,
        "phase": "S251",
        "notes": "7 chapters. Bindu 2 (timing) is highest priority — Layer II Capacity gate.",
    },
    {
        "id": "JATAKA_PARIJATA",
        "name": "Jataka Parijata Vol I+II — Vaidyanatha Dikshita (V. Subrahmanya Sastri)",
        "url": "https://archive.org/download/JatakaParijataVol1/JatakaParijata_Vol1.pdf",
        "filename": "Jataka_Parijata_Vol1_Sastri.pdf",
        "priority": 2,
        "est_rules": 200,
        "phase": "S251",
        "notes": "Vol I+II combined ~200 rules. Avasthas + special lagna rules.",
    },
    {
        "id": "PHALA_DEEPIKA",
        "name": "Phala Deepika — Mantreswara (G.S. Kapoor translation)",
        "url": "https://archive.org/download/PhaladeepikaMantreshwar/Phaladeepika.pdf",
        "filename": "Phala_Deepika_Kapoor.pdf",
        "priority": 3,
        "est_rules": 120,
        "phase": "S251",
        "notes": "Avasthas + Muhurtha. Cross-check with Phaladeepika PVRNR commentary.",
    },
]


# ─────────────────────────────────────────────────────────────────────────────


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def download_text(entry: dict, dry_run: bool = False) -> bool:
    out_path = OUT_DIR / entry["filename"]

    if out_path.exists():
        print(f"  SKIP (exists): {entry['filename']}")
        return True

    print(f"  {'DRY-RUN' if dry_run else 'DOWNLOADING'}: {entry['name']}")
    print(f"    URL: {entry['url']}")
    print(f"    Output: {out_path}")

    if dry_run:
        return True

    try:
        urllib.request.urlretrieve(entry["url"], out_path)
        sha = _sha256(out_path)
        print(f"    SHA256: {sha[:16]}...")
        print(f"    OK: {out_path.name} ({out_path.stat().st_size // 1024} KB)")
        return True
    except Exception as exc:
        print(f"    FAIL: {exc}")
        # Don't leave partial downloads
        if out_path.exists():
            out_path.unlink()
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Show what would be downloaded without fetching")
    parser.add_argument("--text", help="Download only this text ID (e.g. BPHS)")
    parser.add_argument("--list", action="store_true", help="List all texts in manifest")
    args = parser.parse_args(argv)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.list:
        print(f"{'ID':<20} {'Priority':<10} {'Est Rules':<12} {'Phase':<8} Name")
        print("-" * 80)
        for t in sorted(TEXTS, key=lambda x: x["priority"]):
            print(f"{t['id']:<20} {t['priority']:<10} {t['est_rules']:<12} {t['phase']:<8} {t['name'][:50]}")
        return 0

    texts = TEXTS
    if args.text:
        texts = [t for t in TEXTS if t["id"] == args.text]
        if not texts:
            print(f"Unknown text ID: {args.text}. Use --list to see all.")
            return 1

    # Sort by priority
    texts = sorted(texts, key=lambda x: x["priority"])

    print(f"Classical texts download — {len(texts)} item(s)")
    print(f"Output directory: {OUT_DIR}")
    print()

    ok = 0
    fail = 0
    for entry in texts:
        print(f"[{entry['id']}] Priority {entry['priority']} — ~{entry['est_rules']} rules")
        if download_text(entry, dry_run=args.dry_run):
            ok += 1
        else:
            fail += 1

    print()
    print(f"Done: {ok} OK, {fail} failed")

    if fail:
        print("NOTE: Failed downloads often need manual retrieval from archive.org.")
        print("      See CLASSICAL_CORPUS.md for alternative URLs.")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
