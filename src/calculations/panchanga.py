"""
src/calculations/panchanga.py — Session 91

Panchanga: the five limbs of the Vedic almanac.
  1. Tithi    — lunar day (1-30), based on Sun-Moon longitude difference
  2. Vara     — weekday (0=Sun … 6=Sat)
  3. Nakshatra— Moon's nakshatra (1-27)
  4. Yoga     — sum of Sun+Moon longitude / (360/27)
  5. Karana   — half-tithi (11 fixed + 4 variable = 60 per month cycle)

PVRNR textbook: panchanga is the core almanac used in Muhurta selection.
Source: BPHS, standard Vedic almanac (Panchang).
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime

_TITHI_NAMES = [
    "Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami",
    "Shashthi","Saptami","Ashtami","Navami","Dashami",
    "Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima/Amavasya",
]
_NAKSHATRA_NAMES = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
    "Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni",
    "Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
    "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishtha",
    "Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati",
]
_YOGA_NAMES = [
    "Vishkamba","Priti","Ayushman","Saubhagya","Shobhana","Atiganda",
    "Sukarma","Dhriti","Shula","Ganda","Vriddhi","Dhruva",
    "Vyaghata","Harshana","Vajra","Siddhi","Vyatipata","Variyan",
    "Parigha","Shiva","Siddha","Sadhya","Shubha","Shukla",
    "Brahma","Indra","Vaidhriti",
]
_KARANA_NAMES = [
    "Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti",  # 7 variable
    "Shakuni","Chatushpada","Naga","Kimstughna",  # 4 fixed
]
_VARA_NAMES = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
_VARA_LORDS = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]

# Auspicious/inauspicious yogas from Nakshatra × Vara combinations
_AMRITA_SIDDHI = {  # (Vara_index, Nakshatra_0indexed) combinations
    (0,6),(0,22),(1,3),(1,21),(2,0),(2,4),(3,17),(3,9),
    (4,7),(4,15),(5,11),(5,24),(6,10),(6,25),
}
_SARVAARTHA_SIDDHI = {
    (0,0),(0,10),(0,12),(0,21),(1,4),(1,11),(1,14),(1,15),(1,21),
    (2,0),(2,2),(2,9),(2,26),(3,4),(3,11),(3,12),(3,21),
    (4,3),(4,4),(4,7),(4,10),(4,11),(4,14),(4,20),
    (5,0),(5,3),(5,4),(5,11),(5,14),(5,15),(5,20),(5,21),
    (6,2),(6,7),(6,10),(6,14),(6,15),(6,20),(6,21),(6,26),
}


@dataclass
class Panchanga:
    tithi: int            # 1-30
    tithi_name: str
    paksha: str           # "Shukla" (waxing) or "Krishna" (waning)
    vara: int             # 0=Sun…6=Sat
    vara_name: str
    vara_lord: str
    nakshatra: int        # 0-26
    nakshatra_name: str
    nakshatra_pada: int   # 1-4
    yoga: int             # 0-26
    yoga_name: str
    karana: int           # 0-10
    karana_name: str
    amrita_siddhi: bool
    sarvaartha_siddhi: bool
    is_auspicious: bool


def compute_panchanga(sun_lon: float, moon_lon: float,
                       dt: datetime | None = None) -> Panchanga:
    """
    Compute Panchanga from sidereal Sun and Moon longitudes.
    dt: datetime for Vara calculation (if None, uses today).
    """
    if dt is None:
        dt = datetime.now()

    # Tithi: every 12° difference = one tithi
    diff = (moon_lon - sun_lon) % 360
    tithi_raw = int(diff / 12) + 1   # 1-30
    paksha = "Shukla" if tithi_raw <= 15 else "Krishna"
    tithi_display = tithi_raw if tithi_raw <= 15 else tithi_raw - 15
    tithi_name = _TITHI_NAMES[min(tithi_display - 1, 14)]

    # Vara: weekday
    vara = dt.weekday()
    # Python: Mon=0…Sun=6 → Jyotish: Sun=0…Sat=6
    vara_jyotish = (vara + 1) % 7
    vara_name = _VARA_NAMES[vara_jyotish]
    vara_lord = _VARA_LORDS[vara_jyotish]

    # Nakshatra: every 13.333° = one nakshatra
    nak_raw = moon_lon * 27 / 360
    nakshatra = int(nak_raw) % 27
    nakshatra_pada = int((nak_raw % 1) * 4) + 1
    nakshatra_name = _NAKSHATRA_NAMES[nakshatra]

    # Yoga: (Sun+Moon) / (360/27)
    yoga_raw = (sun_lon + moon_lon) * 27 / 360
    yoga = int(yoga_raw) % 27
    yoga_name = _YOGA_NAMES[yoga]

    # Karana: half-tithi (tithi_raw 1-30, each has 2 karanas)
    karana_idx = ((tithi_raw - 1) * 2) % 11
    karana_name = _KARANA_NAMES[karana_idx]

    # Special yogas
    amrita = (vara_jyotish, nakshatra) in _AMRITA_SIDDHI
    sarva  = (vara_jyotish, nakshatra) in _SARVAARTHA_SIDDHI

    # General auspiciousness (simplified)
    auspicious = (amrita or sarva or
                  tithi_raw in {2,3,5,7,10,11,13,15} and
                  vara_jyotish in {1,3,4,5})

    return Panchanga(
        tithi=tithi_raw, tithi_name=tithi_name, paksha=paksha,
        vara=vara_jyotish, vara_name=vara_name, vara_lord=vara_lord,
        nakshatra=nakshatra, nakshatra_name=nakshatra_name,
        nakshatra_pada=nakshatra_pada,
        yoga=yoga, yoga_name=yoga_name,
        karana=karana_idx, karana_name=karana_name,
        amrita_siddhi=amrita, sarvaartha_siddhi=sarva,
        is_auspicious=auspicious,
    )


def compute_hora(dt: datetime, sunrise_hour: float = 6.0) -> tuple[str, int]:
    """
    Compute the planetary Hora (hour) running at a given time.
    Returns (planet_name, hora_number_1_to_24).
    Hora sequence starts from the weekday lord at sunrise.
    """
    # Hora lord sequence (always in this order from day start)
    _HORA_SEQ = ["Sun","Venus","Mercury","Moon","Saturn","Jupiter","Mars"]
    vara_jyotish = (dt.weekday() + 1) % 7
    hours_since_sunrise = (dt.hour + dt.minute / 60) - sunrise_hour
    if hours_since_sunrise < 0:
        hours_since_sunrise += 24
    hora_num = int(hours_since_sunrise) % 24
    # Start from the weekday lord (vara_jyotish maps to HORA_SEQ index)
    start_idx = [0,3,6,2,5,1,4][vara_jyotish]  # Sun→0,Moon→3,Mars→6,Mer→2,Jup→5,Ven→1,Sat→4
    hora_lord_idx = (start_idx + hora_num) % 7
    return _HORA_SEQ[hora_lord_idx], hora_num + 1


def compute_choghadiya(dt: datetime, sunrise_hour: float = 6.0,
                        sunset_hour: float = 18.0) -> dict:
    """
    Choghadiya: 8 time periods per day and 8 per night.
    Returns the current choghadiya name and quality.
    """
    _DAY_CHOGHADIYA  = ["Udveg","Char","Labh","Amrit","Kaal","Shubh","Rog","Udveg"]
    _NIGHT_CHOGHADIYA= ["Shubh","Amrit","Char","Rog","Kaal","Labh","Udveg","Shubh"]
    _QUALITY = {"Amrit":"Excellent","Shubh":"Good","Labh":"Good",
                "Char":"Neutral","Udveg":"Unfavorable","Rog":"Unfavorable","Kaal":"Unfavorable"}
    # Day choghadiya order varies by weekday
    _DAY_START = [5,6,4,3,2,1,0]  # Sun,Mon,Tue,Wed,Thu,Fri,Sat → starting index

    vara_j = (dt.weekday() + 1) % 7
    current_hour = dt.hour + dt.minute / 60
    is_day = sunrise_hour <= current_hour < sunset_hour

    if is_day:
        day_len = sunset_hour - sunrise_hour
        period_len = day_len / 8
        elapsed = current_hour - sunrise_hour
        period_idx = min(int(elapsed / period_len), 7)
        start = _DAY_START[vara_j]
        choghadiya_name = _DAY_CHOGHADIYA[(start + period_idx) % 8]
    else:
        night_len = 24 - (sunset_hour - sunrise_hour)
        if current_hour >= sunset_hour:
            elapsed = current_hour - sunset_hour
        else:
            elapsed = current_hour + (24 - sunset_hour)
        period_len = night_len / 8
        period_idx = min(int(elapsed / period_len), 7)
        choghadiya_name = _NIGHT_CHOGHADIYA[period_idx]

    return {"choghadiya": choghadiya_name,
            "quality": _QUALITY.get(choghadiya_name, "Neutral"),
            "is_day": is_day}


def compute_navamsha_chart(chart):
    try:
        from src.calculations.divisional_charts import compute_divisional_signs
        return compute_divisional_signs(chart)
    except Exception:
        return None

def _d9_sign_index(lon: float) -> int:
    sign = int(lon / 30) % 12
    deg_in_sign = lon % 30
    pada = int(deg_in_sign / (30/9))
    is_odd = (sign % 2 == 0)
    return (sign * 9 + pada) % 12 if is_odd else (sign * 9 + pada + 9) % 12
