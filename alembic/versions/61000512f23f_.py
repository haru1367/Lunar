"""empty message

Revision ID: 61000512f23f
Revises: dc737e43729d
Create Date: 2023-12-16 18:58:06.015323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '61000512f23f'
down_revision: Union[str, None] = 'dc737e43729d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('crater', 'comment_list')
    op.drop_column('crater', 'comment_num')
    op.drop_column('crater', 'heart_list')
    op.drop_column('crater', 'heart_num')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crater', sa.Column('heart_num', sa.INTEGER(), nullable=False))
    op.add_column('crater', sa.Column('heart_list', sa.VARCHAR(), nullable=False))
    op.add_column('crater', sa.Column('comment_num', sa.INTEGER(), nullable=False))
    op.add_column('crater', sa.Column('comment_list', sa.VARCHAR(), nullable=False))
    # ### end Alembic commands ###
