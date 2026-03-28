"""
src/corpus/birth_record.py — BirthRecord (S208)

Machine-readable birth data for the ML training/test pipeline.
Compatible with Astro-Databank (ADB) schema fields.

IMPORTANT: ADB data requires non-commercial research license.
Check src/research/data_license.py before using ADB records in production.

Public API
----------
  BirthRecord   — single birth data record for ML pipeline
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BirthRecord:
    """
    Birth data record for ML training/validation.

    Fields
    ------
    record_id       Unique identifier (e.g. "ADB-001", "PD-1947-INDIA")
    birth_year      Year of birth (used for CV split)
    birth_month     Month 1-12
    birth_day       Day 1-31
    birth_hour      Decimal hour 0.0-23.999 (local time)
    latitude        Birth latitude in decimal degrees (+N/-S)
    longitude       Birth longitude in decimal degrees (+E/-W)
    data_source     Source ID from data_license.KNOWN_SOURCES
    tz_offset       UTC offset in hours (e.g. 5.5 for IST)
    ayanamsha       Ayanamsha system, default "lahiri"
    name            Optional name or label (anonymized for ADB records)
    gender          Optional gender ('M', 'F', 'NB', '')
    rodden_rating   Astro-Databank Rodden Rating (AA, A, B, C, DD, X, XX)
    confirmed_events  List of confirmed outcome event IDs (Phase 3+)
    notes           Any annotation
    """
    record_id: str
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: float
    latitude: float
    longitude: float
    data_source: str
    tz_offset: float = 0.0
    ayanamsha: str = "lahiri"
    name: str = ""
    gender: str = ""
    rodden_rating: str = ""
    confirmed_events: list[str] = field(default_factory=list)
    notes: str = ""
