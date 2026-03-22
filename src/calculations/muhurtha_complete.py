"""
src/calculations/muhurtha_complete.py
Complete Muhurtha engine — Tarabala, Chandrabala, Panchaka, Siddha/Amrita/Visa
Yogas, Abhijit Muhurtha, purpose-specific rule subsets.
Session 148 (Audit H-1, H-2).

Sources:
  Muhurta Chintamani — Daivagyna (Ranjan Publications)
  PVRNR · BPHS Muhurtha chapter
  Mantreswara · Phaladeepika Ch.26 v.20-25 (Tarabala)
  Standard Jyotish Muhurtha tables
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date, time, datetime, timedelta
from typing import Optional

# ─── Nakshatra names ──────────────────────────────────────────────────────────
_NAK = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishtha",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]

_WEEKDAY_LORDS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
]  # Mon=1

# ─── Tarabala ─────────────────────────────────────────────────────────────────
_TARA_NAMES = [
    "Janma",
    "Sampat",
    "Vipat",
    "Kshema",
    "Pratyak",
    "Sadhana",
    "Naidhana",
    "Mitra",
    "Param Mitra",
]
_TARA_QUALITY = {
    "Janma": "avoid",
    "Sampat": "good",
    "Vipat": "avoid",
    "Kshema": "good",
    "Pratyak": "avoid",
    "Sadhana": "excellent",
    "Naidhana": "avoid",
    "Mitra": "good",
    "Param Mitra": "excellent",
}


def tarabala(natal_nak_idx: int, transit_nak_idx: int) -> dict:
    count = ((transit_nak_idx - natal_nak_idx) % 27) + 1
    tara = _TARA_NAMES[(count - 1) % 9]
    return {
        "count": count,
        "tara": tara,
        "quality": _TARA_QUALITY[tara],
        "is_good": _TARA_QUALITY[tara] in ("good", "excellent"),
    }


# ─── Chandrabala ──────────────────────────────────────────────────────────────
_CHANDRA_GOOD = {1, 3, 6, 7, 10, 11}


def chandrabala(natal_moon_si: int, transit_moon_si: int) -> dict:
    house = ((transit_moon_si - natal_moon_si) % 12) + 1
    good = house in _CHANDRA_GOOD
    return {
        "house_from_natal": house,
        "is_good": good,
        "quality": "good" if good else "avoid",
    }


# ─── Panchaka Dosha ───────────────────────────────────────────────────────────
# Moon in Dhanu/Makara/Kumbha/Meena (8,9,10,11 = 0-indexed signs 8,9,10,11)
# with certain Tithis creates Panchaka Dosha

_PANCHAKA_SIGNS = {8, 9, 10, 11}  # Sagittarius, Capricorn, Aquarius, Pisces


def check_panchaka_dosha(
    transit_moon_si: int, weekday: int, nakshatra_idx: int
) -> dict:
    """
    Panchaka Dosha: Moon in Dhanu-Meena with certain conditions.
    Weekday: 0=Mon, 6=Sun. Panchaka Nakshatra: Dhanishtha(22), Shatabhisha(23),
    Purva Bhadrapada(24), Uttara Bhadrapada(25), Revati(26).
    Source: Standard Muhurtha texts
    """
    panchaka_naks = {22, 23, 24, 25, 26}
    has_dosha = transit_moon_si in _PANCHAKA_SIGNS and nakshatra_idx in panchaka_naks
    return {
        "panchaka_dosha": has_dosha,
        "note": "Moon in Panchaka Nakshatra — avoid fire, building, travel"
        if has_dosha
        else "No Panchaka",
    }


# ─── Vishti (Bhadra) Karana ───────────────────────────────────────────────────
# The most inauspicious Karana — 7th in each cycle of 11 Karanas


def check_vishti_karana(tithi: float) -> dict:
    """
    Vishti Karana occurs at specific positions in the lunar month.
    Each Karana = half-tithi. Vishti = 7th movable Karana.
    Source: BPHS Panchanga chapter; Muhurta Chintamani
    """
    karana_idx = int(tithi * 2) % 11
    is_vishti = karana_idx == 6  # 7th Karana (0-indexed = 6)
    return {
        "is_vishti": is_vishti,
        "note": "Vishti (Bhadra) Karana — universally avoid" if is_vishti else "OK",
    }


# ─── Vara-Nakshatra Yogas ─────────────────────────────────────────────────────
# Siddha, Amrita, Visa, Vyaghata, Vajra Yogas
# Source: Muhurta Chintamani; standard tables

# {weekday_idx: [nakshatra_indices that form that yoga with this day]}
_SIDDHA_YOGA: dict[int, set[int]] = {
    0: {7, 8, 10, 11},  # Sunday + Pushya/Ashlesha/Purva/Uttara Phalguni
    1: {3, 5, 6, 7},  # Monday + Rohini/Ardra/Punarvasu/Pushya
    2: {0, 3, 4, 25},  # Tuesday
    3: {4, 13, 14, 17},  # Wednesday
    4: {3, 5, 6, 7},  # Thursday
    5: {13, 14, 24, 26},  # Friday
    6: {7, 10, 11, 26},  # Saturday
}

_AMRITA_YOGA: dict[int, set[int]] = {
    0: {3, 12, 21},  # Sunday
    1: {14, 16, 17},  # Monday
    2: {5, 9, 15},  # Tuesday
    3: {2, 7, 20},  # Wednesday
    4: {0, 6, 25},  # Thursday
    5: {3, 12, 26},  # Friday
    6: {1, 8, 13},  # Saturday
}

_VISA_YOGA: dict[int, set[int]] = {
    0: {9, 10},  # Sunday — Ashlesha, Magha
    1: {16},  # Monday — Anuradha
    2: {17},  # Tuesday — Jyeshtha
    3: {18},  # Wednesday — Mula
    4: {19},  # Thursday
    5: {5},  # Friday — Ardra
    6: {6},  # Saturday
}


def check_vara_nakshatra_yogas(weekday: int, nak_idx: int) -> dict:
    """
    Check Vara-Nakshatra Yogas.
    weekday: 0=Sunday, 1=Monday, ... 6=Saturday
    Source: Muhurta Chintamani
    """
    yogas = []
    if nak_idx in _SIDDHA_YOGA.get(weekday, set()):
        yogas.append({"yoga": "Siddha", "quality": "excellent"})
    if nak_idx in _AMRITA_YOGA.get(weekday, set()):
        yogas.append({"yoga": "Amrita", "quality": "most_auspicious"})
    if nak_idx in _VISA_YOGA.get(weekday, set()):
        yogas.append(
            {
                "yoga": "Visa",
                "quality": "inauspicious",
                "note": "Visa Yoga — avoid important activities",
            }
        )

    return {
        "yogas": yogas,
        "has_siddha": any(y["yoga"] == "Siddha" for y in yogas),
        "has_amrita": any(y["yoga"] == "Amrita" for y in yogas),
        "has_visa": any(y["yoga"] == "Visa" for y in yogas),
    }


# ─── Abhijit Muhurtha ─────────────────────────────────────────────────────────


def compute_abhijit_muhurtha(sunrise_time: datetime, sunset_time: datetime) -> dict:
    """
    Abhijit Muhurtha: ~24 minutes centered on local solar noon.
    Most auspicious Muhurtha — overrides most Panchanga defects.
    Source: Muhurta Chintamani Ch.3; PVRNR BPHS
    """
    day_duration = sunset_time - sunrise_time
    solar_noon = sunrise_time + day_duration / 2
    window = timedelta(minutes=12)
    return {
        "solar_noon": solar_noon.time(),
        "abhijit_start": (solar_noon - window).time(),
        "abhijit_end": (solar_noon + window).time(),
        "note": "Most auspicious Muhurtha — overrides most Panchanga defects",
    }


# ─── Purpose-specific Muhurtha rules ─────────────────────────────────────────

_PURPOSE_RULES: dict[str, dict] = {
    "wedding": {
        "required_tara": {"Sampat", "Kshema", "Sadhana", "Mitra", "Param Mitra"},
        "avoid_nakshatras": {
            4,
            5,
            6,
            8,
            9,
            10,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            21,
            22,
            23,
        },  # avoid rough/fiery
        "required_chandra_houses": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},  # avoid H12
        "note": "Wedding: Moon in auspicious nakshatra and Tara essential",
    },
    "travel": {
        "required_tara": {"Sampat", "Kshema", "Sadhana", "Mitra", "Param Mitra"},
        "avoid_nakshatras": {4, 5, 8, 9, 17, 18},
        "required_chandra_houses": {1, 3, 6, 10, 11},
        "note": "Travel: Avoid Ardra, Mrigashira, Ashlesha",
    },
    "medical": {
        "required_tara": {"Sadhana", "Param Mitra", "Sampat"},
        "avoid_nakshatras": {3, 8, 9, 17, 18},  # avoid Rohini, Ashlesha, Jyeshtha
        "required_chandra_houses": {1, 3, 6, 10, 11},
        "note": "Medical: Siddha/Amrita yoga ideal; avoid Ashlesha",
    },
    "business": {
        "required_tara": {"Sampat", "Sadhana", "Mitra", "Param Mitra"},
        "avoid_nakshatras": {4, 5, 6, 8, 17, 18},
        "required_chandra_houses": {2, 3, 5, 6, 9, 10, 11},
        "note": "Business: H2/H11 Moon placement ideal for wealth",
    },
    "education": {
        "required_tara": {"Sampat", "Kshema", "Sadhana", "Mitra", "Param Mitra"},
        "avoid_nakshatras": {4, 5, 17, 18},
        "required_chandra_houses": {1, 2, 4, 5, 9, 10},
        "note": "Education: Mercury and Jupiter strong days preferred",
    },
}


@dataclass
class MuhurthaReport:
    query_date: date
    query_time: time
    tarabala: dict
    chandrabala: dict
    panchaka_dosha: dict
    vishti_karana: dict
    vara_nakshatra_yogas: dict
    abhijit: Optional[dict]
    purpose: str
    overall_quality: str  # "excellent"/"good"/"acceptable"/"avoid"
    defects: list[str]
    blessings: list[str]
    recommendation: str


def compute_muhurtha(
    natal_moon_nak_idx: int,
    natal_moon_si: int,
    transit_moon_nak_idx: int,
    transit_moon_si: int,
    weekday: int,  # 0=Sunday
    tithi: float,  # 0-30 (Tithi number, fractional)
    sunrise: Optional[datetime] = None,
    sunset: Optional[datetime] = None,
    purpose: str = "general",
    query_date: Optional[date] = None,
    query_time: Optional[time] = None,
) -> MuhurthaReport:
    """
    Compute comprehensive Muhurtha assessment.
    Source: Muhurta Chintamani; BPHS; Phaladeepika Ch.26
    """
    tb = tarabala(natal_moon_nak_idx, transit_moon_nak_idx)
    cb = chandrabala(natal_moon_si, transit_moon_si)
    pk = check_panchaka_dosha(transit_moon_si, weekday, transit_moon_nak_idx)
    vis = check_vishti_karana(tithi)
    vny = check_vara_nakshatra_yogas(weekday, transit_moon_nak_idx)

    abh = None
    if sunrise and sunset:
        abh = compute_abhijit_muhurtha(sunrise, sunset)

    defects = []
    blessings = []

    if not tb["is_good"]:
        defects.append(f"Tarabala: {tb['tara']} — {tb['quality']}")
    else:
        blessings.append(f"Tarabala: {tb['tara']} — {tb['quality']}")

    if not cb["is_good"]:
        defects.append(f"Chandrabala: H{cb['house_from_natal']} — avoid")
    else:
        blessings.append(f"Chandrabala: H{cb['house_from_natal']} — good")

    if pk["panchaka_dosha"]:
        defects.append(pk["note"])
    if vis["is_vishti"]:
        defects.append(vis["note"])

    if vny["has_amrita"]:
        blessings.append("Amrita Yoga — most auspicious")
    if vny["has_siddha"]:
        blessings.append("Siddha Yoga — excellent")
    if vny["has_visa"]:
        defects.append("Visa Yoga — inauspicious")

    # Overall quality
    if len(defects) == 0 and len(blessings) >= 2:
        quality = "excellent"
    elif len(defects) == 0:
        quality = "good"
    elif len(defects) == 1 and (vny["has_amrita"] or vny["has_siddha"]):
        quality = "acceptable"
    else:
        quality = "avoid"

    rec = f"{quality.title()} for {purpose}. "
    if defects:
        rec += f"Defects: {'; '.join(defects[:2])}. "
    if blessings:
        rec += f"Blessings: {'; '.join(blessings[:2])}."

    return MuhurthaReport(
        query_date=query_date or date.today(),
        query_time=query_time or time(0, 0),
        tarabala=tb,
        chandrabala=cb,
        panchaka_dosha=pk,
        vishti_karana=vis,
        vara_nakshatra_yogas=vny,
        abhijit=abh,
        purpose=purpose,
        overall_quality=quality,
        defects=defects,
        blessings=blessings,
        recommendation=rec,
    )
