"""
Normalization layer for cross-engine comparison.

Applied to both LagnaMaster and PyJHora outputs BEFORE diffing.
Ensures formatting differences are never misclassified as bugs.
"""
from __future__ import annotations

import math

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LOOKUP = {s.lower(): s for s in SIGN_NAMES}
SIGN_LOOKUP.update({str(i): s for i, s in enumerate(SIGN_NAMES)})

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati",
]

# Common transliteration variants → canonical name
NAKSHATRA_VARIANTS: dict[str, str] = {
    "ashvini": "Ashwini",
    "krttika": "Krittika",
    "mrgashira": "Mrigashira",
    "mrigasira": "Mrigashira",
    "aridra": "Ardra",
    "thiruvadhirai": "Ardra",
    "pushyami": "Pushya",
    "aslesha": "Ashlesha",
    "makha": "Magha",
    "pubba": "Purva Phalguni",
    "purva phalguni": "Purva Phalguni",
    "uttara phalguni": "Uttara Phalguni",
    "hastham": "Hasta",
    "chitta": "Chitra",
    "chithra": "Chitra",
    "visakha": "Vishakha",
    "anusham": "Anuradha",
    "kettai": "Jyeshtha",
    "moola": "Mula",
    "pooradam": "Purva Ashadha",
    "purva ashadha": "Purva Ashadha",
    "uttaradam": "Uttara Ashadha",
    "uttara ashadha": "Uttara Ashadha",
    "thiruvonam": "Shravana",
    "sravana": "Shravana",
    "avittam": "Dhanishta",
    "dhanista": "Dhanishta",
    "sathayam": "Shatabhisha",
    "satabhisha": "Shatabhisha",
    "poorattadhi": "Purva Bhadrapada",
    "purva bhadrapada": "Purva Bhadrapada",
    "uttarattadhi": "Uttara Bhadrapada",
    "uttara bhadrapada": "Uttara Bhadrapada",
    "revathi": "Revati",
}

NAKSHATRA_LOOKUP = {n.lower(): n for n in NAKSHATRA_NAMES}
NAKSHATRA_LOOKUP.update(NAKSHATRA_VARIANTS)


def normalize_longitude(value: float) -> float:
    """Wrap longitude to [0, 360)."""
    if math.isnan(value):
        raise ValueError("NaN longitude")
    return value % 360.0


def normalize_sign(value: str | int) -> str:
    """Map sign name/index to canonical name."""
    if isinstance(value, int):
        if not 0 <= value <= 11:
            raise ValueError(f"Sign index out of range: {value}")
        return SIGN_NAMES[value]
    key = str(value).strip().lower()
    if key in SIGN_LOOKUP:
        return SIGN_LOOKUP[key]
    raise ValueError(f"Unknown sign: {value}")


def normalize_nakshatra(value: str | int) -> str:
    """Map nakshatra name/index/variant to canonical name."""
    if isinstance(value, int):
        if not 0 <= value <= 26:
            raise ValueError(f"Nakshatra index out of range: {value}")
        return NAKSHATRA_NAMES[value]
    key = str(value).strip().lower()
    if key in NAKSHATRA_LOOKUP:
        return NAKSHATRA_LOOKUP[key]
    raise ValueError(f"Unknown nakshatra: {value}")


def normalize_house_index(value: int, *, zero_indexed: bool = False) -> int:
    """Normalize house index to 1-12."""
    if zero_indexed:
        value = value + 1
    if not 1 <= value <= 12:
        raise ValueError(f"House index out of range: {value}")
    return value


def normalize_chart_output(data: dict, source: str) -> dict:
    """Normalize a full chart output dict from either engine.

    Args:
        data: Raw chart output (planet positions, nakshatras, etc.)
        source: 'lm' or 'pyjhora'

    Returns:
        Normalized dict with consistent types and ranges.
    """
    out = {}

    if "lagna_degree" in data:
        out["lagna_degree"] = normalize_longitude(data["lagna_degree"])
    if "lagna_sign" in data:
        out["lagna_sign"] = normalize_sign(data["lagna_sign"])

    planets = data.get("planets", {})
    out["planets"] = {}
    for name, pdata in planets.items():
        out["planets"][name] = {
            "longitude": normalize_longitude(pdata["longitude"]),
            "sign": normalize_sign(pdata["sign"]),
        }
        if "nakshatra" in pdata:
            out["planets"][name]["nakshatra"] = normalize_nakshatra(
                pdata["nakshatra"]
            )

    # Pass through fields that don't need normalization
    for key in ("ashtakavarga", "yogas", "dashas", "shadbala", "panchangam",
                "dignity", "house_lords"):
        if key in data:
            out[key] = data[key]

    return out
