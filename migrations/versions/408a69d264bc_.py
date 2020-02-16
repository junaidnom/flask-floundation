"""empty message

Revision ID: 408a69d264bc
Revises: 
Create Date: 2019-12-30 00:31:13.334519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '408a69d264bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permission_name'), 'permission', ['name'], unique=True)
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_name'), 'role', ['name'], unique=True)
    op.create_table('tenant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenant_name'), 'tenant', ['name'], unique=False)
    op.create_table('role_to_permission',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    op.create_index(op.f('ix_role_to_permission_permission_id'), 'role_to_permission', ['permission_id'], unique=False)
    op.create_table('role_to_tenant',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenant.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'tenant_id')
    )
    op.create_table('tenant_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('_password', sa.String(length=250), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenant_user_username'), 'tenant_user', ['username'], unique=True)
    op.create_table('role_to_tenant_user',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('tenant_user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['tenant_user_id'], ['tenant_user.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'tenant_user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role_to_tenant_user')
    op.drop_index(op.f('ix_tenant_user_username'), table_name='tenant_user')
    op.drop_table('tenant_user')
    op.drop_table('role_to_tenant')
    op.drop_index(op.f('ix_role_to_permission_permission_id'), table_name='role_to_permission')
    op.drop_table('role_to_permission')
    op.drop_index(op.f('ix_tenant_name'), table_name='tenant')
    op.drop_table('tenant')
    op.drop_index(op.f('ix_role_name'), table_name='role')
    op.drop_table('role')
    op.drop_index(op.f('ix_permission_name'), table_name='permission')
    op.drop_table('permission')
    # ### end Alembic commands ###