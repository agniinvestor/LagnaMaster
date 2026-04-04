"""Mechanism vocabulary and claim extraction for migration audit.

Extracts two-tier claim buckets from both V1 prose descriptions and
V2 structured predictions using deterministic keyword matching.
No NLP dependencies — pure keyword→tag mapping.

Governance: MECHANISM_TAGS is a controlled vocabulary. No new tags
without explicit approval. Tag additions must be committed with
justification in the commit message.
"""
from __future__ import annotations

# ── Tier 2: Mechanism Tags (v0.1 — 18 tags) ────────────────────────────
MECHANISM_TAGS: dict[str, list[str]] = {
    "authority":        ["king", "government", "state", "ruler", "royal"],
    "family_paternal":  ["father", "paternal", "pitru"],
    "family_maternal":  ["mother", "maternal", "matru"],
    "siblings":         ["brother", "sister", "co-born", "sibling", "coborn"],
    "spouse":           ["wife", "husband", "spouse", "marriage", "marital"],
    "disputes":         ["litigation", "conflict", "quarrel", "dispute", "enemy", "enemies"],
    "taxation":         ["tax", "revenue", "levy", "dues"],
    "virtue":           ["righteous", "virtuous", "dharma", "fair", "noble"],
    "deception":        ["fraud", "deception", "cheat", "questionable", "unfair"],
    "public":           ["public", "people", "masses", "popular"],
    "self_effort":      ["self", "own", "personal", "industry"],
    "digestive":        ["stomach", "digestion", "bowel", "gastric"],
    "fire_accident":    ["fire", "burn", "fever", "inflammation"],
    "reputation":       ["fame", "reputation", "honor", "respect", "status"],
    "poverty":          ["poor", "poverty", "destitute", "penury"],
    "progeny_count":    ["sons", "daughters", "children", "progeny", "issue"],
    "longevity_risk":   ["death", "die", "longevity", "lifespan", "danger"],
    "spiritual":        ["spiritual", "moksha", "liberation", "renunciation"],
}

# ── Semantic keywords for domain + direction extraction ─────────────────
# Maps keyword → (domain, direction)
_DOMAIN_KEYWORDS: dict[str, tuple[str, str]] = {
    # Wealth
    "wealthy": ("wealth", "favorable"), "rich": ("wealth", "favorable"),
    "gains": ("wealth", "favorable"), "affluent": ("wealth", "favorable"),
    "prosperous": ("wealth", "favorable"), "income": ("wealth", "favorable"),
    "poor": ("wealth", "unfavorable"), "poverty": ("wealth", "unfavorable"),
    "loss": ("wealth", "unfavorable"), "expenses": ("wealth", "unfavorable"),
    "destitute": ("wealth", "unfavorable"), "penury": ("wealth", "unfavorable"),
    # Health
    "disease": ("health", "unfavorable"), "sickly": ("health", "unfavorable"),
    "disorders": ("health", "unfavorable"), "ailment": ("health", "unfavorable"),
    "healthy": ("health", "favorable"),
    # Character
    "happy": ("character", "favorable"), "happiness": ("character", "favorable"),
    "adventurous": ("character", "favorable"), "intelligent": ("character", "favorable"),
    "miserable": ("character", "unfavorable"), "wicked": ("character", "unfavorable"),
    # Career
    "fame": ("career", "favorable"), "famous": ("career", "favorable"),
    "king": ("career", "favorable"), "authority": ("career", "favorable"),
    "ruler": ("career", "favorable"), "poet": ("career", "favorable"),
    "speaker": ("career", "favorable"),
    # Relationships
    "wife": ("relationships", "favorable"), "husband": ("relationships", "favorable"),
    "marriage": ("relationships", "favorable"), "marital": ("relationships", "favorable"),
    "amity": ("relationships", "favorable"),
    "enmity": ("relationships", "unfavorable"), "divorce": ("relationships", "unfavorable"),
    # Progeny
    "sons": ("progeny", "favorable"), "children": ("progeny", "favorable"),
    "progeny": ("progeny", "favorable"), "barren": ("progeny", "unfavorable"),
    # Longevity
    "death": ("longevity", "unfavorable"), "die": ("longevity", "unfavorable"),
    "longevity": ("longevity", "favorable"), "danger": ("longevity", "unfavorable"),
    # Spirituality
    "spiritual": ("spirituality", "favorable"), "moksha": ("spirituality", "favorable"),
    "renunciation": ("spirituality", "favorable"),
}

# Negation words that flip direction
_NEGATION_WORDS = {"not", "no", "without", "devoid", "bereft", "loss", "lack",
                   "diminished", "reduced", "denied"}


def _infer_mechanisms(text: str) -> list[str]:
    """Extract mechanism tags from text using keyword matching."""
    text_lower = text.lower()
    found: list[str] = []
    for tag, keywords in MECHANISM_TAGS.items():
        if any(kw in text_lower for kw in keywords):
            found.append(tag)
    return found


def _infer_domains(text: str) -> list[tuple[str, str]]:
    """Extract (domain, direction) pairs from text."""
    words = text.lower().replace(",", " ").replace(".", " ").split()
    found: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    # Check for negation context (simple window-based)
    has_negation = bool(_NEGATION_WORDS & set(words))

    for word in words:
        if word in _DOMAIN_KEYWORDS:
            domain, direction = _DOMAIN_KEYWORDS[word]
            # Flip direction if negation detected near domain keyword
            if has_negation and direction == "favorable":
                direction = "unfavorable"
            elif has_negation and direction == "unfavorable":
                direction = "favorable"
            pair = (domain, direction)
            if pair not in seen:
                found.append(pair)
                seen.add(pair)
    return found


def _extraction_confidence(text: str, domains: list[tuple[str, str]],
                           mechanisms: list[str]) -> float:
    """Confidence score for claim extraction quality."""
    words = text.lower().split()
    total = max(len(words), 1)

    mechanism_hits = sum(1 for w in words
                        if any(w in syns for syns in MECHANISM_TAGS.values()))
    semantic_hits = sum(1 for w in words if w in _DOMAIN_KEYWORDS)
    signal_hits = mechanism_hits + semantic_hits
    signal_density = signal_hits / total

    if signal_density >= 0.15:
        return min(0.95, 0.6 + signal_density * 2)
    elif signal_density >= 0.05:
        return 0.5 + signal_density * 2
    elif domains:
        return 0.4
    else:
        return 0.2


def extract_claims(text: str) -> list[dict]:
    """Extract claim buckets from prose text (V1 rules).

    Returns list of claim dicts, each with:
        domain_direction: str  (e.g., "wealth_favorable")
        mechanisms: list[str]  (e.g., ["authority", "taxation"])
        confidence: float      (0.0 - 1.0)
        source_text: str       (original text)
    """
    domains = _infer_domains(text)
    mechanisms = _infer_mechanisms(text)
    confidence = _extraction_confidence(text, domains, mechanisms)

    if not domains:
        # UNMAPPED — no domain confidently extracted
        return [{"domain_direction": "", "mechanisms": mechanisms,
                 "confidence": confidence, "source_text": text}]

    claims: list[dict] = []
    for domain, direction in domains:
        claims.append({
            "domain_direction": f"{domain}_{direction}",
            "mechanisms": mechanisms,
            "confidence": confidence,
            "source_text": text,
        })
    return claims


def extract_v2_bucket(prediction: dict) -> dict:
    """Extract bucket from a V2 prediction dict.

    Uses same keyword mapping as V1 to ensure symmetric comparison.
    """
    domain = prediction.get("domain", "")
    direction = prediction.get("direction", "")
    claim_text = prediction.get("claim", "")

    mechanisms = _infer_mechanisms(claim_text)

    return {
        "domain_direction": f"{domain}_{direction}" if domain else "",
        "mechanisms": mechanisms,
        "confidence": 0.95,  # V2 has structured domain/direction — high confidence
        "source_text": claim_text,
    }
