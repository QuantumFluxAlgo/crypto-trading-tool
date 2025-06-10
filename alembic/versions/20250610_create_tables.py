# alembic/versions/20250610_create_tables.py
"""
Create initial tables: coins, market_data, sentiment_data
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250610_create_tables'
down_revision = None
branch_labels = None
depend_on = None


def upgrade():
    op.create_table(
        'coins',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('symbol', sa.String, nullable=False, unique=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('source', sa.String),
        sa.Column('last_updated', sa.DateTime),
    )
    op.create_table(
        'market_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('coin_id', sa.Integer, sa.ForeignKey('coins.id')),
        sa.Column('timestamp', sa.DateTime),
        sa.Column('price_usd', sa.Numeric),
        sa.Column('market_cap', sa.Numeric),
        sa.Column('volume_24h', sa.Numeric),
        sa.Column('source', sa.String),
    )
    op.create_table(
        'sentiment_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('coin_id', sa.Integer, sa.ForeignKey('coins.id')),
        sa.Column('timestamp', sa.DateTime),
        sa.Column('galaxy_score', sa.Numeric),
        sa.Column('alt_rank', sa.Integer),
        sa.Column('tweet_volume', sa.Integer),
        sa.Column('social_score', sa.Numeric),
    )

def downgrade():
    op.drop_table('sentiment_data')
    op.drop_table('market_data')
    op.drop_table('coins')
