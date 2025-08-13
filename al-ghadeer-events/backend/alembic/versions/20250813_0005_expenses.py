"""expenses table

Revision ID: 20250813_0005
Revises: 20250813_0004
Create Date: 2025-08-13 01:40:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250813_0005'
down_revision = '20250813_0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'expenses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('events.id', ondelete='SET NULL'), nullable=True),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('expense_date', sa.Date(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], name='fk_expenses_created_by_users', ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], name='fk_expenses_updated_by_users', ondelete='SET NULL'),
    )
    op.create_index('ix_expenses_event_id', 'expenses', ['event_id'])
    op.create_index('ix_expenses_category', 'expenses', ['category'])
    op.create_index('ix_expenses_date', 'expenses', ['expense_date'])


def downgrade() -> None:
    op.drop_index('ix_expenses_date', table_name='expenses')
    op.drop_index('ix_expenses_category', table_name='expenses')
    op.drop_index('ix_expenses_event_id', table_name='expenses')
    op.drop_table('expenses')