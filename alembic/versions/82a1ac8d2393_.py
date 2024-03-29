"""empty message

Revision ID: 82a1ac8d2393
Revises: 480056c0c89b
Create Date: 2024-01-14 23:34:38.310197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '82a1ac8d2393'
down_revision: Union[str, None] = '480056c0c89b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dday',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('dday', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('dday_content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dday')
    # ### end Alembic commands ###
