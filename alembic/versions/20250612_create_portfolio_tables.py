"""create portfolios and portfolio_assets tables"""

from alembic import op
import sqlalchemy as sa

revision = '20250612_create_portfolio_tables'
down_revision = '20250611_add_unique_constraints'
branch_labels = None
depend_on = None


def upgrade():
    op.create_table(
        'portfolios',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
    )
    op.create_table(
        'portfolio_assets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('portfolio_id', sa.Integer, sa.ForeignKey('portfolios.id')),
        sa.Column('coin_id', sa.Integer, sa.ForeignKey('coins.id')),
        sa.Column('quantity', sa.Numeric),
    )


def downgrade():
    op.drop_table('portfolio_assets')
    op.drop_table('portfolios')
