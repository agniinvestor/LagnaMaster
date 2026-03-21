"""
src/calculations/yogas_pvrnr.py — Session 62

Yogas from PVRNR Ch.11 not covered in existing modules.
All grounded in textbook p125-145.

Public API
----------
  detect_pvrnr_yogas(chart, dashas, on_date) -> list[PVRNRYoga]
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

_NAT_BENEF = {"Jupiter","Venus","Mercury","Moon"}
_NAT_MALEF = {"Sun","Mars","Saturn","Rahu","Ketu"}
_KENDRA = {1,4,7,10}
_TRIKONA = {1,5,9}
_STRONG = _KENDRA | _TRIKONA


@dataclass
class PVRNRYoga:
    name: str
    present: bool
    score: float
    weighted_score: float
    description: str
    source: str
    dasha_weight: float


def _dasha_wt(planets, dashas, on_date):
    if not dashas: return 0.5
    try:
        from src.calculations.vimshottari_dasa import current_dasha
        md, ad = current_dasha(dashas, on_date)
        return 1.0 if any(p in {md.lord, ad.lord} for p in planets) else 0.5
    except Exception:
        return 0.5


def detect_pvrnr_yogas(chart, dashas=None, on_date: date | None = None) -> list[PVRNRYoga]:
    if on_date is None: on_date = date.today()
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    ph = hmap.planet_house
    results = []

    def y(name, planets, present, score, desc, src):
        dw = _dasha_wt(planets, dashas, on_date)
        results.append(PVRNRYoga(name=name, present=present, score=score,
            weighted_score=round(score*dw,2), description=desc, source=src, dasha_weight=dw))

    # Guru-Mangala Yoga (p125): Jupiter + Mars conjunct or 7th from each other
    jup_h = ph.get("Jupiter",0); mar_h = ph.get("Mars",0)
    guru_mangala = jup_h > 0 and mar_h > 0 and abs(jup_h-mar_h) in {0,6}
    y("Guru-Mangala Yoga",["Jupiter","Mars"],guru_mangala,
      2.0 if guru_mangala else 0.0,
      "Jupiter and Mars conjunct or 7th — righteous, energetic, dharmic","PVRNR p125")

    # Amala Yoga (p125): only natural benefics in H10 from lagna or Moon
    ph.get(hmap.house_lord[9], 0)
    h10_planets = [p for p in chart.planets if ph.get(p) == 10]
    moon_h = ph.get("Moon",0)
    h10_from_moon = ((moon_h + 9 - 1) % 12) + 1 if moon_h else 0
    h10m_planets = [p for p in chart.planets if ph.get(p) == h10_from_moon]
    amala_lagna = h10_planets and all(p in _NAT_BENEF for p in h10_planets)
    amala_moon = h10m_planets and all(p in _NAT_BENEF for p in h10m_planets)
    amala = amala_lagna or amala_moon
    y("Amala Yoga",list(_NAT_BENEF),amala,2.5 if amala else 0.0,
      "Only benefics in H10 from lagna or Moon — everlasting fame, virtuous","PVRNR p125")

    # Sankha Yoga (p126): (Lagnesh strong) + (5th/6th lords mutual kendra)
    lagnesh = hmap.house_lord[0]
    lord5 = hmap.house_lord[4]; lord6 = hmap.house_lord[5]
    l5h = ph.get(lord5,0); l6h = ph.get(lord6,0)
    mutual_kendra_56 = l5h > 0 and l6h > 0 and abs(l5h-l6h) % 12 in {0,3,6,9}
    lagnesh_strong = ph.get(lagnesh,0) in _STRONG
    sankha = lagnesh_strong and mutual_kendra_56
    y("Sankha Yoga",[lagnesh,lord5,lord6],sankha,2.5 if sankha else 0.0,
      "Lagnesh strong + 5th/6th lords in mutual kendra — blessed with wealth, pious","PVRNR p126")

    # Vasumati Yoga (p128): benefics in upachaya houses (3,6,10,11)
    upachaya = {3,6,10,11}
    upachaya_benefics = [p for p in _NAT_BENEF if ph.get(p,0) in upachaya]
    vasumati = len(upachaya_benefics) >= 2
    y("Vasumati Yoga",list(upachaya_benefics),vasumati,
      1.5*len(upachaya_benefics) if vasumati else 0.0,
      f"Benefics {upachaya_benefics} in upachaya houses — wealthy, prosperous","PVRNR p128")

    # Lagnaadhi Yoga (p129): benefics in H7 and H8 from lagna, no malefic conjoining
    h7_pl = [p for p in chart.planets if ph.get(p)==7]
    h8_pl = [p for p in chart.planets if ph.get(p)==8]
    h7_ben = all(p in _NAT_BENEF for p in h7_pl) and h7_pl
    h8_ben = all(p in _NAT_BENEF for p in h8_pl) and h8_pl
    lagnaadhi = bool(h7_ben and h8_ben)
    y("Lagnaadhi Yoga",h7_pl+h8_pl,lagnaadhi,3.0 if lagnaadhi else 0.0,
      "Benefics in H7 and H8, no malefics — great person, learned","PVRNR p129")

    # Jaya Yoga (p129): 10th lord in deep exaltation + 6th lord debilitated
    lord10 = hmap.house_lord[9]
    lord6  = hmap.house_lord[5]
    _DEEP_EXALT = {"Sun":(0,10),"Moon":(1,3),"Mars":(9,28),"Mercury":(5,15),
                    "Jupiter":(3,5),"Venus":(11,27),"Saturn":(6,20)}
    pos10 = chart.planets.get(lord10); pos6 = chart.planets.get(lord6)
    _DEBIL = {"Sun":6,"Moon":7,"Mars":3,"Mercury":11,"Jupiter":9,"Venus":5,"Saturn":0}
    lord10_exalt = (pos10 and _DEEP_EXALT.get(lord10, (None,None))[0] == pos10.sign_index)
    lord6_debil  = (pos6 and _DEBIL.get(lord6) == pos6.sign_index)
    jaya = bool(lord10_exalt and lord6_debil)
    y("Jaya Yoga",[lord10,lord6],jaya,3.0 if jaya else 0.0,
      "10th lord exalted + 6th lord debilitated — victorious, happy, defeats enemies","PVRNR p129")

    # Pushkala Yoga (p129): lagnesh with Moon + Moon dispositor in kendra/adhimitra + Moon aspects lagna
    lagnesh_h = ph.get(lagnesh,0); moon_si = chart.planets["Moon"].sign_index if "Moon" in chart.planets else 0
    lagnesh_with_moon = lagnesh_h == ph.get("Moon",0)
    _SIGN_LORD = {0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
                  6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter"}
    moon_dispositor = _SIGN_LORD[moon_si % 12]
    dispositor_strong = ph.get(moon_dispositor,0) in _STRONG
    pushkala = lagnesh_with_moon and dispositor_strong
    y("Pushkala Yoga",[lagnesh,"Moon",moon_dispositor],pushkala,2.5 if pushkala else 0.0,
      "Lagnesh with Moon, Moon's dispositor strong — eloquent, wealthy, famous","PVRNR p129")

    # Brahma Yoga (p130): Jupiter in kendra from 9th lord, Venus in kendra from 11th lord,
    # Mercury in kendra from lagnesh or 10th lord
    lord9 = hmap.house_lord[8]; lord11 = hmap.house_lord[10]
    l9h = ph.get(lord9,0); l11h = ph.get(lord11,0); jup_h = ph.get("Jupiter",0)
    ven_h = ph.get("Venus",0); mer_h = ph.get("Mercury",0); l10h = ph.get(lord10,0)
    def kendra_from(ref_h, target_h):
        if ref_h == 0 or target_h == 0: return False
        return abs(target_h - ref_h) % 12 in {0,3,6,9}
    brahma = (kendra_from(l9h, jup_h) and kendra_from(l11h, ven_h) and
              (kendra_from(lagnesh_h, mer_h) or kendra_from(l10h, mer_h)))
    y("Brahma Yoga",[lord9,lord11,lagnesh,"Jupiter","Venus","Mercury"],brahma,
      3.0 if brahma else 0.0,
      "Jupiter/Venus/Mercury in kendras from 9th/11th/1st lords — great scholar, renowned","PVRNR p130")

    return results
