"""Kundali Milan — Ashtakoot 36-point compatibility (Session 12)."""

from __future__ import annotations
from dataclasses import dataclass

NAKSHATRAS = [
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
_VARNA = {
    "Cancer": 0,
    "Scorpio": 0,
    "Pisces": 0,
    "Aries": 1,
    "Leo": 1,
    "Sagittarius": 1,
    "Taurus": 2,
    "Virgo": 2,
    "Capricorn": 2,
    "Gemini": 3,
    "Libra": 3,
    "Aquarius": 3,
}
_VARNA_NAMES = {0: "Brahmin", 1: "Kshatriya", 2: "Vaishya", 3: "Shudra"}
_VG = {
    "Aries": "q",
    "Taurus": "q",
    "Gemini": "h",
    "Cancer": "j",
    "Leo": "v",
    "Virgo": "h",
    "Libra": "h",
    "Scorpio": "k",
    "Sagittarius": "qh",
    "Capricorn": "jq",
    "Aquarius": "h",
    "Pisces": "j",
}
_VD = {
    "q": ["q", "j"],
    "h": ["q", "qh"],
    "j": ["j", "k"],
    "v": ["q"],
    "k": [],
    "qh": ["q", "h"],
    "jq": ["j", "q"],
}
_TS = {1: 3, 2: 3, 3: 0, 4: 3, 5: 0, 6: 3, 7: 0, 8: 3, 9: 3}
_Y = [
    "horse",
    "elephant",
    "goat",
    "serpent",
    "dog",
    "cat",
    "cat",
    "goat",
    "cat",
    "rat",
    "rat",
    "cow",
    "buffalo",
    "tiger",
    "buffalo",
    "tiger",
    "deer",
    "deer",
    "dog",
    "monkey",
    "mongoose",
    "monkey",
    "lion",
    "horse",
    "lion",
    "cow",
    "elephant",
]
_YE = {
    frozenset({"horse", "buffalo"}),
    frozenset({"elephant", "lion"}),
    frozenset({"goat", "monkey"}),
    frozenset({"serpent", "mongoose"}),
    frozenset({"dog", "deer"}),
    frozenset({"cat", "rat"}),
    frozenset({"tiger", "cow"}),
}
_SL = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}
_NF = {
    "Sun": {
        "Moon": "F",
        "Mars": "F",
        "Jupiter": "F",
        "Venus": "E",
        "Saturn": "E",
        "Mercury": "N",
    },
    "Moon": {
        "Sun": "F",
        "Mars": "N",
        "Jupiter": "F",
        "Venus": "F",
        "Saturn": "N",
        "Mercury": "F",
    },
    "Mars": {
        "Sun": "F",
        "Moon": "F",
        "Jupiter": "F",
        "Venus": "N",
        "Saturn": "N",
        "Mercury": "E",
    },
    "Mercury": {
        "Sun": "F",
        "Moon": "N",
        "Mars": "N",
        "Jupiter": "N",
        "Venus": "F",
        "Saturn": "F",
    },
    "Jupiter": {
        "Sun": "F",
        "Moon": "F",
        "Mars": "F",
        "Mercury": "E",
        "Venus": "E",
        "Saturn": "N",
    },
    "Venus": {
        "Sun": "E",
        "Moon": "N",
        "Mars": "N",
        "Mercury": "F",
        "Jupiter": "N",
        "Saturn": "F",
    },
    "Saturn": {
        "Sun": "E",
        "Moon": "E",
        "Mars": "N",
        "Mercury": "F",
        "Jupiter": "N",
        "Venus": "F",
    },
}
_GA = [
    "Deva",
    "Manava",
    "Rakshasa",
    "Deva",
    "Deva",
    "Manava",
    "Deva",
    "Deva",
    "Rakshasa",
    "Rakshasa",
    "Manava",
    "Manava",
    "Deva",
    "Rakshasa",
    "Deva",
    "Rakshasa",
    "Deva",
    "Rakshasa",
    "Rakshasa",
    "Manava",
    "Manava",
    "Deva",
    "Rakshasa",
    "Rakshasa",
    "Manava",
    "Deva",
    "Deva",
]
_GT = {
    ("Deva", "Deva"): 6.0,
    ("Deva", "Manava"): 6.0,
    ("Deva", "Rakshasa"): 0.0,
    ("Manava", "Deva"): 5.0,
    ("Manava", "Manava"): 6.0,
    ("Manava", "Rakshasa"): 0.0,
    ("Rakshasa", "Deva"): 1.0,
    ("Rakshasa", "Manava"): 0.0,
    ("Rakshasa", "Rakshasa"): 6.0,
}
_NA = [
    "Aadi",
    "Madhya",
    "Antya",
    "Antya",
    "Madhya",
    "Aadi",
    "Aadi",
    "Madhya",
    "Antya",
    "Antya",
    "Madhya",
    "Aadi",
    "Aadi",
    "Madhya",
    "Antya",
    "Antya",
    "Madhya",
    "Aadi",
    "Aadi",
    "Madhya",
    "Antya",
    "Antya",
    "Madhya",
    "Aadi",
    "Aadi",
    "Madhya",
    "Antya",
]
_MH = {1, 2, 4, 7, 8, 12}


def _ni(lon):
    return min(int(lon / (360 / 27)), 26)


def _ws(p, r):
    return (p - r) % 12 + 1


def _vs(ms, fs):
    return 1.0 if _VARNA.get(ms, 3) <= _VARNA.get(fs, 3) else 0.0


def _vash(ms, fs):
    mg = _VG.get(ms, "h")
    fg = _VG.get(fs, "h")
    if mg == fg:
        return 2.0
    if fg in _VD.get(mg, []):
        return 2.0
    if mg in _VD.get(fg, []):
        return 1.0
    return 0.0


def _ta(m, f):
    fw = ((f - m) % 27) + 1
    rv = ((m - f) % 27) + 1
    return min(3.0, (_TS[((fw - 1) % 9) + 1] + _TS[((rv - 1) % 9) + 1]) / 2.0)


def _yo(m, f):
    my = _Y[m]
    fy = _Y[f]
    return 4.0 if my == fy else (0.0 if frozenset({my, fy}) in _YE else 2.0)


def _gm(ms, fs):
    ml = _SL.get(ms, "Mercury")
    fl = _SL.get(fs, "Mercury")
    if ml == fl:
        return 5.0
    mf = _NF.get(ml, {}).get(fl, "N")
    fm = _NF.get(fl, {}).get(ml, "N")
    if mf == "F" and fm == "F":
        return 5.0
    if mf == "F" or fm == "F":
        return 4.0
    if mf == "N" and fm == "N":
        return 3.0
    if mf == "E" and fm == "E":
        return 0.0
    return 1.0


def _gn(m, f):
    return _GT.get((_GA[m], _GA[f]), 0.0)


def _bh(m, f):
    m2f = (f - m) % 12 + 1
    f2m = (m - f) % 12 + 1
    return 0.0 if m2f in (5, 6, 8, 9) or f2m in (5, 6, 8, 9) else 7.0


def _nd(m, f):
    return 0.0 if _NA[m] == _NA[f] else 8.0


def _bn(m, f):
    m2f = (f - m) % 12 + 1
    f2m = (m - f) % 12 + 1
    if m2f in (6, 8) or f2m in (6, 8):
        return "6/8 Bhakut Dosha"
    if m2f in (5, 9) or f2m in (5, 9):
        return "5/9 Bhakut Dosha"
    return ""


def has_mangal_dosha(c) -> bool:
    ms = c.planets["Mars"].sign_index
    for r in (
        c.lagna_sign_index,
        c.planets["Moon"].sign_index,
        c.planets["Venus"].sign_index,
    ):
        if _ws(ms, r) in _MH:
            return True
    return False


def _grade(s):
    return "Excellent" if s >= 28 else "Good" if s >= 18 else "Weak"


@dataclass
class KootaScore:
    name: str
    max_score: float
    score: float
    male_value: str
    female_value: str
    note: str = ""

    @property
    def percentage(self):
        return self.score / self.max_score * 100 if self.max_score else 0.0

    @property
    def is_dosha(self):
        return self.score == 0.0 and self.max_score > 0


@dataclass
class KundaliMilanResult:
    total_score: float
    max_score: float
    percentage: float
    grade: str
    kootas: dict
    mangal_dosha_male: bool
    mangal_dosha_female: bool
    dosha_cancelled: bool
    nadi_dosha: bool
    bhakut_dosha: bool
    critical_doshas: list


def compute_kundali_milan(cm, cf):
    ml = cm.planets["Moon"].longitude
    fl = cf.planets["Moon"].longitude
    mn = _ni(ml)
    fn = _ni(fl)
    ms = cm.planets["Moon"].sign
    fs = cf.planets["Moon"].sign
    msi = cm.planets["Moon"].sign_index
    fsi = cf.planets["Moon"].sign_index
    v = _vs(ms, fs)
    va = _vash(ms, fs)
    t = _ta(mn, fn)
    y = _yo(mn, fn)
    gm = _gm(ms, fs)
    g = _gn(mn, fn)
    b = _bh(msi, fsi)
    n = _nd(mn, fn)
    total = v + va + t + y + gm + g + b + n
    ks = {
        "Varna": KootaScore(
            "Varna",
            1.0,
            v,
            _VARNA_NAMES.get(_VARNA.get(ms, 3), "?"),
            _VARNA_NAMES.get(_VARNA.get(fs, 3), "?"),
        ),
        "Vashya": KootaScore("Vashya", 2.0, va, _VG.get(ms, "?"), _VG.get(fs, "?")),
        "Tara": KootaScore("Tara", 3.0, t, NAKSHATRAS[mn], NAKSHATRAS[fn]),
        "Yoni": KootaScore("Yoni", 4.0, y, _Y[mn], _Y[fn]),
        "Graha Maitri": KootaScore(
            "Graha Maitri", 5.0, gm, _SL.get(ms, "?"), _SL.get(fs, "?")
        ),
        "Gana": KootaScore("Gana", 6.0, g, _GA[mn], _GA[fn]),
        "Bhakut": KootaScore("Bhakut", 7.0, b, ms, fs, _bn(msi, fsi)),
        "Nadi": KootaScore(
            "Nadi", 8.0, n, _NA[mn], _NA[fn], "Nadi Dosha" if n == 0.0 else ""
        ),
    }
    nd = n == 0.0
    bd = b == 0.0
    mm = has_mangal_dosha(cm)
    fm = has_mangal_dosha(cf)
    cc = mm and fm
    crit = []
    if nd:
        crit.append("Nadi Dosha")
    if bd:
        crit.append("Bhakut Dosha")
    if mm and not cc:
        crit.append("Mangal Dosha (Male)")
    if fm and not cc:
        crit.append("Mangal Dosha (Female)")
    return KundaliMilanResult(
        round(total, 2),
        36.0,
        round(total / 36 * 100, 1),
        _grade(total),
        ks,
        mm,
        fm,
        cc,
        nd,
        bd,
        crit,
    )
