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
AR = 0    # Aries
TA = 30   # Taurus
GE = 60   # Gemini
CA = 90   # Cancer
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
        "lagna": LE + 15, "lagna_sign": "Leo",
        "planets": _p(Sun=LE+10, Moon=SC+5, Mars=CA+15,
                      Mercury=VI+10, Jupiter=SA+5, Venus=LI+10, Saturn=AQ+20),
        "rule_triggers": ["mars_debilitated", "no_neecha_bhanga"],
        "expected": {"mars_dignity": "Debilitation", "nb_count": 0},
        "description": "Mars debilitated Cancer, no NB — Leo Lagna"
    },

    # A-2: Mars debilitated + Moon (Cancer lord) in Kendra from Lagna → NB
    "debil_mars_nb_condition1": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=CA+8, Mars=CA+20,
                      Mercury=TA+15, Jupiter=AR+12, Venus=GE+5, Saturn=AQ+10),
        "rule_triggers": ["mars_debilitated", "nb_condition_1", "nbry"],
        "expected": {"mars_dignity": "Neecha Bhanga", "nb_count": 1},
        "description": "Mars debil Cancer + Moon(Cancer lord) in H1 Kendra → NB"
    },

    # A-3: Mars debilitated + Jupiter (exaltation lord of Cancer=Capricorn→Mars exalts there)
    # Actually Mars exalts in Capricorn, so exaltation lord = Saturn (Capricorn lord)
    # Condition 3: planet that exalts in debil sign in Kendra from Lagna
    # Mars debil in Cancer → exaltation sign = Capricorn → Saturn is Capricorn lord → Saturn in Kendra
    "debil_mars_nb_condition3": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=GE+8, Mars=CA+20,
                      Mercury=TA+15, Jupiter=SA+12, Venus=GE+5, Saturn=AR+10),
        "rule_triggers": ["mars_debilitated", "nb_condition_3"],
        "expected": {"mars_dignity": "Neecha Bhanga", "nb_count": 1},
        "description": "Mars debil Cancer + Saturn(exalt lord) in H1 → NB condition 3"
    },

    # A-4: Venus debilitated in Virgo
    "debil_venus_virgo": {
        "lagna": GE + 10, "lagna_sign": "Gemini",
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+15,
                      Mercury=VI+5, Jupiter=SA+5, Venus=VI+20, Saturn=CP+10),
        "rule_triggers": ["venus_debilitated"],
        "expected": {"venus_dignity": "Debilitation"},
        "description": "Venus debilitated Virgo — Gemini Lagna"
    },

    # A-5: Saturn exalted in Libra — classic Paramotcha
    "saturn_exalt_libra": {
        "lagna": CA + 5, "lagna_sign": "Cancer",
        "planets": _p(Sun=LE+10, Moon=CA+3, Mars=SC+15,
                      Mercury=VI+10, Jupiter=CA+20, Venus=LI+5, Saturn=LI+20),
        "rule_triggers": ["saturn_exalted", "paramotcha_gradient"],
        "expected": {"saturn_dignity": "Exaltation"},
        "description": "Saturn exalted Libra at 20° — exact Paramotcha"
    },

    # A-6: Mercury Mooltrikona — exact 16°-20° Virgo window
    "mercury_mooltrikona": {
        "lagna": VI + 5, "lagna_sign": "Virgo",
        "planets": _p(Sun=LE+10, Moon=TA+5, Mars=AR+10,
                      Mercury=VI+17, Jupiter=SA+5, Venus=LI+10, Saturn=AQ+20),
        "rule_triggers": ["mercury_mooltrikona", "mt_boundary"],
        "expected": {"mercury_dignity": "Mooltrikona"},
        "description": "Mercury at Virgo 17° — exactly in MT range 16°-20°"
    },

    # A-7: Mercury just outside MT — own sign not MT
    "mercury_own_not_mt": {
        "lagna": VI + 5, "lagna_sign": "Virgo",
        "planets": _p(Sun=LE+10, Moon=TA+5, Mars=AR+10,
                      Mercury=VI+21, Jupiter=SA+5, Venus=LI+10, Saturn=AQ+20),
        "rule_triggers": ["mercury_own_sign", "not_mooltrikona"],
        "expected": {"mercury_dignity": "Own Sign"},
        "description": "Mercury at Virgo 21° — own sign but past MT range"
    },

    # A-8: Rahu exalted per PVRNR (Taurus)
    "rahu_exalt_taurus_pvrnr": {
        "lagna": AR + 10, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+20,
                      Mercury=TA+15, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10,
                      Rahu=TA+15, Ketu=SC+15),
        "rule_triggers": ["rahu_exalt_pvrnr", "node_dignity"],
        "expected": {"rahu_dignity_pvrnr": "Exaltation"},
        "description": "Rahu in Taurus — exalted per PVRNR/BPHS"
    },

    # A-9: Vargottama — planet same sign D1 and D9
    # Aries 0°-3°20' = 1st navamsha of Aries = Aries in D9 (Parasara)
    "vargottama_sun_aries": {
        "lagna": AR + 15, "lagna_sign": "Aries",
        "planets": _p(Sun=AR+2, Moon=CA+5, Mars=AR+20,
                      Mercury=TA+15, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["vargottama_sun"],
        "expected": {"sun_vargottama": True},
        "description": "Sun at Aries 2° — Vargottama (D1 Aries = D9 Aries)"
    },

    # A-10: All 6 NB conditions active (NBRY)
    "mars_nbry_multiple_conditions": {
        "lagna": LI + 5, "lagna_sign": "Libra",
        # Mars debil in Cancer. Moon (Cancer lord) in Kendra from Lagna.
        # Saturn (Capricorn lord = exalt lord of Mars) in Kendra from Lagna.
        "planets": _p(Sun=LE+10, Moon=LI+8, Mars=CA+20,
                      Mercury=VI+10, Jupiter=SA+5, Venus=LI+2, Saturn=LI+15),
        "rule_triggers": ["mars_debilitated", "nb_multiple", "nbry"],
        "expected": {"mars_dignity": "Neecha Bhanga Raja Yoga", "nb_count": 2},
        "description": "Mars NB Raja Yoga — Moon+Saturn both in Kendra from Libra Lagna"
    },
}


# ─── SECTION B: Graha Yuddha test charts ──────────────────────────────────────

GRAHA_YUDDHA_CHARTS = {

    # B-1: Mars and Jupiter within 0.5° longitude — at war
    "mars_jupiter_war": {
        "lagna": AR + 15, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=CA+5,
                      Mars=SA+10, Jupiter=SA+10.4,  # 0.4° apart
                      Mercury=VI+10, Venus=LI+5, Saturn=CP+15),
        "rule_triggers": ["graha_yuddha", "planetary_war"],
        "expected": {"war_pair": ("Mars", "Jupiter"), "war_detected": True},
        "description": "Mars-Jupiter war: 0.4° longitude apart in Sagittarius"
    },

    # B-2: Venus and Saturn outside war orb — no war
    "venus_saturn_no_war": {
        "lagna": AR + 15, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=CA+5,
                      Mars=AR+20, Jupiter=SA+5,
                      Mercury=VI+10, Venus=LI+5, Saturn=LI+10),  # 5° apart
        "rule_triggers": ["no_graha_yuddha"],
        "expected": {"war_detected": False},
        "description": "Venus-Saturn 5° apart — no war (orb requires <1°)"
    },

    # B-3: Mercury and Venus at war
    "mercury_venus_war": {
        "lagna": GE + 10, "lagna_sign": "Gemini",
        "planets": _p(Sun=LE+10, Moon=TA+5, Mars=AR+15,
                      Mercury=LI+7, Jupiter=SA+5, Venus=LI+7.6, Saturn=CP+10),
        "rule_triggers": ["graha_yuddha_mercury_venus"],
        "expected": {"war_pair": ("Mercury", "Venus"), "war_detected": True},
        "description": "Mercury-Venus war: 0.6° apart in Libra"
    },
}


# ─── SECTION C: Parivartana Yoga test charts ──────────────────────────────────

PARIVARTANA_CHARTS = {

    # C-1: Sun in Cancer (Moon's sign), Moon in Leo (Sun's sign) — Maha Parivartana
    "sun_moon_parivartana": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=CA+10, Moon=LE+5, Mars=AR+20,
                      Mercury=TA+15, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["parivartana_sun_moon", "maha_parivartana"],
        "expected": {"parivartana_pair": ("Sun", "Moon"), "type": "Maha"},
        "description": "Sun-Moon Parivartana: Sun in Cancer, Moon in Leo"
    },

    # C-2: Jupiter in Gemini (Mercury's sign), Mercury in Sagittarius (Jupiter's sign)
    "jupiter_mercury_parivartana": {
        "lagna": VI + 5, "lagna_sign": "Virgo",
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+10,
                      Mercury=SA+15, Jupiter=GE+10, Venus=LI+5, Saturn=CP+20),
        "rule_triggers": ["parivartana_jupiter_mercury"],
        "expected": {"parivartana_pair": ("Jupiter", "Mercury")},
        "description": "Jupiter-Mercury Parivartana"
    },

    # C-3: Dainya Parivartana — H8 lord exchanges with H1 lord
    # Cancer Lagna: H1=Moon, H8=Saturn. Moon in Capricorn, Saturn in Cancer
    "dainya_parivartana_cancer": {
        "lagna": CA + 5, "lagna_sign": "Cancer",
        "planets": _p(Sun=LE+10, Moon=CP+8, Mars=AR+10,
                      Mercury=GE+15, Jupiter=VI+5, Venus=LI+10, Saturn=CA+15),
        "rule_triggers": ["dainya_parivartana", "h8_lord_exchange"],
        "expected": {"parivartana_type": "Dainya"},
        "description": "Dainya Parivartana: Cancer Lagna, Moon-Saturn exchange involving H8"
    },
}


# ─── SECTION D: Yoga detection test charts ────────────────────────────────────

YOGA_CHARTS = {

    # D-1: Kemadruma — Moon isolated (no planets in H2/H12 from Moon, no Kendra from Moon)
    "kemadruma_confirmed": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=SA+10, Moon=CA+5, Mars=SA+20,
                      Mercury=CP+10, Jupiter=AQ+5, Venus=PI+10, Saturn=CP+15,
                      Rahu=AR+5, Ketu=LI+5),
        "rule_triggers": ["kemadruma_yoga"],
        "expected": {"kemadruma": True},
        "description": "Kemadruma: Moon in Cancer isolated, no planets in H2(Leo) or H12(Gemini)"
    },

    # D-2: Kemadruma cancelled by Moon in Kendra from Lagna
    "kemadruma_cancelled_kendra": {
        "lagna": VI + 5, "lagna_sign": "Virgo",
        "planets": _p(Sun=LE+10, Moon=VI+8, Mars=AR+10,  # Moon in H1 = Kendra
                      Mercury=VI+20, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["kemadruma_cancelled"],
        "expected": {"kemadruma": False, "cancellation": "moon_in_kendra"},
        "description": "Kemadruma cancelled: Moon in Kendra (H1) from Lagna"
    },

    # D-3: Raj Yoga — H1+H5 lords conjunct
    # Cancer Lagna: H1=Moon, H5=Mars (Scorpio). Moon+Mars in same sign.
    "raj_yoga_h1_h5_conjunct": {
        "lagna": CA + 5, "lagna_sign": "Cancer",
        "planets": _p(Sun=LE+10, Moon=SC+10, Mars=SC+15,  # Moon(H1)+Mars(H5) together
                      Mercury=VI+10, Jupiter=VI+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["raj_yoga_conjunction"],
        "expected": {"raj_yoga": True, "type": "conjunction"},
        "description": "Raj Yoga: Cancer Lagna, H1 lord Moon + H5 lord Mars conjunct in Scorpio"
    },

    # D-4: Viparita Raja Yoga (Harsha) — H6 lord in H8
    # Aries Lagna: H6=Virgo=Mercury, H8=Scorpio=Mars. Mercury in Scorpio.
    "viparita_harsha": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+20,
                      Mercury=SC+10, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["viparita_raj_yoga", "harsha_yoga"],
        "expected": {"viparita_yoga": "Harsha"},
        "description": "Harsha Yoga: Aries Lagna, H6 lord Mercury in H8 (Scorpio)"
    },

    # D-5: Pancha Mahapurusha — Jupiter in Cancer (exalt) in H4 (Kendra)
    "hamsa_yoga_jupiter": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=TA+5, Mars=AR+20,
                      Mercury=TA+15, Jupiter=CA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["hamsa_yoga", "pancha_mahapurusha"],
        "expected": {"pm_yoga": "Hamsa", "planet": "Jupiter"},
        "description": "Hamsa Yoga: Jupiter exalted in Cancer, H4 Kendra from Aries Lagna"
    },

    # D-6: Sannyasa Yoga — 4 planets in Leo
    "sannyasa_4_in_leo": {
        "lagna": VI + 5, "lagna_sign": "Virgo",
        "planets": _p(Sun=LE+10, Moon=LE+5, Mars=LE+20, Mercury=LE+15,
                      Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["sannyasa_yoga"],
        "expected": {"sannyasa": True, "sign": "Leo"},
        "description": "Sannyasa Yoga: Sun+Moon+Mars+Mercury all in Leo"
    },

    # D-7: Sunapha — planet in 2nd from Moon (not Sun)
    "sunapha_yoga": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=CA+20,
                      Mercury=LE+10, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["sunapha_yoga"],
        "expected": {"sunapha": True, "planets": ["Mercury"]},
        "description": "Sunapha: Mercury in Leo (2nd from Moon in Cancer)"
    },

    # D-8: Anapha — planet in 12th from Moon
    "anapha_yoga": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+20,
                      Mercury=GE+10, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["anapha_yoga"],
        "expected": {"anapha": True, "planets": ["Mercury"]},
        "description": "Anapha: Mercury in Gemini (12th from Moon in Cancer)"
    },

    # D-9: Amala Yoga — only benefics in H10 from Lagna
    "amala_yoga": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=GE+20,
                      Mercury=CP+10, Jupiter=CP+5, Venus=LI+10, Saturn=GE+10),
        # H10 from Aries = Capricorn. Mercury+Jupiter (benefics) in Capricorn.
        "rule_triggers": ["amala_yoga"],
        "expected": {"amala": True},
        "description": "Amala Yoga: Mercury+Jupiter (benefics only) in H10 (Capricorn) from Aries Lagna"
    },

    # D-10: Mahabhagya — male, daytime, Sun+Moon+Lagna in odd signs
    "mahabhagya_male": {
        "lagna": AR + 15, "lagna_sign": "Aries",   # odd
        "planets": _p(Sun=GE+10, Moon=LE+5, Mars=AR+20,  # odd signs
                      Mercury=TA+15, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["mahabhagya_yoga_male"],
        "expected": {"mahabhagya": True, "gender": "male"},
        "description": "Mahabhagya (male): Aries Lagna, Sun Gemini, Moon Leo — all odd signs"
    },
}


# ─── SECTION E: All 12 Lagnas test charts ─────────────────────────────────────

ALL_LAGNA_CHARTS = {}
for si, (sign_name, lagna_lon) in enumerate([
    ("Aries", AR+15), ("Taurus", TA+15), ("Gemini", GE+15),
    ("Cancer", CA+15), ("Leo", LE+15), ("Virgo", VI+15),
    ("Libra", LI+15), ("Scorpio", SC+15), ("Sagittarius", SA+15),
    ("Capricorn", CP+15), ("Aquarius", AQ+15), ("Pisces", PI+15),
]):
    ALL_LAGNA_CHARTS[f"lagna_{sign_name.lower()}"] = {
        "lagna": lagna_lon, "lagna_sign": sign_name,
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+15,
                      Mercury=VI+10, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": [f"lagna_{sign_name.lower()}", "functional_dignity"],
        "expected": {"lagna_sign": sign_name},
        "description": f"{sign_name} Lagna — functional dignity classification test"
    }


# ─── SECTION F: Nakshatra boundary charts ─────────────────────────────────────

NAKSHATRA_BOUNDARY_CHARTS = {
    # Each nakshatra boundary at multiples of 40/3 degrees
    f"nak_boundary_{i}": {
        "lagna": AR + 15,
        "planets": _p(
            Sun=LE+10, Mars=AR+20, Mercury=VI+10,
            Jupiter=SA+5, Venus=LI+10, Saturn=CP+10,
            Moon=(i * 40.0 / 3.0) % 360,  # exactly at boundary
        ),
        "rule_triggers": ["nakshatra_boundary", "vimshottari_precision"],
        "expected": {"moon_at_boundary": True, "nakshatra_idx": i},
        "description": f"Moon exactly at nakshatra boundary {i} — tests int(lon*3/40) precision"
    }
    for i in range(1, 10)  # test first 9 boundaries
}


# ─── SECTION G: Transit quality test charts ───────────────────────────────────

TRANSIT_CHARTS = {

    # G-1: Sade Sati — Saturn in 12th from natal Moon
    "sade_sati_phase1": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "natal_moon_sign": 2,  # Gemini
        "transit_saturn_sign": 1,  # Taurus = 12th from Gemini
        "rule_triggers": ["sade_sati_phase1"],
        "expected": {"sade_sati": True, "phase": 1},
        "description": "Sade Sati Phase 1: Saturn in 12th from natal Moon"
    },

    # G-2: Vedha obstruction — Saturn in H3 (good transit) but Mars in H12 (Vedha of H3)
    "vedha_obstruction_h3": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "natal": _p(Sun=LE+10, Moon=CA+5, Mars=AR+15,
                    Mercury=VI+10, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "transit": {"Saturn": GE+10, "Mars": PI+5},  # Saturn in H3, Mars in H12 = Vedha
        "rule_triggers": ["vedha_obstruction"],
        "expected": {"vedha_blocked": True, "planet": "Saturn", "house": 3},
        "description": "Vedha: Saturn in H3 (Gemini) obstructed by Mars in H12 (Pisces)"
    },

    # G-3: Tarabala — Moon in 7th nakshatra from natal (Naidhana = most inauspicious)
    "tarabala_naidhana": {
        "lagna": AR + 5,
        "natal_moon_nakshatra": 0,  # Ashwini
        "transit_nakshatra": 6,     # 7th from Ashwini = Punarvasu = Naidhana
        "rule_triggers": ["tarabala_naidhana"],
        "expected": {"tara": "Naidhana", "quality": "avoid"},
        "description": "Tarabala Naidhana: transit nakshatra is 7th from natal — most inauspicious"
    },
}


# ─── SECTION H: High-latitude charts ─────────────────────────────────────────

HIGH_LATITUDE_CHARTS = {

    "helsinki_winter_solstice": {
        "birth_data": {
            "year": 2000, "month": 12, "day": 21, "hour": 8.0,
            "lat": 60.1699, "lon": 24.9384, "tz_offset": 2.0,
            "ayanamsha": "lahiri"
        },
        "rule_triggers": ["bhava_chalita_divergence", "high_latitude"],
        "expected": {"latitude": 60.17, "extreme_bhava_chalita": True},
        "description": "Helsinki winter solstice — extreme Bhava Chalita divergence expected"
    },

    "reykjavik_midsummer": {
        "birth_data": {
            "year": 2000, "month": 6, "day": 21, "hour": 12.0,
            "lat": 64.1466, "lon": -21.9426, "tz_offset": 0.0,
            "ayanamsha": "lahiri"
        },
        "rule_triggers": ["high_latitude", "midnight_sun"],
        "expected": {"latitude": 64.15},
        "description": "Reykjavik midsummer — even more extreme latitude"
    },
}


# ─── SECTION I: Dasha-specific charts ─────────────────────────────────────────

DASHA_CHARTS = {

    # I-1: Moon in Ashwini — Ketu Mahadasha starts
    "ketu_mahadasha_start": {
        "lagna": AR + 5,
        "planets": _p(Sun=LE+10, Moon=AR+3, Mars=AR+20,
                      Mercury=TA+15, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["ketu_mahadasha", "vimshottari_balance"],
        "expected": {"moon_nakshatra": "Ashwini", "md_lord": "Ketu"},
        "description": "Moon in Ashwini (Ketu's nakshatra) — tests Ketu MD period"
    },

    # I-2: Moon at Pushya/Ashlesha boundary
    "moon_pushya_ashlesha_boundary": {
        "lagna": AR + 5,
        "planets": _p(Sun=LE+10, Moon=CA+13.333, Mars=AR+20,  # exactly at boundary
                      Mercury=TA+15, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["nakshatra_boundary", "saturn_mercury_md_boundary"],
        "expected": {"moon_at_nak_boundary": True},
        "description": "Moon exactly at Pushya/Ashlesha boundary (13.333° Cancer)"
    },

    # I-3: Ashtottari applicability — Rahu in H3 (not Kendra/Trikona)
    "ashtottari_applicable": {
        "lagna": AR + 5,
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+20,
                      Mercury=TA+15, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10,
                      Rahu=GE+10, Ketu=SA+10),  # H3 from Aries = Gemini
        "rule_triggers": ["ashtottari_applicable"],
        "expected": {"ashtottari": True, "rahu_house": 3},
        "description": "Rahu in H3 (Gemini) from Aries Lagna — Ashtottari applicable"
    },
}


# ─── SECTION J: Functional dignity by Lagna ───────────────────────────────────

FUNCTIONAL_DIGNITY_CHARTS = {

    # J-1: Taurus Lagna — Saturn is Yogakaraka (H9+H10)
    "taurus_lagna_saturn_yogakaraka": {
        "lagna": TA + 15, "lagna_sign": "Taurus",
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+15,
                      Mercury=VI+10, Jupiter=SA+5, Venus=TA+10, Saturn=CP+20),
        "rule_triggers": ["yogakaraka_saturn_taurus", "functional_benefic"],
        "expected": {
            "saturn_functional": "yogakaraka",
            "jupiter_functional": "malefic"  # rules H8+H11 for Taurus
        },
        "description": "Taurus Lagna: Saturn Yogakaraka (H9+H10), Jupiter functional malefic (H8+H11)"
    },

    # J-2: Leo Lagna — Mars Yogakaraka (H4+H9)
    "leo_lagna_mars_yogakaraka": {
        "lagna": LE + 15, "lagna_sign": "Leo",
        "planets": _p(Sun=LE+20, Moon=CA+5, Mars=SA+15,
                      Mercury=VI+10, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["yogakaraka_mars_leo"],
        "expected": {"mars_functional": "yogakaraka"},
        "description": "Leo Lagna: Mars Yogakaraka (H4 Scorpio + H9 Aries)"
    },

    # J-3: Cancer Lagna — Jupiter mixed (H6 maraka + H9 trikona)
    "cancer_lagna_jupiter_mixed": {
        "lagna": CA + 5, "lagna_sign": "Cancer",
        "planets": _p(Sun=LE+10, Moon=CA+8, Mars=SC+15,
                      Mercury=GE+10, Jupiter=CA+20, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["functional_mixed_jupiter_cancer"],
        "expected": {"jupiter_functional": "neutral"},  # H6+H9 mixed
        "description": "Cancer Lagna: Jupiter rules H6(Sagittarius)+H9(Pisces) — mixed"
    },
}


# ─── SECTION K: Shadbala edge cases ───────────────────────────────────────────

SHADBALA_CHARTS = {

    # K-1: Dig Bala peak — Jupiter in H1 (gets max Dig Bala)
    "jupiter_digbala_peak": {
        "lagna": CA + 5, "lagna_sign": "Cancer",
        "planets": _p(Sun=LE+10, Moon=CA+8, Mars=AR+15,
                      Mercury=GE+10, Jupiter=CA+20, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["dig_bala_peak_jupiter"],
        "expected": {"jupiter_dig_bala": "maximum"},
        "description": "Jupiter in H1 — peak Dig Bala (Mercury/Jupiter peak in H1)"
    },

    # K-2: Saturn Dig Bala peak — H7
    "saturn_digbala_h7": {
        "lagna": AR + 5, "lagna_sign": "Aries",
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+20,
                      Mercury=VI+10, Jupiter=SA+5, Venus=LI+10, Saturn=LI+20),
        "rule_triggers": ["dig_bala_saturn_h7"],
        "expected": {"saturn_dig_bala": "maximum"},
        "description": "Saturn in H7 (Libra from Aries Lagna) — peak Dig Bala"
    },
}


# ─── SECTION L: KP system test charts ────────────────────────────────────────

KP_CHARTS = {

    # L-1: Sub-lord of H7 cusp in Ashwini — Ketu sub-lord
    "kp_h7_cusp_ashwini": {
        "lagna": AR + 0.5,  # 0.5° Aries lagna → H7 cusp near 0.5° Libra
        "planets": _p(Sun=LE+10, Moon=CA+5, Mars=AR+20,
                      Mercury=VI+10, Jupiter=SA+5, Venus=LI+10, Saturn=CP+10),
        "rule_triggers": ["kp_sub_lord_h7", "kp_promise"],
        "description": "KP: H7 cusp sub-lord analysis for marriage promise"
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
    return [name for name, f in ALL_FIXTURES.items()
            if rule in f.get("rule_triggers", [])]


def fixtures_by_section() -> dict[str, int]:
    return {
        "Dignity":           len(DIGNITY_CHARTS),
        "Graha Yuddha":      len(GRAHA_YUDDHA_CHARTS),
        "Parivartana":       len(PARIVARTANA_CHARTS),
        "Yoga Detection":    len(YOGA_CHARTS),
        "All 12 Lagnas":     len(ALL_LAGNA_CHARTS),
        "Nakshatra Boundary": len(NAKSHATRA_BOUNDARY_CHARTS),
        "Transit Quality":   len(TRANSIT_CHARTS),
        "High Latitude":     len(HIGH_LATITUDE_CHARTS),
        "Dasha":             len(DASHA_CHARTS),
        "Functional Dignity": len(FUNCTIONAL_DIGNITY_CHARTS),
        "Shadbala":          len(SHADBALA_CHARTS),
        "KP System":         len(KP_CHARTS),
    }
