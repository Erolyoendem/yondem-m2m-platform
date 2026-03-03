"""initial schema

Revision ID: c8e178707e87
Revises:
Create Date: 2026-03-02 22:30:28.640872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8e178707e87'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. agents (no FK dependencies) ────────────────────────────────────
    op.create_table('agents',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.Enum('publisher', 'advertiser', 'arbitrage', name='agenttype'), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive', 'suspended', name='agentstatus'), nullable=False, server_default='active'),
        sa.Column('performance_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('trust_level', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('commission_earned_total', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('wallet_address', sa.String(), nullable=True),
        sa.Column('daily_budget', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_agents_type', 'agents', ['type'])
    op.create_index('ix_agents_status', 'agents', ['status'])
    op.create_index('ix_agents_created_at', 'agents', ['created_at'])

    # ── 2. shops (no FK dependencies) ─────────────────────────────────────
    op.create_table('shops',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('logo_url', sa.String(500), nullable=True),
        sa.Column('website_url', sa.String(500), nullable=True),
        sa.Column('affiliate_network', sa.String(100), nullable=True),
        sa.Column('commission_rate', sa.Float(), nullable=True),
        sa.Column('cashback_rate', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # ── 3. products (shop_id plain Integer, no FK enforced) ────────────────
    op.create_table('products',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False, server_default='EUR'),
        sa.Column('shop_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('image_url', sa.String(500), nullable=True),
        sa.Column('product_url', sa.String(500), nullable=True),
        sa.Column('affiliate_url', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_products_shop_id', 'products', ['shop_id'])
    op.create_index('ix_products_category', 'products', ['category'])

    # ── 4. deals (plain integers, no FK enforced) ──────────────────────────
    op.create_table('deals',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('discount_value', sa.Float(), nullable=True),
        sa.Column('discount_type', sa.String(20), nullable=True),
        sa.Column('code', sa.String(50), nullable=True),
        sa.Column('shop_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('valid_from', sa.DateTime(), nullable=True),
        sa.Column('valid_until', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # ── 5. iot_devices (preferred_shop_id: no FK – type mismatch String/Int) ─
    op.create_table('iot_devices',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('device_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='active'),
        sa.Column('last_seen', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('api_key', sa.String(), nullable=False),
        sa.Column('auto_order_enabled', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('budget_limit', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('preferred_shop_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('api_key')
    )
    op.create_index('ix_iot_devices_status', 'iot_devices', ['status'])

    # ── 6. smart_contracts (FK → agents) ──────────────────────────────────
    op.create_table('smart_contracts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('agent_id', sa.String(), nullable=False),
        sa.Column('rules', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('execution_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('success_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_executed', sa.DateTime(), nullable=True),
        sa.Column('monthly_budget', sa.Float(), nullable=False, server_default='100.0'),
        sa.Column('spent_this_month', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id'])
    )
    op.create_index('ix_smart_contracts_agent_id', 'smart_contracts', ['agent_id'])
    op.create_index('ix_smart_contracts_is_active', 'smart_contracts', ['is_active'])

    # ── 7. transactions (FK → agents, smart_contracts; product_id: no FK) ─
    op.create_table('transactions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('publisher_id', sa.String(), nullable=False),
        sa.Column('advertiser_id', sa.String(), nullable=False),
        sa.Column('product_id', sa.String(), nullable=True),
        sa.Column('contract_id', sa.String(), nullable=True),
        sa.Column('product_price', sa.Float(), nullable=False),
        sa.Column('commission_amount', sa.Float(), nullable=False),
        sa.Column('platform_fee', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('status', sa.String(), nullable=False, server_default='completed'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['publisher_id'], ['agents.id']),
        sa.ForeignKeyConstraint(['advertiser_id'], ['agents.id']),
        sa.ForeignKeyConstraint(['contract_id'], ['smart_contracts.id']),
    )
    op.create_index('ix_transactions_publisher_id', 'transactions', ['publisher_id'])
    op.create_index('ix_transactions_advertiser_id', 'transactions', ['advertiser_id'])
    op.create_index('ix_transactions_created_at', 'transactions', ['created_at'])
    op.create_index('ix_transactions_status', 'transactions', ['status'])

    # ── 8. bids (FK → agents) ─────────────────────────────────────────────
    op.create_table('bids',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('advertiser_id', sa.String(), nullable=False),
        sa.Column('product_category', sa.String(), nullable=False),
        sa.Column('target_product', sa.String(), nullable=True),
        sa.Column('commission_rate', sa.Float(), nullable=False, server_default='0.10'),
        sa.Column('max_cpc', sa.Float(), nullable=False, server_default='0.50'),
        sa.Column('daily_budget', sa.Float(), nullable=False, server_default='100.0'),
        sa.Column('is_active', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['advertiser_id'], ['agents.id']),
    )
    op.create_index('ix_bids_advertiser_id', 'bids', ['advertiser_id'])
    op.create_index('ix_bids_product_category', 'bids', ['product_category'])
    op.create_index('ix_bids_is_active', 'bids', ['is_active'])

    # ── 9. wallets (FK → agents) ──────────────────────────────────────────
    op.create_table('wallets',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('agent_id', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('wallet_type', sa.String(), nullable=False, server_default='polygon'),
        sa.Column('ydm_balance', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('eth_balance', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_active', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('agent_id'),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id']),
    )


def downgrade() -> None:
    op.drop_table('wallets')
    op.drop_index('ix_bids_is_active', table_name='bids')
    op.drop_index('ix_bids_product_category', table_name='bids')
    op.drop_index('ix_bids_advertiser_id', table_name='bids')
    op.drop_table('bids')
    op.drop_index('ix_transactions_status', table_name='transactions')
    op.drop_index('ix_transactions_created_at', table_name='transactions')
    op.drop_index('ix_transactions_advertiser_id', table_name='transactions')
    op.drop_index('ix_transactions_publisher_id', table_name='transactions')
    op.drop_table('transactions')
    op.drop_index('ix_smart_contracts_is_active', table_name='smart_contracts')
    op.drop_index('ix_smart_contracts_agent_id', table_name='smart_contracts')
    op.drop_table('smart_contracts')
    op.drop_index('ix_iot_devices_status', table_name='iot_devices')
    op.drop_table('iot_devices')
    op.drop_table('deals')
    op.drop_index('ix_products_category', table_name='products')
    op.drop_index('ix_products_shop_id', table_name='products')
    op.drop_table('products')
    op.drop_table('shops')
    op.drop_index('ix_agents_created_at', table_name='agents')
    op.drop_index('ix_agents_status', table_name='agents')
    op.drop_index('ix_agents_type', table_name='agents')
    op.drop_table('agents')
    op.execute("DROP TYPE IF EXISTS agenttype")
    op.execute("DROP TYPE IF EXISTS agentstatus")
