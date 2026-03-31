"""src/corpus/bb_reference.py — Bhavat Bhavam 12×12 semantic reference matrix.

For any house H and any derivative N, returns the semantic meaning of
"Nth house from H" — the entity, domain, and interpretation.

Usage:
    from src.corpus.bb_reference import get_bb_chains, BB_MATRIX

    # What BB chains does house 10 participate in?
    chains = get_bb_chains(house=10)
    # Returns: [
    #   {"base_house": 9, "derivative": "2nd_from", "entity": "father", "domain": "wealth"},
    #   {"base_house": 4, "derivative": "7th_from", "entity": "mother", "domain": "marriage"},
    #   {"base_house": 7, "derivative": "4th_from", "entity": "spouse", "domain": "property_vehicles"},
    #   {"base_house": 10, "derivative": "1st_from", "entity": "native", "domain": "career_status"},
    #   ...
    # ]
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# Core house meanings (1st from each house = the house itself)
# ═══════════════════════════════════════════════════════════════════════════════

HOUSE_MEANINGS = {
    1: {"entity": "native", "domain": "physical_health", "label": "self/body"},
    2: {"entity": "native", "domain": "wealth", "label": "wealth/speech/family"},
    3: {"entity": "siblings", "domain": "character_temperament", "label": "siblings/courage/initiative"},
    4: {"entity": "mother", "domain": "property_vehicles", "label": "mother/home/happiness"},
    5: {"entity": "children", "domain": "intelligence_education", "label": "children/intelligence/purva punya"},
    6: {"entity": "native", "domain": "enemies_litigation", "label": "enemies/disease/debt"},
    7: {"entity": "spouse", "domain": "marriage", "label": "spouse/partnerships"},
    8: {"entity": "native", "domain": "longevity", "label": "longevity/transformation/occult"},
    9: {"entity": "father", "domain": "spirituality", "label": "father/fortune/dharma"},
    10: {"entity": "native", "domain": "career_status", "label": "career/profession/karma"},
    11: {"entity": "native", "domain": "wealth", "label": "gains/income/fulfillment"},
    12: {"entity": "native", "domain": "spirituality", "label": "expenses/loss/moksha/foreign"},
}

# ═══════════════════════════════════════════════════════════════════════════════
# Derivative meanings — what does "Nth from H" mean?
# Key derivatives used in classical Jyotish:
#   2nd from = wealth/resources of that house's entity
#   3rd from = initiative/siblings of that entity
#   4th from = happiness/home of that entity
#   5th from = intelligence/children of that entity
#   6th from = enemies/disease of that entity
#   7th from = partnerships/opposition of that entity
#   8th from = longevity/death of that entity
#   9th from = fortune/dharma of that entity
#   10th from = career/karma of that entity
#   11th from = gains of that entity
#   12th from = loss/expenditure of that entity
# ═══════════════════════════════════════════════════════════════════════════════

DERIVATIVE_LABELS = {
    1: "self",
    2: "wealth/resources",
    3: "initiative/siblings",
    4: "happiness/home",
    5: "intelligence/children",
    6: "enemies/disease",
    7: "partnerships/opposition",
    8: "longevity/death",
    9: "fortune/dharma",
    10: "career/karma",
    11: "gains",
    12: "loss/expenditure",
}

DERIVATIVE_DOMAINS = {
    1: "self",
    2: "wealth",
    3: "character_temperament",
    4: "property_vehicles",
    5: "intelligence_education",
    6: "enemies_litigation",
    7: "marriage",
    8: "longevity",
    9: "spirituality",
    10: "career_status",
    11: "wealth",
    12: "foreign_travel",
}

DERIVATIVE_NAMES = {
    1: "1st_from", 2: "2nd_from", 3: "3rd_from", 4: "4th_from",
    5: "5th_from", 6: "6th_from", 7: "7th_from", 8: "8th_from",
    9: "9th_from", 10: "10th_from", 11: "11th_from", 12: "12th_from",
}


def _compute_bb_matrix() -> dict[int, list[dict]]:
    """Build the full 12×12 BB matrix.

    For each effective_house (1-12), returns all base_houses that view it
    as a meaningful derivative.

    Returns dict[effective_house] → list of {base_house, derivative, entity, domain, label}
    """
    matrix: dict[int, list[dict]] = {h: [] for h in range(1, 13)}

    for base in range(1, 13):
        base_info = HOUSE_MEANINGS[base]
        for n in range(1, 13):
            effective = (base + n - 2) % 12 + 1  # nth house from base
            if n == 1:
                continue  # skip self-reference (1st from = itself)

            matrix[effective].append({
                "base_house": base,
                "derivative": DERIVATIVE_NAMES[n],
                "effective_house": effective,
                "entity": base_info["entity"],
                "domain": DERIVATIVE_DOMAINS[n],
                "label": f"{DERIVATIVE_LABELS[n]} of {base_info['label']}",
            })

    return matrix


BB_MATRIX = _compute_bb_matrix()


def get_bb_chains(house: int) -> list[dict]:
    """Get all BB chains where this house is the effective house.

    Returns list of dicts, each describing one BB interpretation.
    """
    return BB_MATRIX.get(house, [])


def get_bb_chains_for_pair(base_house: int, effective_house: int) -> list[dict]:
    """Get BB chains for a specific base→effective pair."""
    return [c for c in BB_MATRIX.get(effective_house, [])
            if c["base_house"] == base_house]


def get_primary_bb_chains(house: int, max_chains: int = 5) -> list[dict]:
    """Get the most important BB chains for a house.

    Filters to the classical 'primary derivatives' that astrologers
    actually use: 2nd (wealth), 7th (partnerships), 8th (death),
    9th (fortune), 10th (career) from major houses.
    """
    PRIMARY_DERIVATIVES = {"2nd_from", "4th_from", "7th_from", "8th_from",
                           "9th_from", "10th_from"}
    PRIMARY_BASES = {1, 4, 5, 7, 9, 10}  # Major houses

    all_chains = BB_MATRIX.get(house, [])
    filtered = [c for c in all_chains
                if c["derivative"] in PRIMARY_DERIVATIVES
                and c["base_house"] in PRIMARY_BASES]

    # Sort by base_house importance (1, 7, 9, 10, 4, 5)
    priority = {1: 0, 7: 1, 9: 2, 10: 3, 4: 4, 5: 5}
    filtered.sort(key=lambda c: priority.get(c["base_house"], 99))

    return filtered[:max_chains]
