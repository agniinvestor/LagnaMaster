"""
src/db_vector.py — pgvector Schema (S211)

PostgreSQL + pgvector schema for storing 156-dimensional chart feature
embeddings. Used by Phase 6 ML pipeline for similarity search and
feature analysis.

GUARDRAIL G22: No analysis without OSF pre-registration.
This module provides schema only — analysis code is deferred to S611+.

Environment variables
---------------------
PG_DSN      PostgreSQL DSN (same as db_pg.py)
            Requires pgvector extension: CREATE EXTENSION IF NOT EXISTS vector;

Public API
----------
  VECTOR_DIM          Integer: expected feature vector dimension (156)
  VECTOR_SCHEMA_DDL   SQL string to create the schema
  get_create_sql()    Return DDL as list of statements
"""

from __future__ import annotations

# Feature vector dimension: 13 extractors × 12 houses = 156 (as of S198)
VECTOR_DIM: int = 156

# pgvector schema DDL
VECTOR_SCHEMA_DDL: str = f"""
-- pgvector extension (must be installed: CREATE EXTENSION IF NOT EXISTS vector)
-- Schema: chart_embeddings — stores feature vectors for Phase 6 ML analysis
-- G22: Do not run SHAP or statistical analysis without OSF pre-registration.

CREATE TABLE IF NOT EXISTS chart_embeddings (
    id              BIGSERIAL PRIMARY KEY,
    chart_id        BIGINT NOT NULL REFERENCES charts(id) ON DELETE CASCADE,
    school          VARCHAR(20) NOT NULL DEFAULT 'parashari',
    engine_version  VARCHAR(20) NOT NULL,
    feature_vector  vector({VECTOR_DIM}),      -- pgvector type
    feature_names   JSONB,                      -- ordered list of feature names
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (chart_id, school, engine_version)
);

-- Index for nearest-neighbor similarity search
CREATE INDEX IF NOT EXISTS chart_embeddings_vector_idx
    ON chart_embeddings
    USING ivfflat (feature_vector vector_cosine_ops)
    WITH (lists = 100);

-- Index for lookups by chart_id
CREATE INDEX IF NOT EXISTS chart_embeddings_chart_idx
    ON chart_embeddings (chart_id);

-- Metadata table for feature schema versions
CREATE TABLE IF NOT EXISTS feature_schema_versions (
    version         VARCHAR(20) PRIMARY KEY,
    feature_count   INTEGER NOT NULL,
    feature_names   JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    notes           TEXT DEFAULT ''
);
"""


def get_create_sql() -> list[str]:
    """Return DDL as a list of individual SQL statements."""
    return [
        stmt.strip()
        for stmt in VECTOR_SCHEMA_DDL.split(";")
        if stmt.strip() and not stmt.strip().startswith("--")
    ]
