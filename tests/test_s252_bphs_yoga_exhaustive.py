"""tests/test_s252_bphs_yoga_exhaustive.py — S252: BPHS Yoga Exhaustive (150 rules)."""
from __future__ import annotations


def test_yex_count():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    assert BPHS_YOGA_EXHAUSTIVE_REGISTRY.count() == 150


def test_all_yex_rules_present():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    ids = {r.rule_id for r in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all()}
    for i in range(1, 151):
        assert f"YEX{i:03d}" in ids, f"YEX{i:03d} missing"


def test_yex_category():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    for rule in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all():
        assert rule.category == "yoga", f"{rule.rule_id} wrong category"


def test_yex_school_parashari():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    for rule in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all():
        assert rule.school == "parashari", f"{rule.rule_id} unexpected school"


def test_yex_source_bphs():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    for rule in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all():
        assert rule.source == "BPHS", f"{rule.rule_id} wrong source"


def test_pancha_mahapurusha():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    pmp = [r for r in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all() if "pancha_mahapurusha" in r.tags]
    assert len(pmp) == 5


def test_nabhasa_yogas_present():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    nabhasa = [r for r in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all() if "nabhasa" in r.tags]
    assert len(nabhasa) >= 15


def test_viparita_raja_types():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    viparita = [r for r in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all() if "viparita_raja" in r.tags]
    assert len(viparita) == 3
    subtypes = {r.rule_id for r in viparita}
    assert "YEX049" in subtypes  # Harsha
    assert "YEX050" in subtypes  # Sarala
    assert "YEX051" in subtypes  # Vimala


def test_neechabhanga_rules():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    nb = [r for r in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all() if "neechabhanga" in r.tags]
    assert len(nb) >= 7


def test_parivartana_yoga_count():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    pari = [r for r in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all() if "parivartana" in r.tags]
    assert len(pari) >= 10


def test_gaja_kesari():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    rule = BPHS_YOGA_EXHAUSTIVE_REGISTRY.get("YEX072")
    assert rule is not None
    assert "gaja_kesari" in rule.tags
    assert "jupiter_kendra_moon" in rule.tags


def test_dharma_karma_adhipati():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    rule = BPHS_YOGA_EXHAUSTIVE_REGISTRY.get("YEX028")
    assert rule is not None
    assert "dharma_karma_adhipati" in rule.tags


def test_kala_sarpa():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    rule = BPHS_YOGA_EXHAUSTIVE_REGISTRY.get("YEX097")
    assert rule is not None
    assert "kala_sarpa" in rule.tags


def test_mangal_dosha_complete():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    rule = BPHS_YOGA_EXHAUSTIVE_REGISTRY.get("YEX125")
    assert rule is not None
    assert "mangal_dosha" in rule.tags
    rule_cancel = BPHS_YOGA_EXHAUSTIVE_REGISTRY.get("YEX126")
    assert rule_cancel is not None
    assert "mangal_dosha_cancellation" in rule_cancel.tags


def test_implemented_false():
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY
    for rule in BPHS_YOGA_EXHAUSTIVE_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_combined_corpus_includes_yex():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1334  # 1184 + 150 = 1334
