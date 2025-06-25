from alembic import op
import sqlalchemy as sa

revision = '20250611_add_unique_constraints'
down_revision = '20250610_create_tables'
branch_labels = None
depend_on = None


def upgrade():
    # market_data indexes and constraint
    op.create_index('ix_market_data_coin_id', 'market_data', ['coin_id'])
    op.create_index('ix_market_data_timestamp', 'market_data', ['timestamp'])
    op.create_unique_constraint('uix_market_data_coin_time', 'market_data', ['coin_id', 'timestamp'])

    # sentiment_data indexes and constraint
    op.create_index('ix_sentiment_data_coin_id', 'sentiment_data', ['coin_id'])
    op.create_index('ix_sentiment_data_timestamp', 'sentiment_data', ['timestamp'])
    op.create_unique_constraint('uix_sentiment_data_coin_time', 'sentiment_data', ['coin_id', 'timestamp'])


def downgrade():
    op.drop_constraint('uix_sentiment_data_coin_time', 'sentiment_data', type_='unique')
    op.drop_index('ix_sentiment_data_timestamp', table_name='sentiment_data')
    op.drop_index('ix_sentiment_data_coin_id', table_name='sentiment_data')

    op.drop_constraint('uix_market_data_coin_time', 'market_data', type_='unique')
    op.drop_index('ix_market_data_timestamp', table_name='market_data')
    op.drop_index('ix_market_data_coin_id', table_name='market_data')
