"""Changed Insurance

Revision ID: 1302f65c8d7a
Revises: 72ea53219af1
Create Date: 2022-02-28 14:03:53.174069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1302f65c8d7a'
down_revision = '72ea53219af1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insurance', sa.Column('expiredate', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('insurance', 'expiredate')
    # ### end Alembic commands ###
