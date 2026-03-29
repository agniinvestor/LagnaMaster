"""
src/research/data_license.py — Data Source License Compliance (S203)

Tracks licensing for all external data sources used in LagnaMaster.
The primary external dataset is the Astro-Databank (ADB) — a research
archive with a non-commercial, attribution-required license.

IMPORTANT: ADB data must NEVER be used for commercial purposes.
All ADB-derived analyses must be labeled as research-only.

Public API
----------
  DataSourceLicense     — license metadata for one data source
  KNOWN_SOURCES         — registry of pre-defined sources
  check_source_license  — raises if usage violates license terms
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DataSourceLicense:
    """License metadata for an external data source."""
    source_id: str          # Short ID, e.g. "ADB", "PUBLIC_DOMAIN"
    name: str               # Full name
    license_type: str       # e.g. "CC-BY-NC", "Public Domain", "Proprietary-Research"
    commercial_use_allowed: bool
    attribution_required: bool
    url: str
    notes: str = ""
    contact: str = ""
    allowed_uses: list[str] = field(default_factory=list)


# ── Known data sources ────────────────────────────────────────────────────────

KNOWN_SOURCES: dict[str, DataSourceLicense] = {
    "ADB": DataSourceLicense(
        source_id="ADB",
        name="Astro-Databank (Lois Rodden / Astro.com)",
        license_type="Proprietary-Research",
        commercial_use_allowed=False,
        attribution_required=True,
        url="https://www.astro.com/astro-databank",
        notes=(
            "Non-commercial research use only. All publications must cite the "
            "Astro-Databank. Data must not be redistributed. Birth data from ADB "
            "must be anonymized before any public-facing display."
        ),
        contact="astro-databank@astro.com",
        allowed_uses=["academic_research", "internal_validation", "ml_training_research"],
    ),
    "PUBLIC_DOMAIN": DataSourceLicense(
        source_id="PUBLIC_DOMAIN",
        name="Public Domain / Historical Records",
        license_type="Public Domain",
        commercial_use_allowed=True,
        attribution_required=False,
        url="",
        notes="Verified public domain birth data (historical figures, public records).",
        allowed_uses=["all"],
    ),
    "BPHS_TEXT": DataSourceLicense(
        source_id="BPHS_TEXT",
        name="Brihat Parashara Hora Shastra (classical text)",
        license_type="Public Domain",
        commercial_use_allowed=True,
        attribution_required=True,
        url="",
        notes="Ancient text, public domain. Attribution to original source is good practice.",
        allowed_uses=["all"],
    ),
    "SELF_REPORTED": DataSourceLicense(
        source_id="SELF_REPORTED",
        name="User self-reported birth data",
        license_type="User-Consent",
        commercial_use_allowed=True,
        attribution_required=False,
        url="",
        notes=(
            "User consented at signup (DPDP 2023 / GDPR compliant). "
            "Commercial use only within scope of user consent. "
            "Must satisfy G03 privacy guardrail before any production use."
        ),
        allowed_uses=["product", "research_with_consent"],
    ),
}


def check_source_license(source_id: str, commercial: bool = False) -> DataSourceLicense:
    """
    Validate that the intended use of a data source is license-compliant.

    Args:
        source_id:  Key in KNOWN_SOURCES
        commercial: True if the data will be used in a commercial context

    Returns:
        DataSourceLicense if compliant

    Raises:
        KeyError:        source_id not in KNOWN_SOURCES
        PermissionError: use violates license terms
    """
    if source_id not in KNOWN_SOURCES:
        raise KeyError(
            f"Unknown data source '{source_id}'. "
            f"Known sources: {sorted(KNOWN_SOURCES)}"
        )
    lic = KNOWN_SOURCES[source_id]
    if commercial and not lic.commercial_use_allowed:
        raise PermissionError(
            f"Data source '{source_id}' ({lic.name}) does not permit commercial use. "
            f"License: {lic.license_type}. Contact: {lic.contact}"
        )
    return lic
