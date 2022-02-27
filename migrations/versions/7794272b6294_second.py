"""Second

Revision ID: 7794272b6294
Revises: 18312370d8ad
Create Date: 2022-02-25 15:01:47.562967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7794272b6294'
down_revision = '18312370d8ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Car_id'), 'Car', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Car_id'), table_name='Car')
    op.drop_table('Car')
    # ### end Alembic commands ###
