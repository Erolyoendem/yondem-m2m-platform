"""add waitlist table

Revision ID: e7d13100d7f1
Revises: c8e178707e87
Create Date: 2026-03-03 03:06:24.326659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7d13100d7f1'
down_revision: Union[str, Sequence[str], None] = 'c8e178707e87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('waitlist',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_waitlist_created_at', 'waitlist', ['created_at'], unique=False)
    op.create_index('ix_waitlist_email', 'waitlist', ['email'], unique=True)
    op.create_index('ix_waitlist_type', 'waitlist', ['type'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_waitlist_type', table_name='waitlist')
    op.drop_index('ix_waitlist_email', table_name='waitlist')
    op.drop_index('ix_waitlist_created_at', table_name='waitlist')
    op.drop_table('waitlist')
