"""empty message

Revision ID: 2ec4e9778fe8
Revises: 61000512f23f
Create Date: 2023-12-22 21:09:33.820872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '2ec4e9778fe8'
down_revision: Union[str, None] = '61000512f23f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hotplace',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('search_at', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('search_place', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hotplace')
    # ### end Alembic commands ###