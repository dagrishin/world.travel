"""reformat user model

Revision ID: 6258029475d7
Revises: 8321d984b6b4
Create Date: 2023-01-14 23:26:03.723129

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import src

# revision identifiers, used by Alembic.
revision = '6258029475d7'
down_revision = '8321d984b6b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', src.auth.models.RoleTypeEnum(name='role_type'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('user_id', postgresql.UUID(), nullable=False),
    sa.Column('role_id', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.add_column('users', sa.Column('role_id', postgresql.UUID(), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
    op.drop_table('user_roles')
    op.drop_table('roles')
    # ### end Alembic commands ###