# alembic/versions/20250611_add_market_data_cols.py
"""
Add additional market data columns
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250611_add_market_data_cols'
down_revision = '20250611_add_coin_external_ids'
branch_labels = None
depend_on = None


def upgrade():
    op.add_column('market_data', sa.Column('high_24h', sa.Numeric))
    op.add_column('market_data', sa.Column('low_24h', sa.Numeric))
    op.add_column('market_data', sa.Column('price_change_24h', sa.Numeric))
    op.add_column('market_data', sa.Column('price_change_percentage_24h', sa.Numeric))
    op.add_column('market_data', sa.Column('percent_change_1h', sa.Numeric))
    op.add_column('market_data', sa.Column('percent_change_24h', sa.Numeric))


def downgrade():
    op.drop_column('market_data', 'percent_change_24h')
    op.drop_column('market_data', 'percent_change_1h')
    op.drop_column('market_data', 'price_change_percentage_24h')
    op.drop_column('market_data', 'price_change_24h')
    op.drop_column('market_data', 'low_24h')
    op.drop_column('market_data', 'high_24h')
