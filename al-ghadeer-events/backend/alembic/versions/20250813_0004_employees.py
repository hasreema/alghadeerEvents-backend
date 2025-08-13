"""employees table

Revision ID: 20250813_0004
Revises: 20250813_0003
Create Date: 2025-08-13 01:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250813_0004'
down_revision = '20250813_0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=100), nullable=True),
        sa.Column('hourly_wage', sa.Numeric(12, 2), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_employees_full_name', 'employees', ['full_name'])
    op.create_index('ix_employees_role', 'employees', ['role'])
    op.create_index('ix_employees_active', 'employees', ['is_active'])


def downgrade() -> None:
    op.drop_index('ix_employees_active', table_name='employees')
    op.drop_index('ix_employees_role', table_name='employees')
    op.drop_index('ix_employees_full_name', table_name='employees')
    op.drop_table('employees')