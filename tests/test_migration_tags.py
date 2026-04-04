"""Tests for migration claim extraction."""
from __future__ import annotations


def test_extract_domains_from_wealth_text():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("native will be wealthy and famous")
    domains = {c["domain_direction"] for c in claims}
    assert "wealth_favorable" in domains


def test_extract_domains_from_health_text():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("native suffers from stomach disorders")
    domains = {c["domain_direction"] for c in claims}
    assert "health_unfavorable" in domains


def test_extract_mechanism_authority():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("loss of wealth through the king")
    assert any("authority" in c.get("mechanisms", []) for c in claims)


def test_extract_multiple_mechanisms():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("wealth through king and father")
    mechs = set()
    for c in claims:
        mechs.update(c.get("mechanisms", []))
    assert "authority" in mechs
    assert "family_paternal" in mechs


def test_extract_mixed_direction():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("wealthy but through questionable means")
    domains = {c["domain_direction"] for c in claims}
    assert "wealth_favorable" in domains or "wealth_mixed" in domains


def test_unmapped_text_low_confidence():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("life becomes difficult in many ways")
    assert all(c.get("confidence", 1.0) < 0.5 for c in claims) or len(claims) == 0


def test_extract_v2_prediction():
    from src.corpus.migration_tags import extract_v2_bucket
    pred = {"domain": "wealth", "direction": "favorable",
            "claim": "wealthy_through_virtuous_means"}
    bucket = extract_v2_bucket(pred)
    assert bucket["domain_direction"] == "wealth_favorable"
    assert "virtue" in bucket["mechanisms"]


def test_mechanism_tags_frozen():
    """Mechanism tags should not be modified at runtime."""
    from src.corpus.migration_tags import MECHANISM_TAGS
    assert isinstance(MECHANISM_TAGS, dict)
    assert "authority" in MECHANISM_TAGS
    assert len(MECHANISM_TAGS) == 18
