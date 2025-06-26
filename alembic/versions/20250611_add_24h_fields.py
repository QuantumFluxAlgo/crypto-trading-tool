# alembic/versions/20250611_add_24h_fields.py
"""Add open_24h column to market_data"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250611_add_24h_fields'
down_revision = '20250611_add_market_data_cols'
branch_labels = None
depend_on = None

def upgrade():
    op.add_column('market_data', sa.Column('open_24h', sa.Numeric))

def downgrade():
    op.drop_column('market_data', 'open_24h')

