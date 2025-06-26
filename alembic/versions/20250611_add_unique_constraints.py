from alembic import op
import sqlalchemy as sa

revision = '20250611_add_unique_constraints'
down_revision = '20250611_add_24h_fields'
branch_labels = None
depend_on = None


def upgrade():
    # market_data indexes and constraint
    with op.batch_alter_table('market_data') as batch_op:
        batch_op.create_index('ix_market_data_coin_id', ['coin_id'])
        batch_op.create_index('ix_market_data_timestamp', ['timestamp'])
        batch_op.create_unique_constraint('uix_market_data_coin_time', ['coin_id', 'timestamp'])

    # sentiment_data indexes and constraint
    with op.batch_alter_table('sentiment_data') as batch_op:
        batch_op.create_index('ix_sentiment_data_coin_id', ['coin_id'])
        batch_op.create_index('ix_sentiment_data_timestamp', ['timestamp'])
        batch_op.create_unique_constraint('uix_sentiment_data_coin_time', ['coin_id', 'timestamp'])


def downgrade():
    with op.batch_alter_table('sentiment_data') as batch_op:
        batch_op.drop_constraint('uix_sentiment_data_coin_time', type_='unique')
        batch_op.drop_index('ix_sentiment_data_timestamp')
        batch_op.drop_index('ix_sentiment_data_coin_id')

    with op.batch_alter_table('market_data') as batch_op:
        batch_op.drop_constraint('uix_market_data_coin_time', type_='unique')
        batch_op.drop_index('ix_market_data_timestamp')
        batch_op.drop_index('ix_market_data_coin_id')
