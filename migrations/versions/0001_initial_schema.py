"""migrations/versions/0001_initial_schema.py
Alembic migration — initial PostgreSQL schema for LagnaMaster.
Creates the `charts` and `score_runs` tables with indexes.

Run:
    alembic upgrade head
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "charts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("day", sa.Integer(), nullable=False),
        sa.Column("hour", sa.Float(), nullable=False),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lon", sa.Float(), nullable=False),
        sa.Column(
            "tz_offset", sa.Float(), nullable=False, server_default=sa.text("5.5")
        ),
        sa.Column(
            "ayanamsha", sa.Text(), nullable=False, server_default=sa.text("'lahiri'")
        ),
        sa.Column(
            "chart_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "scores_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )

    op.create_table(
        "score_runs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "chart_id",
            sa.Integer(),
            sa.ForeignKey("charts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "run_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "scores_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
    )

    # Indexes
    op.create_index("idx_charts_created", "charts", ["created_at"], postgresql_using="btree")
    op.create_index(
        "idx_charts_name",
        "charts",
        ["name"],
        postgresql_where=sa.text("name IS NOT NULL"),
    )
    op.create_index("idx_score_runs_chart", "score_runs", ["chart_id"])


def downgrade() -> None:
    op.drop_table("score_runs")
    op.drop_table("charts")
