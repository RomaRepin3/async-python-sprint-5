"""
Init

Revision ID: d1f32ca8bc0c
Revises: 
Create Date: 2024-05-31 11:49:44.255961

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd1f32ca8bc0c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('login', sa.String(length=100), nullable=False),
        sa.Column('password', sa.String(length=100), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('login')
    )
    op.create_index(op.f('ix_user_created_at'), 'user', ['created_at'], unique=False)
    op.create_table(
        'file',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('path', sa.String(length=500), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('is_downloadable', sa.Boolean(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('path')
    )
    op.create_index(op.f('ix_file_created_at'), 'file', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_file_created_at'), table_name='file')
    op.drop_table('file')
    op.drop_index(op.f('ix_user_created_at'), table_name='user')
    op.drop_table('user')
