"""User email

Revision ID: b4a9f37a0a94
Revises: 43ea06b96a59
Create Date: 2025-01-15 13:57:07.531766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4a9f37a0a94'
down_revision: Union[str, None] = '43ea06b96a59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(), nullable=False))
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['email'])
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
