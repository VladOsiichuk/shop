"""add orders

Revision ID: 4ee70d284f88
Revises: e61b070710a0
Create Date: 2021-11-11 23:04:20.378050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ee70d284f88'
down_revision = 'e61b070710a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('receiver_phone_number', sa.String(length=12), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_lines',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.BigInteger(), nullable=True),
    sa.Column('product_id', sa.BigInteger(), nullable=True),
    sa.Column('qty', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_lines')
    op.drop_table('orders')
    # ### end Alembic commands ###