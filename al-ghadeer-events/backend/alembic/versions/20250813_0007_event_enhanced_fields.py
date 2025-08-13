"""enhanced event fields

Revision ID: 20250813_0007
Revises: 20250813_0006
Create Date: 2025-08-13 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250813_0007'
down_revision = '20250813_0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('events', sa.Column('name', sa.String(length=255), nullable=True))
    op.add_column('events', sa.Column('type', sa.String(length=50), nullable=True))
    op.add_column('events', sa.Column('type_custom', sa.String(length=100), nullable=True))
    op.add_column('events', sa.Column('starts_at', sa.DateTime(), nullable=True))
    op.add_column('events', sa.Column('locations', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('events', sa.Column('gender', sa.String(length=20), nullable=True))
    op.add_column('events', sa.Column('guest_count', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('special_requests', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('events', sa.Column('deposit_total', sa.Numeric(12, 2), nullable=True))
    op.add_column('events', sa.Column('deposit_paid', sa.Numeric(12, 2), nullable=True))
    op.add_column('events', sa.Column('phones', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.create_index('ix_events_name', 'events', ['name'])
    op.create_index('ix_events_type', 'events', ['type'])
    op.create_index('ix_events_starts_at', 'events', ['starts_at'])


def downgrade() -> None:
    op.drop_index('ix_events_starts_at', table_name='events')
    op.drop_index('ix_events_type', table_name='events')
    op.drop_index('ix_events_name', table_name='events')
    op.drop_column('events', 'phones')
    op.drop_column('events', 'deposit_paid')
    op.drop_column('events', 'deposit_total')
    op.drop_column('events', 'special_requests')
    op.drop_column('events', 'guest_count')
    op.drop_column('events', 'gender')
    op.drop_column('events', 'locations')
    op.drop_column('events', 'starts_at')
    op.drop_column('events', 'type_custom')
    op.drop_column('events', 'type')
    op.drop_column('events', 'name')