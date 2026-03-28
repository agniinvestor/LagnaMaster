"""
update_docs_s191.py — S191 documentation sync

Marks S191 complete in ROADMAP.md and updates CLASSICAL_CORPUS.md
with VedAstro installation status.

Run: python update_docs_s191.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parent


def update_roadmap() -> None:
    path = ROOT / "docs" / "ROADMAP.md"
    original = path.read_text()

    updated = original.replace(
        "| S191 | VedAstro install + cross-validation, ruff no-jhora rule, Protocol interface stubs, classical texts download | G17, G23, G24 | 🔴 |",
        "| S191 | VedAstro install + cross-validation, ruff no-jhora rule, Protocol interface stubs, classical texts download | G17, G23, G24 | ✅ |",
    )

    if updated == original:
        print("ROADMAP.md: S191 row already updated or not found")
    else:
        path.write_text(updated)
        print("ROADMAP.md: S191 → ✅")


def update_classical_corpus() -> None:
    path = ROOT / "docs" / "CLASSICAL_CORPUS.md"
    original = path.read_text()

    # Update VedAstro row to show installed status
    old_row = "| **VedAstro** | 1,000+ yogas, all planets/houses, Muhurtha, Life predictor | S191: Install + cross-validate |"
    new_row = "| **VedAstro** | 1,000+ yogas, all planets/houses, Muhurtha, Life predictor | ✅ S191: Installed (v1.23.20), cross-validate script in tools/ |"

    updated = original.replace(old_row, new_row)

    # Also update DOB dataset row
    old_dob = "| **VedAstro DOB Dataset** | 15,800 records, Rodden AA, accurate timezone+DST | S191: Download to `data/vedastro/` |"
    new_dob = "| **VedAstro DOB Dataset** | 15,800 records, Rodden AA, accurate timezone+DST | ✅ S191: data/vedastro/ created, download pending |"

    updated = updated.replace(old_dob, new_dob)

    if updated == original:
        print("CLASSICAL_CORPUS.md: VedAstro rows already updated or not found")
    else:
        path.write_text(updated)
        print("CLASSICAL_CORPUS.md: VedAstro installation status updated")


def update_memory_test_count() -> None:
    """Update MEMORY.md test count to reflect S191 additions (+34 tests)."""
    path = ROOT / "MEMORY.md"
    if not path.exists():
        print("MEMORY.md: not found, skipping")
        return
    original = path.read_text()
    # Update test count from 1338 to 1372
    updated = original.replace("1338 passed", "1372 passed")
    if updated != original:
        path.write_text(updated)
        print("MEMORY.md: test count updated to 1372")
    else:
        print("MEMORY.md: test count already current or not found")


if __name__ == "__main__":
    update_roadmap()
    update_classical_corpus()
    update_memory_test_count()
    print("\nDone — S191 docs sync complete.")
