"""src/corpus/source_texts.py — Canonical source text registry.

Single source of truth for text names, schools, systems, and translators.
Validates that source and concordance_texts entries use canonical names.
"""
from __future__ import annotations

CANONICAL_SOURCES: dict[str, dict] = {
    "BPHS": {
        "full_name": "Brihat Parasara Hora Shastra",
        "translator": "santhanam",
        "school": "parashari",
        "system": "natal",
        "chapters": 97,
        "min_commentary": 0.40,   # Santhanam has extensive notes
        "min_concordance": 0.25,
    },
    "Saravali": {
        "full_name": "Saravali (Kalyana Varma)",
        "translator": "santhanam",
        "school": "parashari",
        "system": "natal",
        "chapters": 68,
        "min_commentary": 0.30,   # Santhanam notes present but terser
        "min_concordance": 0.20,
    },
    "Phaladeepika": {
        "full_name": "Phaladeepika (Mantreswara)",
        "translator": "gs_kapoor",
        "school": "parashari",
        "system": "natal",
        "chapters": 27,
        "min_commentary": 0.30,
        "min_concordance": 0.25,
    },
    "Brihat Jataka": {
        "full_name": "Brihat Jataka (Varahamihira)",
        "translator": "subrahmanya_sastri",
        "school": "parashari",
        "system": "natal",
        "chapters": 28,
        "min_commentary": 0.20,   # Terse text, fewer translator notes
        "min_concordance": 0.30,
    },
    "UttaraKalamrita": {
        "full_name": "Uttara Kalamrita (Kalidasa)",
        "translator": "ps_sastri",
        "school": "parashari",
        "system": "natal",
        "chapters": 7,
        "min_commentary": 0.20,
        "min_concordance": 0.25,
    },
    "JatakaParijata": {
        "full_name": "Jataka Parijata (Vaidyanatha Dikshita)",
        "translator": "subrahmanya_sastri",
        "school": "parashari",
        "system": "natal",
        "chapters": 30,
        "min_commentary": 0.20,
        "min_concordance": 0.25,
    },
    "SarvarthaChintamani": {
        "full_name": "Sarvartha Chintamani (Venkatesha)",
        "translator": "bs_rao",
        "school": "parashari",
        "system": "natal",
        "min_commentary": 0.20,
        "min_concordance": 0.20,
    },
    "LaghuParashari": {
        "full_name": "Laghu Parashari (Jyotish Ratnakar)",
        "translator": "various",
        "school": "parashari",
        "system": "natal",
        "chapters": 8,
        "min_commentary": 0.15,   # Short text, less commentary
        "min_concordance": 0.20,
    },
    "BhavarthaRatnakara": {
        "full_name": "Bhavartha Ratnakara (Ramanujacharya)",
        "translator": "various",
        "school": "parashari",
        "system": "natal",
        "chapters": 20,
        "min_commentary": 0.15,
        "min_concordance": 0.20,
    },
    "JaiminiSutras": {
        "full_name": "Jaimini Sutras",
        "translator": "sanjay_rath",
        "school": "jaimini",
        "system": "natal",
        "min_commentary": 0.30,
        "min_concordance": 0.15,   # Jaimini has less overlap with Parashari
    },
    "LalKitab": {
        "full_name": "Lal Kitab (1952)",
        "translator": "lk_vashisth",
        "school": "lal_kitab",
        "system": "natal",
        "min_commentary": 0.15,
        "min_concordance": 0.10,   # Unique system, low concordance expected
    },
    "ChandraKalaNadi": {
        "full_name": "Chandra Kala Nadi (Deva Keralam)",
        "translator": "cg_rajan",
        "school": "nadi",
        "system": "natal",
        "min_commentary": 0.15,
        "min_concordance": 0.10,
    },
    "PrasnaMarga": {
        "full_name": "Prasna Marga",
        "translator": "various",
        "school": "parashari",
        "system": "horary",
        "min_commentary": 0.20,
        "min_concordance": 0.15,
    },
    "TajikaNeelakanthi": {
        "full_name": "Tajika Neelakanthi",
        "translator": "various",
        "school": "tajika",
        "system": "varshaphala",
        "min_commentary": 0.20,
        "min_concordance": 0.10,
    },
    "MuhurthaChintamani": {
        "full_name": "Muhurtha Chintamani",
        "translator": "various",
        "school": "parashari",
        "system": "muhurtha",
        "min_commentary": 0.20,
        "min_concordance": 0.10,
    },
}

VALID_SOURCE_NAMES = frozenset(CANONICAL_SOURCES.keys())


def get_source_info(name: str) -> dict | None:
    """Look up canonical info for a source text name."""
    return CANONICAL_SOURCES.get(name)


def validate_source_name(name: str) -> bool:
    """Check if a source name is canonical."""
    return name in VALID_SOURCE_NAMES


def get_expected_system(source: str) -> str | None:
    """Get the expected system for a source text."""
    info = CANONICAL_SOURCES.get(source)
    return info["system"] if info else None


def get_expected_school(source: str) -> str | None:
    """Get the expected school for a source text."""
    info = CANONICAL_SOURCES.get(source)
    return info["school"] if info else None
