"""event contract fields

Revision ID: 20250813_0008
Revises: 20250813_0007
Create Date: 2025-08-13 19:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250813_0008'
down_revision = '20250813_0007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('events', sa.Column('special_requests_text', sa.Text(), nullable=True))
    op.add_column('events', sa.Column('deposit_paid_flag', sa.Boolean(), nullable=True))
    op.add_column('events', sa.Column('end_time', sa.Time(), nullable=True))
    op.add_column('events', sa.Column('contacts_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('events', sa.Column('services_flags', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('events', sa.Column('pricing', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('events', sa.Column('menu_selections', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('events', sa.Column('dietary_restrictions', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('events', sa.Column('decoration_type', sa.String(length=50), nullable=True))
    op.add_column('events', sa.Column('internal_notes', sa.Text(), nullable=True))
    op.add_column('events', sa.Column('cancel_reason', sa.Text(), nullable=True))
    op.add_column('events', sa.Column('actual_guests', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('events', 'actual_guests')
    op.drop_column('events', 'cancel_reason')
    op.drop_column('events', 'internal_notes')
    op.drop_column('events', 'decoration_type')
    op.drop_column('events', 'dietary_restrictions')
    op.drop_column('events', 'menu_selections')
    op.drop_column('events', 'pricing')
    op.drop_column('events', 'services_flags')
    op.drop_column('events', 'contacts_json')
    op.drop_column('events', 'end_time')
    op.drop_column('events', 'deposit_paid_flag')
    op.drop_column('events', 'special_requests_text')