"""
tests/test_s211_ml_infra_schema.py — S211: pgvector + TimescaleDB + MLflow + family schema

Schema modules for Phase 6 ML infrastructure. All are configuration/DDL
only — no live database connections required in tests.
"""

from __future__ import annotations


# ── pgvector schema ───────────────────────────────────────────────────────────

def test_vector_schema_import():
    from src.db_vector import VECTOR_SCHEMA_DDL, VECTOR_DIM
    assert VECTOR_SCHEMA_DDL is not None
    assert isinstance(VECTOR_DIM, int) and VECTOR_DIM > 0


def test_vector_dim_matches_feature_count():
    """Vector dimension must match ChartFeatureVector output (13×12=156)."""
    from src.db_vector import VECTOR_DIM
    assert VECTOR_DIM == 156, f"Expected VECTOR_DIM=156, got {VECTOR_DIM}"


def test_vector_schema_contains_table():
    from src.db_vector import VECTOR_SCHEMA_DDL
    assert "chart_embeddings" in VECTOR_SCHEMA_DDL.lower()


# ── TimescaleDB schema ────────────────────────────────────────────────────────

def test_timescale_schema_import():
    from src.db_timescale import TIMESCALE_SCHEMA_DDL
    assert TIMESCALE_SCHEMA_DDL is not None


def test_timescale_schema_has_hypertable():
    from src.db_timescale import TIMESCALE_SCHEMA_DDL
    assert "hypertable" in TIMESCALE_SCHEMA_DDL.lower() or "timescaledb" in TIMESCALE_SCHEMA_DDL.lower()


def test_timescale_schema_has_dasha_table():
    from src.db_timescale import TIMESCALE_SCHEMA_DDL
    assert "dasha" in TIMESCALE_SCHEMA_DDL.lower()


# ── MLflow config ─────────────────────────────────────────────────────────────

def test_mlflow_config_import():
    from src.ml.mlflow_config import EXPERIMENT_NAMES, DEFAULT_TRACKING_URI
    assert EXPERIMENT_NAMES is not None
    assert DEFAULT_TRACKING_URI is not None


def test_mlflow_ob3_experiment_defined():
    from src.ml.mlflow_config import EXPERIMENT_NAMES
    assert "OB-3" in EXPERIMENT_NAMES


def test_mlflow_config_get_experiment():
    from src.ml.mlflow_config import get_experiment_config
    cfg = get_experiment_config("OB-3")
    assert "name" in cfg
    assert "tags" in cfg


# ── Family schema ─────────────────────────────────────────────────────────────

def test_family_schema_import():
    from src.db_family import FAMILY_SCHEMA_DDL, FamilyRelation
    assert FAMILY_SCHEMA_DDL is not None
    assert FamilyRelation is not None


def test_family_relation_values():
    from src.db_family import FamilyRelation
    assert "PARENT" in FamilyRelation.__members__
    assert "CHILD" in FamilyRelation.__members__
    assert "SPOUSE" in FamilyRelation.__members__


def test_family_schema_has_members_table():
    from src.db_family import FAMILY_SCHEMA_DDL
    assert "family_members" in FAMILY_SCHEMA_DDL.lower()


def test_family_schema_has_relations_table():
    from src.db_family import FAMILY_SCHEMA_DDL
    assert "family_relations" in FAMILY_SCHEMA_DDL.lower()
