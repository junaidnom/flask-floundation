"""empty message

Revision ID: a279c9131455
Revises: 408a69d264bc
Create Date: 2020-03-04 14:01:44.224883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a279c9131455'
down_revision = '408a69d264bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_result_first_name'), 'test_result', ['first_name'], unique=False)
    op.create_index(op.f('ix_test_result_last_name'), 'test_result', ['last_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_test_result_last_name'), table_name='test_result')
    op.drop_index(op.f('ix_test_result_first_name'), table_name='test_result')
    op.drop_table('test_result')
    # ### end Alembic commands ###
