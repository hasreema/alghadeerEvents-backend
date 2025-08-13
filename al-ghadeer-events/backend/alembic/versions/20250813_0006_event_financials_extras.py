"""event financials and extras

Revision ID: 20250813_0006
Revises: 20250813_0005
Create Date: 2025-08-13 02:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250813_0006'
down_revision = '20250813_0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add fields to events
    op.add_column('events', sa.Column('event_type', sa.String(length=50), nullable=True))
    op.add_column('events', sa.Column('quoted_total', sa.Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('events', sa.Column('payments_total', sa.Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('events', sa.Column('expenses_total', sa.Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('events', sa.Column('labor_total', sa.Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('events', sa.Column('outstanding_amount', sa.Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('events', sa.Column('payment_status', sa.String(length=20), nullable=False, server_default='unpaid'))
    op.create_index('ix_events_payment_status', 'events', ['payment_status'])
    op.create_index('ix_events_event_type', 'events', ['event_type'])

    # services
    op.create_table(
        'event_services',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('events.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('total_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # contacts
    op.create_table(
        'event_contacts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('events.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('note', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # assignments
    op.create_table(
        'event_assignments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('events.id', ondelete='CASCADE'), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id', ondelete='SET NULL'), nullable=True),
        sa.Column('role', sa.String(length=100), nullable=True),
        sa.Column('hours', sa.Numeric(10, 2), nullable=False),
        sa.Column('hourly_rate', sa.Numeric(12, 2), nullable=False),
        sa.Column('total_cost', sa.Numeric(12, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('event_assignments')
    op.drop_table('event_contacts')
    op.drop_table('event_services')

    op.drop_index('ix_events_event_type', table_name='events')
    op.drop_index('ix_events_payment_status', table_name='events')
    op.drop_column('events', 'payment_status')
    op.drop_column('events', 'outstanding_amount')
    op.drop_column('events', 'labor_total')
    op.drop_column('events', 'expenses_total')
    op.drop_column('events', 'payments_total')
    op.drop_column('events', 'quoted_total')
    op.drop_column('events', 'event_type')