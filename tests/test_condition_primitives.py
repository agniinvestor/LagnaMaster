"""tests/test_condition_primitives.py — Tests for new condition primitives."""
from __future__ import annotations

import pytest
from src.corpus.v2_builder import V2ChapterBuilder

from src.corpus.taxonomy import (
    VALID_CONDITION_PRIMITIVES,
    VALID_SIGN_TYPES,
    VALID_DERIVATIONS,
    VALID_UPAGRAHAS,
    VALID_CONDITION_MODES,
)


# ── Taxonomy completeness ────────────────────────────────────────────────────

def test_sign_types_contains_movable():
    assert "movable" in VALID_SIGN_TYPES

def test_sign_types_contains_all_modalities():
    for st in ("movable", "fixed", "dual"):
        assert st in VALID_SIGN_TYPES

def test_sign_types_contains_all_elements():
    for st in ("fire", "earth", "air", "water"):
        assert st in VALID_SIGN_TYPES

def test_sign_types_contains_parity():
    for st in ("odd", "even"):
        assert st in VALID_SIGN_TYPES

def test_derivations_contains_arudha():
    assert "arudha_pada" in VALID_DERIVATIONS

def test_derivations_contains_upa_pada():
    assert "upa_pada" in VALID_DERIVATIONS

def test_derivations_contains_karakamsa():
    assert "karakamsa" in VALID_DERIVATIONS

def test_derivations_contains_all_special_lagnas():
    for d in ("navamsa_lagna", "hora_lagna", "ghati_lagna",
              "varnada_lagna", "sri_lagna", "indu_lagna", "pranapada_lagna"):
        assert d in VALID_DERIVATIONS

def test_upagrahas_contains_dhuma():
    assert "dhuma" in VALID_UPAGRAHAS

def test_upagrahas_contains_gulika():
    assert "gulika" in VALID_UPAGRAHAS

def test_upagrahas_contains_mandi():
    assert "mandi" in VALID_UPAGRAHAS

def test_condition_modes():
    assert VALID_CONDITION_MODES == frozenset({"occupies", "aspects"})

def test_new_primitives_in_valid_set():
    for p in ("planet_in_sign_type", "planet_in_derived_house", "upagraha_in_house"):
        assert p in VALID_CONDITION_PRIMITIVES


def _make_builder(**kwargs):
    defaults = dict(
        chapter="Ch.99", category="test", id_start=9900,
        session="S999", sloka_count=10,
        chapter_tags=["test"],
    )
    defaults.update(kwargs)
    return V2ChapterBuilder(**defaults)


def _base_add(**overrides):
    """Return kwargs for a minimal valid b.add() call."""
    defaults = dict(
        conditions=[{"type": "planet_in_house", "planet": "sun", "house": 1}],
        signal_group="test_signal",
        direction="favorable", intensity="moderate",
        domains=["wealth"],
        predictions=[{"entity": "native", "claim": "test_claim_placeholder",
                       "domain": "wealth", "direction": "favorable", "magnitude": 0.5}],
        verse_ref="Ch.99 v.1",
        description="Test rule for condition primitive validation testing purposes.",
        commentary_context="Test commentary for validation.",
    )
    defaults.update(overrides)
    return defaults


# ── planet_in_sign_type validation ───────────────────────────────────────────

def test_sign_type_valid_accepted():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "movable"}],
    ))
    assert len(b.rules()) == 1


def test_sign_type_invalid_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "INVALID"}],
        ))


def test_sign_type_missing_sign_type_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_sign_type", "planet": "lord_of_5"}],
        ))


# ── planet_in_derived_house validation ───────────────────────────────────────

def test_derived_house_valid_accepted():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                      "base_house": 1, "offset": 7, "planet": "rahu"}],
    ))
    assert len(b.rules()) == 1


def test_derived_house_invalid_derivation_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_derived_house", "derivation": "INVALID",
                          "base_house": 1, "offset": 7, "planet": "rahu"}],
        ))


def test_derived_house_arudha_requires_base_house():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                          "offset": 7, "planet": "rahu"}],
        ))


def test_derived_house_karakamsa_no_base_house_ok():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_derived_house", "derivation": "karakamsa",
                      "offset": 1, "planet": "jupiter"}],
    ))
    assert len(b.rules()) == 1


def test_derived_house_with_aspects_mode():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                      "base_house": 1, "offset": 11, "planet": "jupiter",
                      "mode": "aspects"}],
    ))
    assert len(b.rules()) == 1


def test_derived_house_invalid_mode_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                          "base_house": 1, "offset": 7, "planet": "rahu",
                          "mode": "INVALID"}],
        ))


# ── upagraha_in_house validation ────────────────────────────────────────────

def test_upagraha_valid_accepted():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "upagraha_in_house", "upagraha": "dhuma", "house": 3}],
    ))
    assert len(b.rules()) == 1


def test_upagraha_invalid_name_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "upagraha_in_house", "upagraha": "INVALID", "house": 3}],
        ))


def test_upagraha_missing_house_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "upagraha_in_house", "upagraha": "dhuma"}],
        ))


# ── _build_primary_condition for new types ───────────────────────────────────

def test_primary_condition_sign_type():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "movable"}],
    ))
    r = b.rules()[0]
    assert r.primary_condition["placement_type"] == "planet_in_sign_type"
    assert r.primary_condition["planet"] == "lord_of_5"


def test_primary_condition_derived_house():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                      "base_house": 1, "offset": 7, "planet": "rahu"}],
    ))
    r = b.rules()[0]
    assert r.primary_condition["placement_type"] == "planet_in_derived_house"
    assert r.primary_condition["planet"] == "rahu"


def test_primary_condition_upagraha():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "upagraha_in_house", "upagraha": "dhuma", "house": 3}],
    ))
    r = b.rules()[0]
    assert r.primary_condition["placement_type"] == "upagraha_in_house"
    assert r.primary_condition["planet"] == "dhuma"
