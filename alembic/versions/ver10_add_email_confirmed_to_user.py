"""add email_confirmed to user

Revision ID: ver10
Revises: ver9
Create Date: 2026-01-09 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ver10'
down_revision: Union[str, None] = 'ver9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Thêm column email_confirmed vào bảng users
    op.add_column('users', sa.Column('email_confirmed', sa.Boolean(), nullable=False, server_default='0'))


def downgrade() -> None:
    # Xóa column email_confirmed
    op.drop_column('users', 'email_confirmed')
