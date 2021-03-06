"""Adding all models

Revision ID: 72ea53219af1
Revises: 9ce4ceae01b9
Create Date: 2022-02-28 13:46:57.635833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72ea53219af1'
down_revision = '9ce4ceae01b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('insurance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_insurance_id'), 'insurance', ['id'], unique=True)
    op.create_table('manager',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('fee', sa.Float(), nullable=True),
    sa.Column('sellchance', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_manager_id'), 'manager', ['id'], unique=True)
    op.create_table('owner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_owner_id'), 'owner', ['id'], unique=True)
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('dateofcreation', sa.DateTime(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.Column('manager', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manager'], ['manager.id'], ),
    sa.ForeignKeyConstraint(['owner'], ['owner.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_car_id'), 'car', ['id'], unique=True)
    op.create_table('insurancelist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car', sa.Integer(), nullable=True),
    sa.Column('insurance', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['car'], ['car.id'], ),
    sa.ForeignKeyConstraint(['insurance'], ['insurance.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_insurancelist_id'), 'insurancelist', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_insurancelist_id'), table_name='insurancelist')
    op.drop_table('insurancelist')
    op.drop_index(op.f('ix_car_id'), table_name='car')
    op.drop_table('car')
    op.drop_index(op.f('ix_owner_id'), table_name='owner')
    op.drop_table('owner')
    op.drop_index(op.f('ix_manager_id'), table_name='manager')
    op.drop_table('manager')
    op.drop_index(op.f('ix_insurance_id'), table_name='insurance')
    op.drop_table('insurance')
    # ### end Alembic commands ###
