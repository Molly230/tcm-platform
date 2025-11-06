"""create shipping table

Revision ID: shipping_001
Revises:
Create Date: 2025-10-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = 'shipping_001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建shippings表
    op.create_table('shippings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('courier_company', sa.Enum('SF', 'ZTO', 'YTO', 'STO', 'YD', 'JTSD', 'JD', 'EMS', 'DBKD', 'OTHER', name='couriercompany'), nullable=False),
    sa.Column('courier_company_name', sa.String(), nullable=True),
    sa.Column('tracking_number', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'PREPARING', 'SHIPPED', 'IN_TRANSIT', 'OUT_FOR_DELIVERY', 'DELIVERED', 'FAILED', 'RETURNED', 'CANCELLED', name='shippingstatus'), nullable=True),
    sa.Column('courier_name', sa.String(), nullable=True),
    sa.Column('courier_phone', sa.String(), nullable=True),
    sa.Column('shipped_at', sa.DateTime(), nullable=True),
    sa.Column('estimated_delivery_at', sa.DateTime(), nullable=True),
    sa.Column('delivered_at', sa.DateTime(), nullable=True),
    sa.Column('tracking_history', sa.JSON(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shippings_id'), 'shippings', ['id'], unique=False)
    op.create_index(op.f('ix_shippings_order_id'), 'shippings', ['order_id'], unique=True)
    op.create_index(op.f('ix_shippings_tracking_number'), 'shippings', ['tracking_number'], unique=False)


def downgrade() -> None:
    # 删除索引
    op.drop_index(op.f('ix_shippings_tracking_number'), table_name='shippings')
    op.drop_index(op.f('ix_shippings_order_id'), table_name='shippings')
    op.drop_index(op.f('ix_shippings_id'), table_name='shippings')
    # 删除表
    op.drop_table('shippings')
