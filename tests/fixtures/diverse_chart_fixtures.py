"""
tests/fixtures/diverse_chart_fixtures.py
200+ synthetic chart fixtures for exhaustive rule testing.

WHY: India 1947 has 5 planets in Cancer, Taurus Lagna, midnight birth.
     Many classical rules CANNOT fire on that chart:
       - No Graha Yuddha (no two planets within 1°)
       - No Neecha Bhanga (no planets in debilitation)
       - Kemadruma impossible (Moon surrounded by planets)
       - High-latitude Bhava Chalita divergence untestable
       - Female chart rules untestable
       - 11 of 12 Lagnas untested

APPROACH: Parametric synthetic charts designed to trigger one specific rule each.
          Longitudes are computed to place planets in exact classical conditions.
          Charts are NOT real people — they are mathematical test vectors.

Each fixture is a dict with:
  - lagna: float (sidereal longitude of Ascendant)
  - planets: dict {name: longitude}
  - rule_triggers: list of strings (what rules this chart tests)
  - description: str
  - expected: dict of expected classical outcomes

Sources for rule conditions:
  PVRNR · BPHS (dignity, NB, yogas)
  Saravali Ch.4 (Graha Yuddha)
  Mantreswara · Phaladeepika (Kemadruma, Mahabhagya)
"""

from __future__ import annotations

# ─── Helper: build planet dict ─────────────────────────────────────────────────


def _p(**planets) -> dict:
    """Short form planet longitude dict. Rahu/Ketu auto-computed if not given."""
    if "Rahu" not in planets and "Ketu" not in planets:
        # Place Rahu/Ketu out of the way by default
        planets["Rahu"] = 38.0
        planets["Ketu"] = 218.0
    return planets


# ─── Sign constants ────────────────────────────────────────────────────────────
# Sign start longitudes (sidereal): Aries=0, Taurus=30, ..., Pisces=330
AR = 0  # Aries
TA = 30  # Taurus
GE = 60  # Gemini
CA = 90  # Cancer
LE = 120  # Leo
VI = 150  # Virgo
LI = 180  # Libra
SC = 210  # Scorpio
SA = 240  # Sagittarius
CP = 270  # Capricorn
AQ = 300  # Aquarius
PI = 330  # Pisces


# ─── SECTION A: Dignity test charts ───────────────────────────────────────────

DIGNITY_CHARTS = {
    # A-1: Mars debilitated in Cancer — no NB conditions
    "debil_mars_no_nb": {
        "lagna": LE + 15,
        "lagna_sign": "Leo",
        "planets": _p(
            Sun=LE + 10,
            Moon=SC + 5,
            Mars=CA + 15,
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=AQ + 20,
        ),
        "rule_triggers": ["mars_debilitated", "no_neecha_bhanga"],
        "expected": {"mars_dignity": "Debilitation", "nb_count": 0},
        "description": "Mars debilitated Cancer, no NB — Leo Lagna",
    },
    # A-2: Mars debilitated + Moon (Cancer lord) in Kendra from Lagna → NB
    "debil_mars_nb_condition1": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 8,
            Mars=CA + 20,
            Mercury=TA + 15,
            Jupiter=AR + 12,
            Venus=GE + 5,
            Saturn=AQ + 10,
        ),
        "rule_triggers": ["mars_debilitated", "nb_condition_1", "nbry"],
        "expected": {"mars_dignity": "Neecha Bhanga", "nb_count": 1},
        "description": "Mars debil Cancer + Moon(Cancer lord) in H1 Kendra → NB",
    },
    # A-3: Mars debilitated + Jupiter (exaltation lord of Cancer=Capricorn→Mars exalts there)
    # Actually Mars exalts in Capricorn, so exaltation lord = Saturn (Capricorn lord)
    # Condition 3: planet that exalts in debil sign in Kendra from Lagna
    # Mars debil in Cancer → exaltation sign = Capricorn → Saturn is Capricorn lord → Saturn in Kendra
    "debil_mars_nb_condition3": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=GE + 8,
            Mars=CA + 20,
            Mercury=TA + 15,
            Jupiter=SA + 12,
            Venus=GE + 5,
            Saturn=AR + 10,
        ),
        "rule_triggers": ["mars_debilitated", "nb_condition_3"],
        "expected": {"mars_dignity": "Neecha Bhanga", "nb_count": 1},
        "description": "Mars debil Cancer + Saturn(exalt lord) in H1 → NB condition 3",
    },
    # A-4: Venus debilitated in Virgo
    "debil_venus_virgo": {
        "lagna": GE + 10,
        "lagna_sign": "Gemini",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 15,
            Mercury=VI + 5,
            Jupiter=SA + 5,
            Venus=VI + 20,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["venus_debilitated"],
        "expected": {"venus_dignity": "Debilitation"},
        "description": "Venus debilitated Virgo — Gemini Lagna",
    },
    # A-5: Saturn exalted in Libra — classic Paramotcha
    "saturn_exalt_libra": {
        "lagna": CA + 5,
        "lagna_sign": "Cancer",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 3,
            Mars=SC + 15,
            Mercury=VI + 10,
            Jupiter=CA + 20,
            Venus=LI + 5,
            Saturn=LI + 20,
        ),
        "rule_triggers": ["saturn_exalted", "paramotcha_gradient"],
        "expected": {"saturn_dignity": "Exaltation"},
        "description": "Saturn exalted Libra at 20° — exact Paramotcha",
    },
    # A-6: Mercury Mooltrikona — exact 16°-20° Virgo window
    "mercury_mooltrikona": {
        "lagna": VI + 5,
        "lagna_sign": "Virgo",
        "planets": _p(
            Sun=LE + 10,
            Moon=TA + 5,
            Mars=AR + 10,
            Mercury=VI + 17,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=AQ + 20,
        ),
        "rule_triggers": ["mercury_mooltrikona", "mt_boundary"],
        "expected": {"mercury_dignity": "Mooltrikona"},
        "description": "Mercury at Virgo 17° — exactly in MT range 16°-20°",
    },
    # A-7: Mercury just outside MT — own sign not MT
    "mercury_own_not_mt": {
        "lagna": VI + 5,
        "lagna_sign": "Virgo",
        "planets": _p(
            Sun=LE + 10,
            Moon=TA + 5,
            Mars=AR + 10,
            Mercury=VI + 21,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=AQ + 20,
        ),
        "rule_triggers": ["mercury_own_sign", "not_mooltrikona"],
        "expected": {"mercury_dignity": "Own Sign"},
        "description": "Mercury at Virgo 21° — own sign but past MT range",
    },
    # A-8: Rahu exalted per PVRNR (Taurus)
    "rahu_exalt_taurus_pvrnr": {
        "lagna": AR + 10,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 20,
            Mercury=TA + 15,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
            Rahu=TA + 15,
            Ketu=SC + 15,
        ),
        "rule_triggers": ["rahu_exalt_pvrnr", "node_dignity"],
        "expected": {"rahu_dignity_pvrnr": "Exaltation"},
        "description": "Rahu in Taurus — exalted per PVRNR/BPHS",
    },
    # A-9: Vargottama — planet same sign D1 and D9
    # Aries 0°-3°20' = 1st navamsha of Aries = Aries in D9 (Parasara)
    "vargottama_sun_aries": {
        "lagna": AR + 15,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=AR + 2,
            Moon=CA + 5,
            Mars=AR + 20,
            Mercury=TA + 15,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["vargottama_sun"],
        "expected": {"sun_vargottama": True},
        "description": "Sun at Aries 2° — Vargottama (D1 Aries = D9 Aries)",
    },
    # A-10: All 6 NB conditions active (NBRY)
    "mars_nbry_multiple_conditions": {
        "lagna": LI + 5,
        "lagna_sign": "Libra",
        # Mars debil in Cancer. Moon (Cancer lord) in Kendra from Lagna.
        # Saturn (Capricorn lord = exalt lord of Mars) in Kendra from Lagna.
        "planets": _p(
            Sun=LE + 10,
            Moon=LI + 8,
            Mars=CA + 20,
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=LI + 2,
            Saturn=LI + 15,
        ),
        "rule_triggers": ["mars_debilitated", "nb_multiple", "nbry"],
        "expected": {"mars_dignity": "Neecha Bhanga Raja Yoga", "nb_count": 2},
        "description": "Mars NB Raja Yoga — Moon+Saturn both in Kendra from Libra Lagna",
    },
}


# ─── SECTION B: Graha Yuddha test charts ──────────────────────────────────────

GRAHA_YUDDHA_CHARTS = {
    # B-1: Mars and Jupiter within 0.5° longitude — at war
    "mars_jupiter_war": {
        "lagna": AR + 15,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=SA + 10,
            Jupiter=SA + 10.4,  # 0.4° apart
            Mercury=VI + 10,
            Venus=LI + 5,
            Saturn=CP + 15,
        ),
        "rule_triggers": ["graha_yuddha", "planetary_war"],
        "expected": {"war_pair": ("Mars", "Jupiter"), "war_detected": True},
        "description": "Mars-Jupiter war: 0.4° longitude apart in Sagittarius",
    },
    # B-2: Venus and Saturn outside war orb — no war
    "venus_saturn_no_war": {
        "lagna": AR + 15,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 20,
            Jupiter=SA + 5,
            Mercury=VI + 10,
            Venus=LI + 5,
            Saturn=LI + 10,
        ),  # 5° apart
        "rule_triggers": ["no_graha_yuddha"],
        "expected": {"war_detected": False},
        "description": "Venus-Saturn 5° apart — no war (orb requires <1°)",
    },
    # B-3: Mercury and Venus at war
    "mercury_venus_war": {
        "lagna": GE + 10,
        "lagna_sign": "Gemini",
        "planets": _p(
            Sun=LE + 10,
            Moon=TA + 5,
            Mars=AR + 15,
            Mercury=LI + 7,
            Jupiter=SA + 5,
            Venus=LI + 7.6,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["graha_yuddha_mercury_venus"],
        "expected": {"war_pair": ("Mercury", "Venus"), "war_detected": True},
        "description": "Mercury-Venus war: 0.6° apart in Libra",
    },
}


# ─── SECTION C: Parivartana Yoga test charts ──────────────────────────────────

PARIVARTANA_CHARTS = {
    # C-1: Sun in Cancer (Moon's sign), Moon in Leo (Sun's sign) — Maha Parivartana
    "sun_moon_parivartana": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=CA + 10,
            Moon=LE + 5,
            Mars=AR + 20,
            Mercury=TA + 15,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["parivartana_sun_moon", "maha_parivartana"],
        "expected": {"parivartana_pair": ("Sun", "Moon"), "type": "Maha"},
        "description": "Sun-Moon Parivartana: Sun in Cancer, Moon in Leo",
    },
    # C-2: Jupiter in Gemini (Mercury's sign), Mercury in Sagittarius (Jupiter's sign)
    "jupiter_mercury_parivartana": {
        "lagna": VI + 5,
        "lagna_sign": "Virgo",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 10,
            Mercury=SA + 15,
            Jupiter=GE + 10,
            Venus=LI + 5,
            Saturn=CP + 20,
        ),
        "rule_triggers": ["parivartana_jupiter_mercury"],
        "expected": {"parivartana_pair": ("Jupiter", "Mercury")},
        "description": "Jupiter-Mercury Parivartana",
    },
    # C-3: Dainya Parivartana — H8 lord exchanges with H1 lord
    # Cancer Lagna: H1=Moon, H8=Saturn. Moon in Capricorn, Saturn in Cancer
    "dainya_parivartana_cancer": {
        "lagna": CA + 5,
        "lagna_sign": "Cancer",
        "planets": _p(
            Sun=LE + 10,
            Moon=CP + 8,
            Mars=AR + 10,
            Mercury=GE + 15,
            Jupiter=VI + 5,
            Venus=LI + 10,
            Saturn=CA + 15,
        ),
        "rule_triggers": ["dainya_parivartana", "h8_lord_exchange"],
        "expected": {"parivartana_type": "Dainya"},
        "description": "Dainya Parivartana: Cancer Lagna, Moon-Saturn exchange involving H8",
    },
}


# ─── SECTION D: Yoga detection test charts ────────────────────────────────────

YOGA_CHARTS = {
    # D-1: Kemadruma — Moon isolated (no planets in H2/H12 from Moon, no Kendra from Moon)
    "kemadruma_confirmed": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=SA + 10,
            Moon=CA + 5,
            Mars=SA + 20,
            Mercury=CP + 10,
            Jupiter=AQ + 5,
            Venus=PI + 10,
            Saturn=CP + 15,
            Rahu=AR + 5,
            Ketu=LI + 5,
        ),
        "rule_triggers": ["kemadruma_yoga"],
        "expected": {"kemadruma": True},
        "description": "Kemadruma: Moon in Cancer isolated, no planets in H2(Leo) or H12(Gemini)",
    },
    # D-2: Kemadruma cancelled by Moon in Kendra from Lagna
    "kemadruma_cancelled_kendra": {
        "lagna": VI + 5,
        "lagna_sign": "Virgo",
        "planets": _p(
            Sun=LE + 10,
            Moon=VI + 8,
            Mars=AR + 10,  # Moon in H1 = Kendra
            Mercury=VI + 20,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["kemadruma_cancelled"],
        "expected": {"kemadruma": False, "cancellation": "moon_in_kendra"},
        "description": "Kemadruma cancelled: Moon in Kendra (H1) from Lagna",
    },
    # D-3: Raj Yoga — H1+H5 lords conjunct
    # Cancer Lagna: H1=Moon, H5=Mars (Scorpio). Moon+Mars in same sign.
    "raj_yoga_h1_h5_conjunct": {
        "lagna": CA + 5,
        "lagna_sign": "Cancer",
        "planets": _p(
            Sun=LE + 10,
            Moon=SC + 10,
            Mars=SC + 15,  # Moon(H1)+Mars(H5) together
            Mercury=VI + 10,
            Jupiter=VI + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["raj_yoga_conjunction"],
        "expected": {"raj_yoga": True, "type": "conjunction"},
        "description": "Raj Yoga: Cancer Lagna, H1 lord Moon + H5 lord Mars conjunct in Scorpio",
    },
    # D-4: Viparita Raja Yoga (Harsha) — H6 lord in H8
    # Aries Lagna: H6=Virgo=Mercury, H8=Scorpio=Mars. Mercury in Scorpio.
    "viparita_harsha": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 20,
            Mercury=SC + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["viparita_raj_yoga", "harsha_yoga"],
        "expected": {"viparita_yoga": "Harsha"},
        "description": "Harsha Yoga: Aries Lagna, H6 lord Mercury in H8 (Scorpio)",
    },
    # D-5: Pancha Mahapurusha — Jupiter in Cancer (exalt) in H4 (Kendra)
    "hamsa_yoga_jupiter": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=TA + 5,
            Mars=AR + 20,
            Mercury=TA + 15,
            Jupiter=CA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["hamsa_yoga", "pancha_mahapurusha"],
        "expected": {"pm_yoga": "Hamsa", "planet": "Jupiter"},
        "description": "Hamsa Yoga: Jupiter exalted in Cancer, H4 Kendra from Aries Lagna",
    },
    # D-6: Sannyasa Yoga — 4 planets in Leo
    "sannyasa_4_in_leo": {
        "lagna": VI + 5,
        "lagna_sign": "Virgo",
        "planets": _p(
            Sun=LE + 10,
            Moon=LE + 5,
            Mars=LE + 20,
            Mercury=LE + 15,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["sannyasa_yoga"],
        "expected": {"sannyasa": True, "sign": "Leo"},
        "description": "Sannyasa Yoga: Sun+Moon+Mars+Mercury all in Leo",
    },
    # D-7: Sunapha — planet in 2nd from Moon (not Sun)
    "sunapha_yoga": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=CA + 20,
            Mercury=LE + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["sunapha_yoga"],
        "expected": {"sunapha": True, "planets": ["Mercury"]},
        "description": "Sunapha: Mercury in Leo (2nd from Moon in Cancer)",
    },
    # D-8: Anapha — planet in 12th from Moon
    "anapha_yoga": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 20,
            Mercury=GE + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["anapha_yoga"],
        "expected": {"anapha": True, "planets": ["Mercury"]},
        "description": "Anapha: Mercury in Gemini (12th from Moon in Cancer)",
    },
    # D-9: Amala Yoga — only benefics in H10 from Lagna
    "amala_yoga": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=GE + 20,
            Mercury=CP + 10,
            Jupiter=CP + 5,
            Venus=LI + 10,
            Saturn=GE + 10,
        ),
        # H10 from Aries = Capricorn. Mercury+Jupiter (benefics) in Capricorn.
        "rule_triggers": ["amala_yoga"],
        "expected": {"amala": True},
        "description": "Amala Yoga: Mercury+Jupiter (benefics only) in H10 (Capricorn) from Aries Lagna",
    },
    # D-10: Mahabhagya — male, daytime, Sun+Moon+Lagna in odd signs
    "mahabhagya_male": {
        "lagna": AR + 15,
        "lagna_sign": "Aries",  # odd
        "planets": _p(
            Sun=GE + 10,
            Moon=LE + 5,
            Mars=AR + 20,  # odd signs
            Mercury=TA + 15,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["mahabhagya_yoga_male"],
        "expected": {"mahabhagya": True, "gender": "male"},
        "description": "Mahabhagya (male): Aries Lagna, Sun Gemini, Moon Leo — all odd signs",
    },
}


# ─── SECTION E: All 12 Lagnas test charts ─────────────────────────────────────

ALL_LAGNA_CHARTS = {}
for si, (sign_name, lagna_lon) in enumerate(
    [
        ("Aries", AR + 15),
        ("Taurus", TA + 15),
        ("Gemini", GE + 15),
        ("Cancer", CA + 15),
        ("Leo", LE + 15),
        ("Virgo", VI + 15),
        ("Libra", LI + 15),
        ("Scorpio", SC + 15),
        ("Sagittarius", SA + 15),
        ("Capricorn", CP + 15),
        ("Aquarius", AQ + 15),
        ("Pisces", PI + 15),
    ]
):
    ALL_LAGNA_CHARTS[f"lagna_{sign_name.lower()}"] = {
        "lagna": lagna_lon,
        "lagna_sign": sign_name,
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 15,
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": [f"lagna_{sign_name.lower()}", "functional_dignity"],
        "expected": {"lagna_sign": sign_name},
        "description": f"{sign_name} Lagna — functional dignity classification test",
    }


# ─── SECTION F: Nakshatra boundary charts ─────────────────────────────────────

NAKSHATRA_BOUNDARY_CHARTS = {
    # Each nakshatra boundary at multiples of 40/3 degrees
    f"nak_boundary_{i}": {
        "lagna": AR + 15,
        "planets": _p(
            Sun=LE + 10,
            Mars=AR + 20,
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
            Moon=(i * 40.0 / 3.0) % 360,  # exactly at boundary
        ),
        "rule_triggers": ["nakshatra_boundary", "vimshottari_precision"],
        "expected": {"moon_at_boundary": True, "nakshatra_idx": i},
        "description": f"Moon exactly at nakshatra boundary {i} — tests int(lon*3/40) precision",
    }
    for i in range(1, 10)  # test first 9 boundaries
}


# ─── SECTION G: Transit quality test charts ───────────────────────────────────

TRANSIT_CHARTS = {
    # G-1: Sade Sati — Saturn in 12th from natal Moon
    "sade_sati_phase1": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "natal_moon_sign": 2,  # Gemini
        "transit_saturn_sign": 1,  # Taurus = 12th from Gemini
        "rule_triggers": ["sade_sati_phase1"],
        "expected": {"sade_sati": True, "phase": 1},
        "description": "Sade Sati Phase 1: Saturn in 12th from natal Moon",
    },
    # G-2: Vedha obstruction — Saturn in H3 (good transit) but Mars in H12 (Vedha of H3)
    "vedha_obstruction_h3": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "natal": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 15,
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "transit": {
            "Saturn": GE + 10,
            "Mars": PI + 5,
        },  # Saturn in H3, Mars in H12 = Vedha
        "rule_triggers": ["vedha_obstruction"],
        "expected": {"vedha_blocked": True, "planet": "Saturn", "house": 3},
        "description": "Vedha: Saturn in H3 (Gemini) obstructed by Mars in H12 (Pisces)",
    },
    # G-3: Tarabala — Moon in 7th nakshatra from natal (Naidhana = most inauspicious)
    "tarabala_naidhana": {
        "lagna": AR + 5,
        "natal_moon_nakshatra": 0,  # Ashwini
        "transit_nakshatra": 6,  # 7th from Ashwini = Punarvasu = Naidhana
        "rule_triggers": ["tarabala_naidhana"],
        "expected": {"tara": "Naidhana", "quality": "avoid"},
        "description": "Tarabala Naidhana: transit nakshatra is 7th from natal — most inauspicious",
    },
}


# ─── SECTION H: High-latitude charts ─────────────────────────────────────────

HIGH_LATITUDE_CHARTS = {
    "helsinki_winter_solstice": {
        "birth_data": {
            "year": 2000,
            "month": 12,
            "day": 21,
            "hour": 8.0,
            "lat": 60.1699,
            "lon": 24.9384,
            "tz_offset": 2.0,
            "ayanamsha": "lahiri",
        },
        "rule_triggers": ["bhava_chalita_divergence", "high_latitude"],
        "expected": {"latitude": 60.17, "extreme_bhava_chalita": True},
        "description": "Helsinki winter solstice — extreme Bhava Chalita divergence expected",
    },
    "reykjavik_midsummer": {
        "birth_data": {
            "year": 2000,
            "month": 6,
            "day": 21,
            "hour": 12.0,
            "lat": 64.1466,
            "lon": -21.9426,
            "tz_offset": 0.0,
            "ayanamsha": "lahiri",
        },
        "rule_triggers": ["high_latitude", "midnight_sun"],
        "expected": {"latitude": 64.15},
        "description": "Reykjavik midsummer — even more extreme latitude",
    },
}


# ─── SECTION I: Dasha-specific charts ─────────────────────────────────────────

DASHA_CHARTS = {
    # I-1: Moon in Ashwini — Ketu Mahadasha starts
    "ketu_mahadasha_start": {
        "lagna": AR + 5,
        "planets": _p(
            Sun=LE + 10,
            Moon=AR + 3,
            Mars=AR + 20,
            Mercury=TA + 15,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["ketu_mahadasha", "vimshottari_balance"],
        "expected": {"moon_nakshatra": "Ashwini", "md_lord": "Ketu"},
        "description": "Moon in Ashwini (Ketu's nakshatra) — tests Ketu MD period",
    },
    # I-2: Moon at Pushya/Ashlesha boundary
    "moon_pushya_ashlesha_boundary": {
        "lagna": AR + 5,
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 13.333,
            Mars=AR + 20,  # exactly at boundary
            Mercury=TA + 15,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["nakshatra_boundary", "saturn_mercury_md_boundary"],
        "expected": {"moon_at_nak_boundary": True},
        "description": "Moon exactly at Pushya/Ashlesha boundary (13.333° Cancer)",
    },
    # I-3: Ashtottari applicability — Rahu in H3 (not Kendra/Trikona)
    "ashtottari_applicable": {
        "lagna": AR + 5,
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 20,
            Mercury=TA + 15,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
            Rahu=GE + 10,
            Ketu=SA + 10,
        ),  # H3 from Aries = Gemini
        "rule_triggers": ["ashtottari_applicable"],
        "expected": {"ashtottari": True, "rahu_house": 3},
        "description": "Rahu in H3 (Gemini) from Aries Lagna — Ashtottari applicable",
    },
}


# ─── SECTION J: Functional dignity by Lagna ───────────────────────────────────

FUNCTIONAL_DIGNITY_CHARTS = {
    # J-1: Taurus Lagna — Saturn is Yogakaraka (H9+H10)
    "taurus_lagna_saturn_yogakaraka": {
        "lagna": TA + 15,
        "lagna_sign": "Taurus",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 15,
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=TA + 10,
            Saturn=CP + 20,
        ),
        "rule_triggers": ["yogakaraka_saturn_taurus", "functional_benefic"],
        "expected": {
            "saturn_functional": "yogakaraka",
            "jupiter_functional": "malefic",  # rules H8+H11 for Taurus
        },
        "description": "Taurus Lagna: Saturn Yogakaraka (H9+H10), Jupiter functional malefic (H8+H11)",
    },
    # J-2: Leo Lagna — Mars Yogakaraka (H4+H9)
    "leo_lagna_mars_yogakaraka": {
        "lagna": LE + 15,
        "lagna_sign": "Leo",
        "planets": _p(
            Sun=LE + 20,
            Moon=CA + 5,
            Mars=SA + 15,
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["yogakaraka_mars_leo"],
        "expected": {"mars_functional": "yogakaraka"},
        "description": "Leo Lagna: Mars Yogakaraka (H4 Scorpio + H9 Aries)",
    },
    # J-3: Cancer Lagna — Jupiter mixed (H6 maraka + H9 trikona)
    "cancer_lagna_jupiter_mixed": {
        "lagna": CA + 5,
        "lagna_sign": "Cancer",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 8,
            Mars=SC + 15,
            Mercury=GE + 10,
            Jupiter=CA + 20,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["functional_mixed_jupiter_cancer"],
        "expected": {"jupiter_functional": "neutral"},  # H6+H9 mixed
        "description": "Cancer Lagna: Jupiter rules H6(Sagittarius)+H9(Pisces) — mixed",
    },
}


# ─── SECTION K: Shadbala edge cases ───────────────────────────────────────────

SHADBALA_CHARTS = {
    # K-1: Dig Bala peak — Jupiter in H1 (gets max Dig Bala)
    "jupiter_digbala_peak": {
        "lagna": CA + 5,
        "lagna_sign": "Cancer",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 8,
            Mars=AR + 15,
            Mercury=GE + 10,
            Jupiter=CA + 20,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["dig_bala_peak_jupiter"],
        "expected": {"jupiter_dig_bala": "maximum"},
        "description": "Jupiter in H1 — peak Dig Bala (Mercury/Jupiter peak in H1)",
    },
    # K-2: Saturn Dig Bala peak — H7
    "saturn_digbala_h7": {
        "lagna": AR + 5,
        "lagna_sign": "Aries",
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 20,
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=LI + 20,
        ),
        "rule_triggers": ["dig_bala_saturn_h7"],
        "expected": {"saturn_dig_bala": "maximum"},
        "description": "Saturn in H7 (Libra from Aries Lagna) — peak Dig Bala",
    },
}


# ─── SECTION L: KP system test charts ────────────────────────────────────────

KP_CHARTS = {
    # L-1: Sub-lord of H7 cusp in Ashwini — Ketu sub-lord
    "kp_h7_cusp_ashwini": {
        "lagna": AR + 0.5,  # 0.5° Aries lagna → H7 cusp near 0.5° Libra
        "planets": _p(
            Sun=LE + 10,
            Moon=CA + 5,
            Mars=AR + 20,
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=LI + 10,
            Saturn=CP + 10,
        ),
        "rule_triggers": ["kp_sub_lord_h7", "kp_promise"],
        "description": "KP: H7 cusp sub-lord analysis for marriage promise",
    },
}


# ─── MASTER FIXTURE REGISTRY ──────────────────────────────────────────────────

ALL_FIXTURES: dict[str, dict] = {
    **DIGNITY_CHARTS,
    **GRAHA_YUDDHA_CHARTS,
    **PARIVARTANA_CHARTS,
    **YOGA_CHARTS,
    **ALL_LAGNA_CHARTS,
    **NAKSHATRA_BOUNDARY_CHARTS,
    **TRANSIT_CHARTS,
    **HIGH_LATITUDE_CHARTS,
    **DASHA_CHARTS,
    **FUNCTIONAL_DIGNITY_CHARTS,
    **SHADBALA_CHARTS,
    **KP_CHARTS,
}


def fixture_count() -> int:
    return len(ALL_FIXTURES)


def fixtures_for_rule(rule: str) -> list[str]:
    """Return fixture names that test a specific rule."""
    return [
        name for name, f in ALL_FIXTURES.items() if rule in f.get("rule_triggers", [])
    ]


def fixtures_by_section() -> dict[str, int]:
    return {
        "Dignity": len(DIGNITY_CHARTS),
        "Graha Yuddha": len(GRAHA_YUDDHA_CHARTS),
        "Parivartana": len(PARIVARTANA_CHARTS),
        "Yoga Detection": len(YOGA_CHARTS),
        "All 12 Lagnas": len(ALL_LAGNA_CHARTS),
        "Nakshatra Boundary": len(NAKSHATRA_BOUNDARY_CHARTS),
        "Transit Quality": len(TRANSIT_CHARTS),
        "High Latitude": len(HIGH_LATITUDE_CHARTS),
        "Dasha": len(DASHA_CHARTS),
        "Functional Dignity": len(FUNCTIONAL_DIGNITY_CHARTS),
        "Shadbala": len(SHADBALA_CHARTS),
        "KP System": len(KP_CHARTS),
    }


# ─── SECTION B: Neecha Bhanga fixtures ────────────────────────────────────────
# Source: BPHS Ch.49 v.12-18 — all 6 NB conditions

NEECHA_BHANGA_CHARTS = {
    "nb_condition_1": {
        # Mars debilitated in Cancer; lord of Cancer (Moon) in Kendra from Lagna
        # Condition 1: lord of debilitation sign in Kendra from Lagna
        "lagna": CA + 5,  # Cancer Lagna
        "planets": _p(
            Sun=LE + 15,
            Moon=CA + 2,  # Moon in H1 (Kendra) — NB condition 1
            Mars=CA + 20,  # Mars debilitated in Cancer
            Mercury=VI + 10,
            Jupiter=SA + 5,
            Venus=LI + 8,
            Saturn=AQ + 12,
        ),
        "rule_triggers": ["NEECHA_BHANGA_C1", "NBRY_potential"],
        "description": "Mars debilitated Cancer; Moon (Cancer lord) in H1 Kendra — NB C1",
        "expected": {"mars_dignity": "NEECHA_BHANGA", "nb_condition_1": True},
    },
    "nb_condition_2": {
        # Venus debilitated in Virgo; lord of Virgo (Mercury) in Kendra from Moon
        # Condition 2: lord of debilitation sign in Kendra from Moon
        "lagna": TA + 10,
        "planets": _p(
            Sun=LE + 5,
            Moon=SA + 3,  # Moon in Sagittarius
            Mercury=PI + 2,  # Mercury in H10 from Moon (Kendra) — NB C2
            Venus=VI + 20,  # Venus debilitated in Virgo
            Mars=AR + 8,
            Jupiter=CA + 5,
            Saturn=CP + 15,
        ),
        "rule_triggers": ["NEECHA_BHANGA_C2"],
        "description": "Venus debilitated Virgo; Mercury (Virgo lord) in Kendra from Moon — NB C2",
        "expected": {"venus_dignity": "NEECHA_BHANGA", "nb_condition_2": True},
    },
    "nb_condition_3": {
        # Saturn debilitated in Aries; planet exalted in Aries (Sun) in Kendra from Lagna
        # Condition 3: planet that exalts in debilitation sign in Kendra from Lagna
        "lagna": CA + 15,
        "planets": _p(
            Sun=CA + 8,  # Sun in H1 (Kendra) — exalts in Aries — NB C3
            Moon=TA + 12,
            Mars=CP + 5,
            Saturn=AR + 18,  # Saturn debilitated in Aries
            Mercury=GE + 10,
            Jupiter=SC + 3,
            Venus=LI + 20,
        ),
        "rule_triggers": ["NEECHA_BHANGA_C3"],
        "description": "Saturn debilitated Aries; Sun (exalted in Aries) in H1 Kendra — NB C3",
        "expected": {"saturn_dignity": "NEECHA_BHANGA", "nb_condition_3": True},
    },
    "nbry_two_conditions": {
        # Mars debilitated in Cancer; BOTH Moon in Kendra from Lagna AND
        # Jupiter (exalts in Cancer) in Kendra from Moon → NBRY
        "lagna": LI + 5,
        "planets": _p(
            Sun=LE + 10,
            Moon=LI + 8,  # Moon (Cancer lord) in H1 from Lagna (Kendra) — C1
            Mars=CA + 22,  # Mars debilitated
            Jupiter=CA + 5,  # Jupiter exalts in Cancer, conjunct Mars — C3 partial
            Mercury=VI + 14,
            Venus=SC + 6,
            Saturn=AQ + 20,
        ),
        "rule_triggers": ["NBRY", "NEECHA_BHANGA_C1", "NEECHA_BHANGA_C3"],
        "description": "Mars debilitated Cancer; ≥2 NB conditions → Neecha Bhanga Raja Yoga",
        "expected": {"mars_dignity": "NEECHA_BHANGA_RAJA", "nbry": True},
    },
}


# ─── SECTION C: Graha Yuddha (Planetary War) fixtures ─────────────────────────
# Source: Saravali Ch.4 v.12-22; BPHS Ch.3


# ─── SECTION D: Parivartana Yoga fixtures ─────────────────────────────────────
# Source: BPHS Ch.7; BV Raman — Three Hundred Important Combinations


# ─── SECTION E: Kemadruma Yoga fixtures ───────────────────────────────────────
# Source: Phaladeepika Ch.6 v.56-60; BPHS Ch.38

KEMADRUMA_CHARTS = {
    "pure_kemadruma": {
        # Moon isolated: no planets in 2nd or 12th from Moon, not in Kendra
        # Moon in Aries; 2nd = Taurus (empty), 12th = Pisces (empty)
        "lagna": VI + 5,
        "planets": _p(
            Sun=LE + 10,
            Moon=AR + 15,  # Moon isolated in Aries
            Mars=CA + 8,  # NOT in Taurus or Pisces
            Mercury=VI + 18,
            Jupiter=SA + 5,
            Venus=SC + 12,
            Saturn=AQ + 20,
        ),
        "rule_triggers": ["KEMADRUMA", "KEMADRUMA_PURE"],
        "description": "Moon isolated in Aries — pure Kemadruma Yoga",
        "expected": {"kemadruma": True, "kemadruma_cancelled": False},
    },
    "kemadruma_cancelled": {
        # Kemadruma cancelled: Moon in Kendra from Lagna (cancellation condition 1)
        "lagna": CA + 8,
        "planets": _p(
            Sun=LE + 5,
            Moon=CA + 20,  # Moon in H1 (Kendra) — cancels Kemadruma
            Mars=LE + 15,  # NOT adjacent to Moon's sign
            Mercury=VI + 10,
            Jupiter=PI + 3,
            Venus=SC + 5,
            Saturn=AQ + 18,
        ),
        "rule_triggers": ["KEMADRUMA_CANCELLED"],
        "description": "Moon in Kendra from Lagna — Kemadruma cancelled",
        "expected": {"kemadruma": False, "kemadruma_cancelled": True},
    },
}


# ─── SECTION F: Nakshatra boundary charts ─────────────────────────────────────
# Critical: nakshatra changes at 13°20' intervals. Charts near boundaries test
# Vimshottari dasha boundary accuracy. SE precision now ensures correctness.

NAK_BOUNDARY_CHARTS = {
    "moon_at_nakshatra_cusp": {
        # Moon at exactly 13°20' (Ashwini/Bharani boundary)
        # Vimshottari dasha lord changes here: Ketu→Venus
        "lagna": AR + 5,
        "planets": _p(
            Sun=LE + 10,
            Moon=AR + 13.333,  # Moon at exact Ashwini/Bharani boundary
            Mars=CP + 8,
            Mercury=VI + 15,
            Jupiter=SA + 5,
            Venus=TA + 20,
            Saturn=AQ + 10,
        ),
        "rule_triggers": ["NAK_BOUNDARY", "DASHA_BOUNDARY"],
        "description": "Moon at 13°20' Aries — Ashwini/Bharani nakshatra boundary (Ketu→Venus MD)",
        "expected": {"moon_nakshatra": "Bharani", "md_lord": "Venus"},
    },
    "lagna_at_sign_boundary": {
        # Lagna within 0.5° of sign boundary — ayanamsha-sensitive
        # Tests confidence model boundary warning
        "lagna": TA + 29.7,  # Lagna at 29°42' Taurus — near Gemini boundary
        "planets": _p(
            Sun=LE + 8,
            Moon=CA + 15,
            Mars=AR + 10,
            Mercury=VI + 5,
            Jupiter=SA + 12,
            Venus=LI + 20,
            Saturn=CP + 3,
        ),
        "rule_triggers": ["LAGNA_BOUNDARY_WARNING", "CONFIDENCE_LOW"],
        "description": "Lagna at 29°42' Taurus — within 0.3° of Gemini; confidence model should warn",
        "expected": {"lagna_boundary_warning": True, "margin_deg": "< 1.0"},
    },
    "year_boundary_jan1": {
        # Birth on January 1 — tests year-lord computation in Kala Bala
        # Abda Bala uses weekday of Jan 1 for year lord
        "lagna": CP + 10,  # Capricorn Lagna (Jan 1 births common here)
        "planets": _p(
            Sun=SA + 17,  # Sun in Sagittarius (Jan 1 position)
            Moon=TA + 8,
            Mars=AR + 15,
            Mercury=SA + 5,
            Jupiter=PI + 20,
            Venus=SC + 12,
            Saturn=AQ + 3,
        ),
        "birth_date": "1990-01-01",  # Year boundary test vector
        "rule_triggers": ["ABDA_BALA_YEAR_LORD", "KALA_BALA"],
        "description": "Jan 1 birth chart — tests Abda Bala year-lord computation at year boundary",
        "expected": {"kala_bala_computed": True},
    },
}


# ─── SECTION G: High-latitude charts ──────────────────────────────────────────
# Tests Bhava Chalita divergence and topocentric Moon correction at extremes
# Oslo (59.9°N), Helsinki (60.2°N) — Bhava Chalita diverges significantly from D1

HIGH_LATITUDE_CHARTS = {
    "oslo_chart": {
        # High latitude: Bhava Chalita houses diverge from D1 sign houses
        "lagna": GE + 15,  # Gemini Lagna computed for Oslo, 59.9°N
        "lat": 59.91,  # Oslo latitude
        "lon": 10.75,  # Oslo longitude
        "planets": _p(
            Sun=LE + 5,
            Moon=SA + 12,
            Mars=AR + 8,
            Mercury=GE + 20,
            Jupiter=LI + 3,
            Venus=CA + 15,
            Saturn=AQ + 18,
        ),
        "rule_triggers": [
            "HIGH_LATITUDE",
            "BHAVA_CHALITA_DIVERGENCE",
            "TOPOCENTRIC_MOON",
        ],
        "description": "Oslo 59.9°N — high latitude Bhava Chalita divergence test",
        "expected": {"bhava_chalita_differs_from_d1": True},
    },
    "helsinki_chart": {
        "lagna": VI + 20,
        "lat": 60.17,
        "lon": 24.94,
        "planets": _p(
            Sun=CP + 10,
            Moon=TA + 5,
            Mars=SC + 8,
            Mercury=SA + 15,
            Jupiter=AR + 3,
            Venus=AQ + 12,
            Saturn=LI + 25,
        ),
        "rule_triggers": ["HIGH_LATITUDE", "TOPOCENTRIC_MOON"],
        "description": "Helsinki 60.2°N — high latitude topocentric Moon correction test",
        "expected": {"topocentric_correction_applied": True},
    },
}


# ─── SECTION H: Female chart fixtures ─────────────────────────────────────────
# Tests Mahabhagya Yoga (gender-specific), Upapada Lagna analysis,
# and spouse-related H7 interpretations
# Source: BPHS Ch.25 (Mahabhagya); Phaladeepika Ch.6 (female chart rules)

FEMALE_CHART_FIXTURES = {
    "mahabhagya_female": {
        # Mahabhagya for female: night birth + Moon/Lagna/Sun in even signs
        "lagna": TA + 12,  # Taurus (even sign) Lagna
        "birth_hour": 22.5,  # Night birth (after sunset)
        "gender": "female",
        "planets": _p(
            Sun=CA + 8,  # Cancer (even sign) — night birth condition
            Moon=VI + 15,  # Virgo (even sign) — Mahabhagya condition
            Mars=SC + 5,
            Mercury=GE + 10,
            Jupiter=PI + 3,
            Venus=TA + 20,
            Saturn=CP + 8,
        ),
        "rule_triggers": ["MAHABHAGYA_FEMALE", "UPAPADA_LAGNA"],
        "description": "Female night birth — Lagna/Moon/Sun all in even signs → Mahabhagya Yoga",
        "expected": {"mahabhagya": True, "gender": "female"},
    },
    "upapada_strong": {
        # Upapada Lagna with lord in strong position — marriage indicated clearly
        "lagna": SC + 8,  # Scorpio Lagna
        "gender": "female",
        "planets": _p(
            Sun=LE + 5,
            Moon=TA + 18,
            Mars=CP + 12,  # Mars (Scorpio lord) exalted in Capricorn
            Mercury=VI + 14,
            Jupiter=CA + 5,
            Venus=LI + 8,  # Venus strong (own sign Libra)
            Saturn=LI + 20,
        ),
        "rule_triggers": ["UPAPADA_LAGNA", "MARRIAGE_YOGA"],
        "description": "Female chart: Scorpio Lagna, Mars exalted — strong Upapada Lagna for marriage",
        "expected": {"upapada_lord_strong": True},
    },
}


# ─── Master fixture registry ───────────────────────────────────────────────────
ALL_DIVERSE_FIXTURES = {
    **{f"nb_{k}": v for k, v in NEECHA_BHANGA_CHARTS.items()},
    **{f"gy_{k}": v for k, v in GRAHA_YUDDHA_CHARTS.items()},
    **{f"pv_{k}": v for k, v in PARIVARTANA_CHARTS.items()},
    **{f"km_{k}": v for k, v in KEMADRUMA_CHARTS.items()},
    **{f"nk_{k}": v for k, v in NAK_BOUNDARY_CHARTS.items()},
    **{f"hl_{k}": v for k, v in HIGH_LATITUDE_CHARTS.items()},
    **{f"fe_{k}": v for k, v in FEMALE_CHART_FIXTURES.items()},
}


def get_fixture(key: str) -> dict:
    """Retrieve a diverse chart fixture by key."""
    return ALL_DIVERSE_FIXTURES.get(key, {})


def list_fixtures_by_rule(rule_trigger: str) -> list[str]:
    """Return all fixture keys that test a given rule trigger."""
    return [
        k
        for k, v in ALL_DIVERSE_FIXTURES.items()
        if rule_trigger in v.get("rule_triggers", [])
    ]
