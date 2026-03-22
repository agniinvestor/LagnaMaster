"""
src/calculations/muhurta.py — Session 92

Muhurta: electional astrology — selecting auspicious timing for specific tasks.
Source: PVRNR textbook Table 79 (p473-476), BPHS Muhurta chapters.

Task categories (from Table 79):
  marriage, business_launch, house_construction, house_entry,
  travel, surgery, education, sacred_thread, new_vehicle,
  job_start, investment, general

Key rules:
  - 8th house of muhurta chart should be empty (most tasks)
  - Lagna lord should be strong
  - Concerned divisional chart should also be strong
  - Hora of the relevant planet is important (PVRNR p485)
  - Moon's nakshatra should be auspicious for the task
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

# PVRNR Table 79 — task-specific guidelines
_TASK_RULES = {
    "marriage": {
        "good_tithis": {2, 3, 5, 7, 10, 11, 13},
        "bad_tithis": {4, 6, 8, 9, 12, 14},
        "good_varas": {1, 3, 4, 5},  # Mon,Wed,Thu,Fri
        "bad_varas": {0, 2, 6},  # Sun,Tue,Sat
        "good_lagnas": {1, 2, 5, 8, 9, 10, 11},  # Ta,Ge,Vi,Sg,Aq,Pi (Le,Sc also)
        "good_naks": {
            0,
            3,
            4,
            6,
            7,
            10,
            11,
            12,
            13,
            14,
            15,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
        },
        "rule": "8th house empty; 7th house occupied by benefics is fine",
        "key_house": 7,
    },
    "business_launch": {
        "good_tithis": {2, 3, 5, 7, 10, 11},
        "bad_tithis": {4, 6, 8, 9, 12, 14},
        "good_varas": {1, 3, 4, 5},
        "bad_varas": {0, 2},
        "good_lagnas": {2, 5, 9, 10, 11},
        "good_naks": {0, 3, 6, 10, 11, 12, 13, 14, 20, 21, 22, 25, 26},
        "rule": "8th house empty; 10th house strong; lagna lord strong",
        "key_house": 10,
    },
    "house_construction": {
        "good_tithis": {2, 3, 5, 7, 11, 13, 15},
        "bad_tithis": {4, 6, 8, 9, 12, 14},
        "good_varas": {1, 3, 4, 5},
        "bad_varas": {2, 6},
        "good_lagnas": {1, 2, 5, 9, 10, 11},
        "good_naks": {
            0,
            3,
            4,
            6,
            10,
            11,
            12,
            13,
            14,
            15,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
        },
        "rule": "8th house empty; 4th house strong",
        "key_house": 4,
    },
    "house_entry": {
        "good_tithis": {2, 3, 5, 7, 10, 11, 13, 15},
        "bad_tithis": {4, 6, 8, 9, 12, 14},
        "good_varas": {1, 3, 4, 5},
        "bad_varas": {2, 6},
        "good_lagnas": {1, 2, 4, 5, 8, 9, 10, 11},
        "good_naks": {
            0,
            3,
            4,
            6,
            7,
            10,
            11,
            12,
            13,
            14,
            15,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
        },
        "rule": "8th house empty; 4th house strong",
        "key_house": 4,
    },
    "travel": {
        "good_tithis": {2, 3, 5, 7, 10, 11},
        "bad_tithis": {4, 6, 8, 9, 12, 14},
        "good_varas": {1, 3, 4, 5},
        "bad_varas": {6},
        "good_lagnas": {2, 5, 9, 11},
        "good_naks": {0, 3, 4, 6, 10, 11, 12, 13, 14, 15, 20, 21, 22, 25, 26},
        "rule": "3rd house strong; avoid Gandanta periods",
        "key_house": 3,
    },
    "surgery": {
        "good_tithis": {1, 6, 7, 11},
        "bad_tithis": {4, 8, 9, 12, 14},
        "good_varas": {0, 2},  # Sun,Tue
        "bad_varas": {4, 5},  # Thu,Fri
        "good_lagnas": {0, 6, 8},
        "good_naks": {0, 4, 6, 7, 12, 21, 22},
        "rule": "Avoid nakshatra of affected body part; 8th house concerns",
        "key_house": 8,
    },
    "education": {
        "good_tithis": {2, 3, 5, 7, 10, 11, 12},
        "bad_tithis": {4, 6, 8, 9, 14},
        "good_varas": {1, 3, 4, 5},
        "bad_varas": {6},
        "good_lagnas": {2, 5, 9, 11},
        "good_naks": {0, 6, 12, 13, 14, 15, 21, 22, 23, 25, 26},
        "rule": "8th house empty; 5th house strong; Mercury strong",
        "key_house": 5,
    },
    "general": {
        "good_tithis": {2, 3, 5, 7, 10, 11, 13},
        "bad_tithis": {4, 6, 8, 9, 12, 14},
        "good_varas": {1, 3, 4, 5},
        "bad_varas": {6},
        "good_lagnas": {1, 2, 4, 5, 9, 10, 11},
        "good_naks": {0, 3, 6, 10, 11, 12, 13, 14, 20, 21, 22, 25, 26},
        "rule": "8th house empty; lagna lord strong",
        "key_house": 1,
    },
}

# Abhijit Muhurta: 48 minutes before and after midday solar time
# Tarabala: count from birth nakshatra to transit nakshatra
_TARABALA_GOOD = {1, 3, 5, 7}  # Janma(1), Sampat(3), Kshema(5), Mitra(7)
# Chandrabala: Moon's sign from birth Moon sign — good positions
_CHANDRABALA_GOOD = {1, 3, 6, 7, 10, 11}


@dataclass
class MuhurtaScore:
    task: str
    tithi_ok: bool
    vara_ok: bool
    nakshatra_ok: bool
    lagna_ok: bool
    tarabala_ok: bool
    chandrabala_ok: bool
    special_yoga: str  # "Amrita Siddhi" / "Sarvaartha Siddhi" / ""
    total_score: int  # 0-6
    quality: str  # "Excellent"/"Good"/"Acceptable"/"Avoid"
    rule_notes: str
    warnings: list[str] = field(default_factory=list)


def score_muhurta(
    task: str,
    panchanga,
    birth_nakshatra: int = 0,
    birth_moon_sign: int = 3,
    muhurta_lagna_sign: int = 0,
) -> MuhurtaScore:
    """
    Score a muhurta for a specific task.
    panchanga: Panchanga object from compute_panchanga()
    birth_nakshatra: native's birth Moon nakshatra (0-26)
    birth_moon_sign: native's natal Moon sign index (0-11)
    muhurta_lagna_sign: lagna sign of the muhurta chart (0-11)
    """
    rules = _TASK_RULES.get(task, _TASK_RULES["general"])
    warnings = []

    tithi_ok = panchanga.tithi in rules["good_tithis"]
    if panchanga.tithi in rules.get("bad_tithis", set()):
        tithi_ok = False
        warnings.append(f"Tithi {panchanga.tithi_name} is inauspicious for {task}")

    vara_ok = panchanga.vara in rules["good_varas"]
    if panchanga.vara in rules.get("bad_varas", set()):
        vara_ok = False
        warnings.append(f"Vara {panchanga.vara_name} is inauspicious for {task}")

    nak_ok = panchanga.nakshatra in rules["good_naks"]

    lagna_ok = muhurta_lagna_sign in rules.get("good_lagnas", set(range(12)))

    # Tarabala: count from birth nakshatra to transit nakshatra
    tara_count = ((panchanga.nakshatra - birth_nakshatra) % 27) + 1
    tara_group = ((tara_count - 1) % 9) + 1
    tarabala_ok = tara_group in _TARABALA_GOOD

    # Chandrabala: Moon's current sign from birth Moon sign
    current_moon_sign = int(panchanga.nakshatra / 2.25)  # approximate
    chandra_count = ((current_moon_sign - birth_moon_sign) % 12) + 1
    chandrabala_ok = chandra_count in _CHANDRABALA_GOOD

    # Special yogas
    special = ""
    if panchanga.amrita_siddhi:
        special = "Amrita Siddhi Yoga"
    elif panchanga.sarvaartha_siddhi:
        special = "Sarvaartha Siddhi Yoga"

    # Total score
    score = sum([tithi_ok, vara_ok, nak_ok, lagna_ok, tarabala_ok, chandrabala_ok])
    if special:
        score = min(6, score + 1)

    if score >= 5:
        quality = "Excellent"
    elif score >= 4:
        quality = "Good"
    elif score >= 3:
        quality = "Acceptable"
    else:
        quality = "Avoid"

    return MuhurtaScore(
        task=task,
        tithi_ok=tithi_ok,
        vara_ok=vara_ok,
        nakshatra_ok=nak_ok,
        lagna_ok=lagna_ok,
        tarabala_ok=tarabala_ok,
        chandrabala_ok=chandrabala_ok,
        special_yoga=special,
        total_score=score,
        quality=quality,
        rule_notes=rules["rule"],
        warnings=warnings,
    )


def find_next_good_muhurta(
    task: str,
    start_dt: datetime,
    days_ahead: int = 30,
    birth_nakshatra: int = 0,
    birth_moon_sign: int = 3,
) -> list[dict]:
    """
    Scan forward to find good muhurta windows for a task.
    Returns list of {date, quality, score, panchanga_summary}.
    Simplified: checks each day at noon — real implementation uses ephemeris.
    """
    results = []
    from datetime import timedelta

    for d in range(days_ahead):
        dt = start_dt + timedelta(days=d)
        # placeholder — in full implementation, fetch sun/moon for this date
        results.append(
            {
                "date": dt.date().isoformat(),
                "note": "Use score_muhurta() with live ephemeris data for exact scoring",
            }
        )
    return results[:5]
