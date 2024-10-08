"""empty message

Revision ID: 36f37500b06a
Revises: 
Create Date: 2024-09-16 01:22:18.257151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36f37500b06a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coupons',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('coupon_number', sa.String(), nullable=False),
    sa.Column('is_used', sa.Boolean(), nullable=False),
    sa.Column('create_user_email', sa.String(), nullable=False),
    sa.Column('create_user_name', sa.String(), nullable=False),
    sa.Column('discount_price', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('coupon_number')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('coupons')
    # ### end Alembic commands ###
