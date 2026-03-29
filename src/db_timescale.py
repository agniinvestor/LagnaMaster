"""
src/db_timescale.py — TimescaleDB Schema (S211)

TimescaleDB schema for time-series dasha data, outcome confirmations,
and transit activations. Used by Phase 5 (S611-S700) temporal model.

Requires TimescaleDB extension:
  CREATE EXTENSION IF NOT EXISTS timescaledb;

Public API
----------
  TIMESCALE_SCHEMA_DDL   SQL DDL string for all time-series tables
  get_create_sql()       Return DDL as list of statements
"""

from __future__ import annotations

TIMESCALE_SCHEMA_DDL: str = """
-- TimescaleDB extension (must be installed)
-- Tables are converted to hypertables after creation.

-- Dasha periods: tracks active dasha/antardasha periods for each chart
CREATE TABLE IF NOT EXISTS dasha_periods (
    id              BIGSERIAL PRIMARY KEY,
    chart_id        BIGINT NOT NULL,
    period_start    TIMESTAMPTZ NOT NULL,
    period_end      TIMESTAMPTZ NOT NULL,
    md_planet       VARCHAR(20) NOT NULL,   -- Mahadasha lord
    ad_planet       VARCHAR(20),            -- Antardasha lord (NULL for MD only)
    pd_planet       VARCHAR(20),            -- Pratyantardasha lord
    dasha_system    VARCHAR(30) NOT NULL DEFAULT 'vimshottari',
    school          VARCHAR(20) NOT NULL DEFAULT 'parashari',
    capacity_score  REAL,                   -- Promise engine capacity at period start
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Convert to hypertable (TimescaleDB call — run after table creation)
-- SELECT create_hypertable('dasha_periods', 'period_start', if_not_exists => TRUE);

-- Outcome confirmations: confirmed life events for validation pipeline
CREATE TABLE IF NOT EXISTS outcome_confirmations (
    id              BIGSERIAL PRIMARY KEY,
    chart_id        BIGINT NOT NULL,
    event_date      TIMESTAMPTZ NOT NULL,   -- When the event occurred
    outcome_domain  VARCHAR(30) NOT NULL,   -- career, relationship, health, etc.
    outcome_type    VARCHAR(30) NOT NULL,   -- promotion, marriage, relocation, etc.
    confirmed       BOOLEAN NOT NULL,       -- TRUE = event occurred as predicted
    user_prior_prob REAL,                   -- G04: captured BEFORE showing prediction
    confidence_mean REAL,                   -- Mean engine confidence
    signal_isolation REAL,                  -- confidence_mean - user_prior_prob
    data_source     VARCHAR(30) NOT NULL DEFAULT 'self_reported',
    rodden_rating   VARCHAR(5) DEFAULT '',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Convert to hypertable
-- SELECT create_hypertable('outcome_confirmations', 'event_date', if_not_exists => TRUE);

-- Transit activations: when planets transit over key natal positions
CREATE TABLE IF NOT EXISTS transit_activations (
    id              BIGSERIAL PRIMARY KEY,
    chart_id        BIGINT NOT NULL,
    transit_date    TIMESTAMPTZ NOT NULL,
    transit_planet  VARCHAR(20) NOT NULL,
    natal_point     VARCHAR(30) NOT NULL,   -- 'moon', 'lagna', 'h10_cusp', etc.
    aspect_type     VARCHAR(20) NOT NULL,   -- 'conjunction', 'opposition', etc.
    delivery_score  REAL,                   -- Layer II delivery gate score
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Convert to hypertable
-- SELECT create_hypertable('transit_activations', 'transit_date', if_not_exists => TRUE);
"""


def get_create_sql() -> list[str]:
    """Return DDL as a list of individual SQL statements (non-comment lines)."""
    return [
        stmt.strip()
        for stmt in TIMESCALE_SCHEMA_DDL.split(";")
        if stmt.strip() and not stmt.strip().startswith("--") and not stmt.strip().startswith("/*")
    ]
