# alembic/versions/20250611_add_coin_external_ids.py
"""
Add coin_external_ids table to link internal coins with third‑party IDs.
"""
from alembic import op
import sqlalchemy as sa

revision = '20250611_add_coin_external_ids'
down_revision = '20250610_create_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "coin_external_ids",
        sa.Column("coin_id", sa.Integer, sa.ForeignKey("coins.id"), primary_key=True),
        sa.Column("coingecko_id", sa.String, unique=True),
        sa.Column("coinmarketcap_id", sa.Integer, unique=True),
        sa.Column("lunarcrush_symbol", sa.String, unique=True),
    )


def downgrade():
    op.drop_table("coin_external_ids")
