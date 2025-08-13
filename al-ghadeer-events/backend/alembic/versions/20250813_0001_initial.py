"""initial

Revision ID: 20250813_0001
Revises: 
Create Date: 2025-08-13 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250813_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('time', sa.Time(), nullable=True),
        sa.Column('organizer', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_events_title', 'events', ['title'])
    op.create_index('ix_events_location', 'events', ['location'])

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('assigned_to', sa.String(length=100), nullable=True),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('priority', sa.String(length=50), nullable=True),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('events.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_tasks_title', 'tasks', ['title'])
    op.create_index('ix_tasks_event_id', 'tasks', ['event_id'])


def downgrade() -> None:
    op.drop_index('ix_tasks_event_id', table_name='tasks')
    op.drop_index('ix_tasks_title', table_name='tasks')
    op.drop_table('tasks')

    op.drop_index('ix_events_location', table_name='events')
    op.drop_index('ix_events_title', table_name='events')
    op.drop_table('events')