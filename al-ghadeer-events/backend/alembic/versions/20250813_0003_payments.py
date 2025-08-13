"""payments table

Revision ID: 20250813_0003
Revises: 20250813_0002
Create Date: 2025-08-13 01:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250813_0003'
down_revision = '20250813_0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('events.id', ondelete='CASCADE'), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('method', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('note', sa.String(length=500), nullable=True),
        sa.Column('receipt_url', sa.String(length=500), nullable=True),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], name='fk_payments_created_by_users', ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], name='fk_payments_updated_by_users', ondelete='SET NULL'),
    )
    op.create_index('ix_payments_event_id', 'payments', ['event_id'])
    op.create_index('ix_payments_status', 'payments', ['status'])


def downgrade() -> None:
    op.drop_index('ix_payments_status', table_name='payments')
    op.drop_index('ix_payments_event_id', table_name='payments')
    op.drop_table('payments')