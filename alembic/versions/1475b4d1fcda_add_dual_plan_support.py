"""add_dual_plan_support

Revision ID: 1475b4d1fcda
Revises: 
Create Date: 2026-02-07 15:09:29.834736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1475b4d1fcda'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to users table
    op.add_column('users', sa.Column('plan_type', sa.String(), nullable=False, server_default='express'))
    op.add_column('users', sa.Column('plan_status', sa.String(), nullable=False, server_default='trial'))
    op.add_column('users', sa.Column('baileys_session_id', sa.String(), nullable=True))
    op.add_column('users', sa.Column('baileys_auth_state', sa.Text(), nullable=True))
    
    # Add source column to messages table
    op.add_column('messages', sa.Column('source', sa.String(), nullable=False, server_default='api'))
    
    # Add backup_source column to backups table
    op.add_column('backups', sa.Column('backup_source', sa.String(), nullable=False, server_default='api'))
    
    # Create subscriptions table
    op.create_table(
        'subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('plan_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='active'),
        sa.Column('current_period_start', sa.DateTime(), nullable=True),
        sa.Column('current_period_end', sa.DateTime(), nullable=True),
        sa.Column('cancel_at_period_end', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        
        # Payment tracking
        sa.Column('stripe_subscription_id', sa.String(), nullable=True),
        sa.Column('stripe_customer_id', sa.String(), nullable=True),
        sa.Column('price_monthly', sa.Numeric(10, 2), nullable=True),
        
        # Usage tracking (for Express plan limits)
        sa.Column('messages_this_period', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('max_messages', sa.Integer(), nullable=False, server_default='5000'),
    )
    
    # Create indexes for better performance
    op.create_index('idx_users_plan_type', 'users', ['plan_type'])
    op.create_index('idx_users_baileys_session', 'users', ['baileys_session_id'])
    op.create_index('idx_messages_source', 'messages', ['source'])
    op.create_index('idx_backups_source', 'backups', ['backup_source'])
    op.create_index('idx_subscriptions_user_id', 'subscriptions', ['user_id'])
    op.create_index('idx_subscriptions_status', 'subscriptions', ['status'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_subscriptions_status')
    op.drop_index('idx_subscriptions_user_id')
    op.drop_index('idx_backups_source')
    op.drop_index('idx_messages_source')
    op.drop_index('idx_users_baileys_session')
    op.drop_index('idx_users_plan_type')
    
    # Drop subscriptions table
    op.drop_table('subscriptions')
    
    # Remove columns from backups
    op.drop_column('backups', 'backup_source')
    
    # Remove columns from messages
    op.drop_column('messages', 'source')
    
    # Remove columns from users
    op.drop_column('users', 'baileys_auth_state')
    op.drop_column('users', 'baileys_session_id')
    op.drop_column('users', 'plan_status')
    op.drop_column('users', 'plan_type')
