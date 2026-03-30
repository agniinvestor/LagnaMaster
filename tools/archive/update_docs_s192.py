"""
update_docs_s192.py — S192 documentation sync

Marks S192 complete in ROADMAP.md and updates MEMORY.md test count.

Run: python update_docs_s192.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parent


def update_roadmap() -> None:
    path = ROOT / "docs" / "ROADMAP.md"
    original = path.read_text()

    updated = original.replace(
        "| S192 | Python Protocol interfaces — module boundary formalization | — | 🔴 |",
        "| S192 | Python Protocol interfaces — module boundary formalization | — | ✅ |",
    )

    if updated == original:
        print("ROADMAP.md: S192 row not found or already updated")
    else:
        path.write_text(updated)
        print("ROADMAP.md: S192 → ✅")


def update_memory() -> None:
    path = ROOT / "docs" / "MEMORY.md"
    original = path.read_text()

    updated = original.replace("1457 passing", "1484 passing")
    updated = updated.replace(
        "- **Sessions 189–191:** Phase 0 bootstrap — Kala Bala verification, C-18 stress fixtures, VedAstro install, Protocol stubs, ruff G17 rule",
        "- **Sessions 189–191:** Phase 0 bootstrap — Kala Bala verification, C-18 stress fixtures, VedAstro install, Protocol stubs, ruff G17 rule\n- **Session 192:** Protocol adapters — ScoringEngineAdapter, VimshottariDasaAdapter, NullFeedbackService, NullMLService",
    )
    updated = updated.replace("- **Next session:** S192", "- **Next session:** S193")

    if updated == original:
        print("docs/MEMORY.md: already current")
    else:
        path.write_text(updated)
        print("docs/MEMORY.md: updated (1484 tests, Next session S193)")


if __name__ == "__main__":
    update_roadmap()
    update_memory()
    print("\nDone — S192 docs sync complete.")
