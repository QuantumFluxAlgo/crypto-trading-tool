# alembic/versions/20250611_add_24h_fields.py
"""Add 24h market columns to market_data"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250611_add_24h_fields'
down_revision = '20250610_create_tables'
branch_labels = None
depend_on = None

def upgrade():
    op.add_column('market_data', sa.Column('open_24h', sa.Numeric))
    op.add_column('market_data', sa.Column('high_24h', sa.Numeric))
    op.add_column('market_data', sa.Column('low_24h', sa.Numeric))
    op.add_column('market_data', sa.Column('percent_change_24h', sa.Numeric))

def downgrade():
    op.drop_column('market_data', 'percent_change_24h')
    op.drop_column('market_data', 'low_24h')
    op.drop_column('market_data', 'high_24h')
    op.drop_column('market_data', 'open_24h')

