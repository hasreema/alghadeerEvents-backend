"""auth and audit columns

Revision ID: 20250813_0002
Revises: 20250813_0001
Create Date: 2025-08-13 00:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250813_0002'
down_revision = '20250813_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('email', name='uq_users_email'),
        sa.UniqueConstraint('username', name='uq_users_username'),
    )
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_username', 'users', ['username'])

    # audit columns on events
    op.add_column('events', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('updated_by', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_events_created_by_users', 'events', 'users', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('fk_events_updated_by_users', 'events', 'users', ['updated_by'], ['id'], ondelete='SET NULL')
    op.create_index('ix_events_date', 'events', ['date'])
    op.create_index('ix_events_status', 'events', ['status'])
    op.create_index('ix_events_date_status', 'events', ['date', 'status'])

    # audit columns on tasks
    op.add_column('tasks', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('updated_by', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_tasks_created_by_users', 'tasks', 'users', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('fk_tasks_updated_by_users', 'tasks', 'users', ['updated_by'], ['id'], ondelete='SET NULL')
    op.create_index('ix_tasks_status', 'tasks', ['status'])
    op.create_index('ix_tasks_priority', 'tasks', ['priority'])
    op.create_index('ix_tasks_status_priority', 'tasks', ['status', 'priority'])
    op.create_index('ix_tasks_due_date', 'tasks', ['due_date'])


def downgrade() -> None:
    # drop task indices and fks/cols
    op.drop_index('ix_tasks_due_date', table_name='tasks')
    op.drop_index('ix_tasks_status_priority', table_name='tasks')
    op.drop_index('ix_tasks_priority', table_name='tasks')
    op.drop_index('ix_tasks_status', table_name='tasks')
    op.drop_constraint('fk_tasks_updated_by_users', 'tasks', type_='foreignkey')
    op.drop_constraint('fk_tasks_created_by_users', 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'updated_by')
    op.drop_column('tasks', 'created_by')

    # drop event indices and fks/cols
    op.drop_index('ix_events_date_status', table_name='events')
    op.drop_index('ix_events_status', table_name='events')
    op.drop_index('ix_events_date', table_name='events')
    op.drop_constraint('fk_events_updated_by_users', 'events', type_='foreignkey')
    op.drop_constraint('fk_events_created_by_users', 'events', type_='foreignkey')
    op.drop_column('events', 'updated_by')
    op.drop_column('events', 'created_by')

    # drop users table
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')