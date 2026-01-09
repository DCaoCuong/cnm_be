"""create email_verifications table

Revision ID: ver9
Revises: ver8
Create Date: 2026-01-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'ver9'
down_revision = 'ver8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tạo bảng email_verifications
    op.create_table(
        'email_verifications',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('code_hash', sa.String(length=255), nullable=False),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('resend_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_sent_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('verified', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        
        # Audit columns (từ AuditMixin)
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('deleted_by', sa.String(length=36), nullable=True),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    
    # Tạo index cho user_id để tăng tốc query
    op.create_index('ix_email_verifications_user_id', 'email_verifications', ['user_id'])
    
    # Tạo index composite cho các query phổ biến
    op.create_index(
        'ix_email_verifications_user_active', 
        'email_verifications', 
        ['user_id', 'is_active', 'verified']
    )


def downgrade() -> None:
    # Xóa indexes
    op.drop_index('ix_email_verifications_user_active', table_name='email_verifications')
    op.drop_index('ix_email_verifications_user_id', table_name='email_verifications')
    
    # Xóa bảng
    op.drop_table('email_verifications')
