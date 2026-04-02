"""tests/test_condition_primitives.py — Tests for new condition primitives."""
from __future__ import annotations


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
