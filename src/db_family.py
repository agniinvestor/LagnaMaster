"""
src/db_family.py — Family Map Schema (S211)

PostgreSQL schema for the multigenerational family chart network.
Family relationships enable Phase 8 (S841-S900) multigenerational
pattern analysis and Phase 3 (S471-S530) family consent tracking.

GUARDRAIL G03: Each family member requires independent consent.
GUARDRAIL G16: Minimum 30 users before any social-proof display.

Public API
----------
  FamilyRelation          Enum of relationship types
  FAMILY_SCHEMA_DDL       SQL DDL string for family tables
  get_create_sql()        Return DDL as list of statements
"""

from __future__ import annotations

import enum


class FamilyRelation(enum.Enum):
    """Directional relationship types for the family graph."""
    PARENT = "parent"
    CHILD = "child"
    SPOUSE = "spouse"
    SIBLING = "sibling"
    GRANDPARENT = "grandparent"
    GRANDCHILD = "grandchild"
    UNCLE_AUNT = "uncle_aunt"
    NEPHEW_NIECE = "nephew_niece"
    COUSIN = "cousin"
    OTHER = "other"


FAMILY_SCHEMA_DDL: str = """
-- Family map schema for multigenerational pattern analysis (Phase 8)
-- G03: Each member requires independent DPDP 2023 / GDPR consent
-- G16: Minimum 30 users before any cluster/social display

-- Family groups: a named family unit
CREATE TABLE IF NOT EXISTS family_groups (
    id              BIGSERIAL PRIMARY KEY,
    owner_user_id   BIGINT NOT NULL,        -- user who created the family map
    name            VARCHAR(100) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Family members: each person in the family map
CREATE TABLE IF NOT EXISTS family_members (
    id                  BIGSERIAL PRIMARY KEY,
    family_group_id     BIGINT NOT NULL REFERENCES family_groups(id) ON DELETE CASCADE,
    chart_id            BIGINT,             -- NULL if no chart yet
    nickname            VARCHAR(100) NOT NULL,
    relation_to_owner   VARCHAR(30) NOT NULL,
    birth_year          INTEGER,            -- for display only; full chart stored in charts
    consent_granted     BOOLEAN NOT NULL DEFAULT FALSE,
    consent_granted_at  TIMESTAMPTZ,
    consent_withdrawn_at TIMESTAMPTZ,
    data_source         VARCHAR(30) NOT NULL DEFAULT 'self_reported',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Family relations: directed graph edges between family members
CREATE TABLE IF NOT EXISTS family_relations (
    id              BIGSERIAL PRIMARY KEY,
    family_group_id BIGINT NOT NULL REFERENCES family_groups(id) ON DELETE CASCADE,
    from_member_id  BIGINT NOT NULL REFERENCES family_members(id) ON DELETE CASCADE,
    to_member_id    BIGINT NOT NULL REFERENCES family_members(id) ON DELETE CASCADE,
    relation_type   VARCHAR(30) NOT NULL,   -- FamilyRelation enum value
    confidence      REAL NOT NULL DEFAULT 1.0,  -- for inferred relations
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (from_member_id, to_member_id, relation_type)
);

-- Family pattern observations: confirmed outcome patterns across family members
-- Used for Phase 8 multigenerational analysis (not before G03 compliance)
CREATE TABLE IF NOT EXISTS family_patterns (
    id              BIGSERIAL PRIMARY KEY,
    family_group_id BIGINT NOT NULL REFERENCES family_groups(id) ON DELETE CASCADE,
    pattern_type    VARCHAR(50) NOT NULL,   -- e.g. 'career_domain', 'health_domain'
    member_ids      JSONB NOT NULL,         -- array of family_member IDs showing pattern
    rule_ids        JSONB NOT NULL,         -- corpus rule IDs that may explain pattern
    confidence      REAL NOT NULL,
    notes           TEXT DEFAULT '',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for fast family lookups
CREATE INDEX IF NOT EXISTS family_members_group_idx ON family_members (family_group_id);
CREATE INDEX IF NOT EXISTS family_relations_from_idx ON family_relations (from_member_id);
CREATE INDEX IF NOT EXISTS family_relations_to_idx ON family_relations (to_member_id);
"""


def get_create_sql() -> list[str]:
    """Return DDL as a list of individual SQL statements."""
    return [
        stmt.strip()
        for stmt in FAMILY_SCHEMA_DDL.split(";")
        if stmt.strip() and not stmt.strip().startswith("--")
    ]
