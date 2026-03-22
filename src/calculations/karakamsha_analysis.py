"""
src/calculations/karakamsha_analysis.py
Karakamsha Lagna, Ishta Devata, Upapada analysis (Jaimini).
Session 150.

Requires Rashi Drishti from jaimini_rashi_drishti.py.

Sources:
  Jaimini Sutras Adhyaya 1 Pada 2 (Karakamsha)
  Sanjay Rath · Crux of Vedic Astrology Ch.8 (Ishta Devata)
  Sanjay Rath · Crux of Vedic Astrology, Upapada chapter
  PVRNR · BPHS Ch.32 (Atmakaraka and Karakamsha)
"""

from __future__ import annotations
from dataclasses import dataclass

# ─── Ishta Devata (Chosen Deity) from Karakamsha ─────────────────────────────
# Source: Sanjay Rath · Crux of Vedic Astrology Ch.8

# Planet → associated deity
PLANET_DEITY: dict[str, dict] = {
    "Sun": {"deity": "Shiva", "mantra_seed": "OM", "gemstone": "Ruby"},
    "Moon": {"deity": "Parvati/Devi", "mantra_seed": "SHREEM", "gemstone": "Pearl"},
    "Mars": {
        "deity": "Skanda/Kartikeya",
        "mantra_seed": "KREEM",
        "gemstone": "Red Coral",
    },
    "Mercury": {"deity": "Vishnu", "mantra_seed": "AIM", "gemstone": "Emerald"},
    "Jupiter": {
        "deity": "Brahma/Indra",
        "mantra_seed": "HREEM",
        "gemstone": "Yellow Sapphire",
    },
    "Venus": {"deity": "Lakshmi", "mantra_seed": "SHREEM", "gemstone": "Diamond"},
    "Saturn": {
        "deity": "Yama/Shani",
        "mantra_seed": "SHAM",
        "gemstone": "Blue Sapphire",
    },
    "Rahu": {
        "deity": "Durga/Saraswati",
        "mantra_seed": "RAAM",
        "gemstone": "Hessonite",
    },
    "Ketu": {"deity": "Ganesha/Brahma", "mantra_seed": "GAM", "gemstone": "Cat's Eye"},
}


@dataclass
class KarakamshaResult:
    atmakaraka: str  # AK planet
    karakamsha_sign: int  # D9 sign of AK
    karakamsha_sign_name: str
    ishta_devata: str  # Planet with strongest Rashi Drishti to Karakamsha
    ishta_deity_name: str
    ishta_mantra_seed: str
    ishta_gemstone: str
    planets_aspecting_karakamsha: list[str]
    is_swamsha: bool  # AK in own sign or exalt in D9


_SIGN_NAMES = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]


def compute_karakamsha_analysis(chart, chara_karaka_result) -> KarakamshaResult:
    """
    Compute Karakamsha and Ishta Devata.
    Requires: chara_karaka_result from chara_karaka_config.py
              Rashi Drishti from jaimini_rashi_drishti.py
    Source: Sanjay Rath · Crux of Vedic Astrology Ch.8; PVRNR · BPHS Ch.32
    """
    from src.calculations.jaimini_rashi_drishti import has_rashi_drishti
    from src.calculations.chara_karaka_config import compute_karakamsha, is_swamsha

    ak = chara_karaka_result.atmakaraka

    # Karakamsha Lagna = D9 sign of AK
    karakamsha_si = compute_karakamsha(chart, chara_karaka_result)

    # Planets with Rashi Drishti to Karakamsha sign
    aspecting = []
    for planet, pdata in chart.planets.items():
        if has_rashi_drishti(pdata.sign_index, karakamsha_si):
            aspecting.append(planet)

    # Ishta Devata = planet with strongest influence on Karakamsha
    # Priority: (1) planet IN Karakamsha sign, (2) strongest aspecting planet
    _NAT_STRENGTH = [
        "Sun",
        "Moon",
        "Venus",
        "Jupiter",
        "Mercury",
        "Mars",
        "Saturn",
        "Rahu",
        "Ketu",
    ]

    ishta_planet = None
    # First check if any planet is IN Karakamsha sign
    for p in _NAT_STRENGTH:
        if p in chart.planets and chart.planets[p].sign_index == karakamsha_si:
            ishta_planet = p
            break

    # If not, use strongest planet with Rashi Drishti
    if ishta_planet is None:
        for p in _NAT_STRENGTH:
            if p in aspecting:
                ishta_planet = p
                break

    if ishta_planet is None:
        ishta_planet = "Jupiter"  # default

    deity_info = PLANET_DEITY.get(ishta_planet, PLANET_DEITY["Jupiter"])

    swamsha = is_swamsha(chart, chara_karaka_result)

    return KarakamshaResult(
        atmakaraka=ak,
        karakamsha_sign=karakamsha_si,
        karakamsha_sign_name=_SIGN_NAMES[karakamsha_si],
        ishta_devata=ishta_planet,
        ishta_deity_name=deity_info["deity"],
        ishta_mantra_seed=deity_info["mantra_seed"],
        ishta_gemstone=deity_info["gemstone"],
        planets_aspecting_karakamsha=aspecting,
        is_swamsha=swamsha,
    )


# ─── Upapada (A12) Analysis ───────────────────────────────────────────────────


@dataclass
class UpakadaResult:
    upapada_sign: int
    upapada_sign_name: str
    planets_in_upapada: list[str]
    planets_aspecting_upapada: list[str]  # via Rashi Drishti
    spouse_quality: str  # brief description
    marriage_indicators: list[str]


def compute_upapada_analysis(chart, upapada_sign: int) -> UpakadaResult:
    """
    Analyse the Upapada Lagna (A12) for marriage partner quality.
    Requires Rashi Drishti from jaimini_rashi_drishti.py.
    Source: Sanjay Rath · Crux of Vedic Astrology, Upapada chapter
    """
    from src.calculations.jaimini_rashi_drishti import has_rashi_drishti

    # Planets in Upapada sign
    in_upapada = [p for p, pd in chart.planets.items() if pd.sign_index == upapada_sign]

    # Planets aspecting Upapada by Rashi Drishti
    aspecting = [
        p
        for p, pd in chart.planets.items()
        if has_rashi_drishti(pd.sign_index, upapada_sign)
        and pd.sign_index != upapada_sign
    ]

    # Spouse quality from planets
    benefics = {"Jupiter", "Venus", "Moon", "Mercury"}
    malefics = {"Saturn", "Mars", "Sun", "Rahu", "Ketu"}

    benefic_influence = [p for p in (in_upapada + aspecting) if p in benefics]
    malefic_influence = [p for p in (in_upapada + aspecting) if p in malefics]

    indicators = []
    if "Jupiter" in benefic_influence:
        indicators.append("Jupiter influence: pious, learned, prosperous spouse")
    if "Venus" in benefic_influence:
        indicators.append("Venus influence: attractive, artistic, refined spouse")
    if "Moon" in benefic_influence:
        indicators.append("Moon influence: nurturing, emotionally sensitive spouse")
    if "Saturn" in malefic_influence and not benefic_influence:
        indicators.append("Saturn without benefic: delays or difficulties in marriage")
    if "Mars" in malefic_influence and not benefic_influence:
        indicators.append(
            "Mars without benefic: passionate but potentially combative partner"
        )
    if not indicators:
        indicators.append("Mixed or neutral influences on Upapada")

    if len(benefic_influence) > len(malefic_influence):
        spouse_quality = "Generally favorable spouse indications"
    elif len(malefic_influence) > len(benefic_influence):
        spouse_quality = "Challenges in marriage partnership indicated"
    else:
        spouse_quality = "Mixed indications — highly dependent on other factors"

    return UpakadaResult(
        upapada_sign=upapada_sign,
        upapada_sign_name=_SIGN_NAMES[upapada_sign],
        planets_in_upapada=in_upapada,
        planets_aspecting_upapada=aspecting,
        spouse_quality=spouse_quality,
        marriage_indicators=indicators,
    )
