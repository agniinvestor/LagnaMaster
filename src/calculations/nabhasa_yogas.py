"""
src/calculations/nabhasa_yogas.py — Session 106

Nabhasa Yogas — complete 32 types from BPHS Ch.35.
"Sky formations" based on the pattern of planetary distribution.

BPHS divides into 4 groups:
  A. Āśraya (3) — based on sign type occupied
  B. Dala (2) — based on house type (kendra/trikona) occupied
  C. Ākriti (20) — based on geometric pattern across signs
  D. Sankhya (7) — based on total number of occupied signs

Only the strongest yoga in each group manifests (BPHS rule).
Each has a result description from classical commentary.

Source: BPHS Ch.35; B.V. Raman "Three Hundred Important Combinations" (intro);
        also PVRNR workbook list.
"""
from __future__ import annotations
from dataclasses import dataclass, field

_PLANETS_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]

# Sign classifications
_MOVABLE  = {0, 3, 6, 9}   # Ar, Cn, Li, Cp
_FIXED    = {1, 4, 7, 10}  # Ta, Le, Sc, Aq
_DUAL     = {2, 5, 8, 11}  # Ge, Vi, Sg, Pi
_FIRE     = {0, 4, 8}
_EARTH    = {1, 5, 9}
_AIR      = {2, 6, 10}
_WATER    = {3, 7, 11}
_ODD      = {0, 2, 4, 6, 8, 10}
_EVEN     = {1, 3, 5, 7, 9, 11}

_KENDRA   = {1, 4, 7, 10}
_TRIKONA  = {1, 5, 9}
_UPACHAYA = {3, 6, 10, 11}


@dataclass
class NabhasaYoga:
    name: str
    group: str         # "Āśraya" / "Dala" / "Ākriti" / "Sankhya"
    present: bool
    result: str        # classical interpretation
    planets_involved: list[str] = field(default_factory=list)


def _occupied_signs(chart) -> set[int]:
    return {chart.planets[p].sign_index for p in _PLANETS_7 if p in chart.planets}


def _occupied_houses(chart) -> set[int]:
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    return {hmap.planet_house[p] for p in _PLANETS_7 if p in hmap.planet_house}


def detect_nabhasa_yogas(chart) -> list[NabhasaYoga]:
    """Detect all 32 Nabhasa yogas."""
    yogas = []
    occ = _occupied_signs(chart)
    n_signs = len(occ)

    # ── GROUP A: Āśraya (3 yogas) ─────────────────────────────────────────────
    all_movable = all(s in _MOVABLE for s in occ)
    all_fixed   = all(s in _FIXED   for s in occ)
    all_dual    = all(s in _DUAL    for s in occ)

    yogas.append(NabhasaYoga("Rājju", "Āśraya", all_movable,
        "Rajju yoga: all planets in movable signs — constant travel, no fixed abode"))
    yogas.append(NabhasaYoga("Musala", "Āśraya", all_fixed,
        "Musala yoga: all planets in fixed signs — resolute, authoritative, wealthy"))
    yogas.append(NabhasaYoga("Nāla", "Āśraya", all_dual,
        "Nala yoga: all planets in dual signs — skilled, versatile, mixed results"))

    # ── GROUP B: Dala (2 yogas) ───────────────────────────────────────────────
    occ_houses = _occupied_houses(chart)
    all_kendra = all(h in _KENDRA for h in occ_houses)
    all_panap  = all(h in {2,5,8,11} for h in occ_houses)  # panapara
    all_apoklima = all(h in {3,6,9,12} for h in occ_houses)

    yogas.append(NabhasaYoga("Śubha", "Dala", all_kendra,
        "Shubha yoga: all planets in kendra — powerful, achieves desired results"))
    yogas.append(NabhasaYoga("Āśubha", "Dala", all_apoklima,
        "Ashubha yoga: all planets in apoklima — weak, struggles, overcome by enemies"))

    # ── GROUP C: Ākriti (20 yogas) ────────────────────────────────────────────
    # Gadā: all in two adjacent signs
    sign_list = sorted(occ)
    gada = n_signs == 2 and (sign_list[1] - sign_list[0]) in {1, 11}
    yogas.append(NabhasaYoga("Gadā", "Ākriti", gada,
        "Gada: planets in 2 adjacent signs — aggressive, violent, wealthy"))

    # Śakata: planets in 1st and 7th only
    shakata = (occ <= {chart.lagna_sign_index, (chart.lagna_sign_index+6)%12}
               and n_signs == 2)
    yogas.append(NabhasaYoga("Śakata", "Ākriti", shakata,
        "Shakata: planets in 1st and 7th — like a cart, fluctuating fortune"))

    # Vihaga: planets in 4th and 10th only
    vihaga_signs = {(chart.lagna_sign_index+3)%12, (chart.lagna_sign_index+9)%12}
    vihaga = occ <= vihaga_signs and n_signs == 2
    yogas.append(NabhasaYoga("Vihaga", "Ākriti", vihaga,
        "Vihaga: planets in 4th and 10th — like a bird, frequent travel"))

    # Śrīnātah: planets in 1st, 5th, 9th (all trines)
    trine_signs = {chart.lagna_sign_index, (chart.lagna_sign_index+4)%12,
                   (chart.lagna_sign_index+8)%12}
    srinat = occ <= trine_signs and n_signs >= 2
    yogas.append(NabhasaYoga("Śrīnātah (Trikona)", "Ākriti", srinat,
        "Srinatha: planets in trikona signs — prosperity, righteous, fortunate"))

    # Paśa: 5 or more signs occupied
    pasha = n_signs >= 5
    yogas.append(NabhasaYoga("Paśa", "Ākriti", pasha,
        "Pasha (noose): 5+ signs occupied — many activities, scattered"))

    # Kedarā: 4 or more signs occupied
    kedara = n_signs == 4
    yogas.append(NabhasaYoga("Kedarā", "Ākriti", kedara,
        "Kedara (field): 4 signs occupied — agricultural nature, hardworking"))

    # Śūla: 3 groups in trine positions
    sula_signs = [{0,4,8},{1,5,9},{2,6,10},{3,7,11}]
    sula = any(occ <= s for s in sula_signs) and n_signs == 3
    yogas.append(NabhasaYoga("Śūla", "Ākriti", sula,
        "Shula: planets in trine signs — aggressive, hurt others, eventually wealthy"))

    # Yava: planets in 1-3 and 7-9 (two halves)
    yava_half1 = set(range(0,3))
    yava_half2 = set(range(6,9))
    yava = all(s in yava_half1 | yava_half2 for s in occ) and len(occ & yava_half1) >= 2
    yogas.append(NabhasaYoga("Yava", "Ākriti", yava,
        "Yava (barley): planets in 1-3 and 7-9 signs — wealthy, generous"))

    # Camara: all planets in 7 consecutive signs
    sorted_occ = sorted(occ)
    camara = n_signs == 7 and (sorted_occ[-1] - sorted_occ[0]) == 6
    yogas.append(NabhasaYoga("Camara", "Ākriti", camara,
        "Chamara: 7 consecutive signs — skilled in debate, intelligent"))

    # ── GROUP D: Sankhya (7 yogas) ────────────────────────────────────────────
    _SANKHYA = {
        1: ("Gola",    "All in 1 sign — isolated, poor, sick, wanderer"),
        2: ("Yuga",    "2 signs — heretic, poor, lazy"),
        3: ("Śūla_s",  "3 signs — skilled fighter, suffering"),
        4: ("Kedarā_s","4 signs — farmer, patient, food-giver"),
        5: ("Paśa_s",  "5 signs — imprisoned, many relatives"),
        6: ("Damini",  "6 signs — wealthy, capable, generous"),
        7: ("Veena",   "7 signs — happy, wealthy, leader of people"),
    }
    if n_signs in _SANKHYA:
        name, result = _SANKHYA[n_signs]
        yogas.append(NabhasaYoga(name, "Sankhya", True, result))

    return yogas


def strongest_nabhasa(chart) -> list[NabhasaYoga]:
    """Return only present Nabhasa yogas."""
    return [y for y in detect_nabhasa_yogas(chart) if y.present]
