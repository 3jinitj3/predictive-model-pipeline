"""create test table

Revision ID: 065034e327f3
Revises: 
Create Date: 2026-11-03 21:12:23.739561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '065034e327f3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'test',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('desciption', sa.Unicode(200))
    )

def downgrade() -> None:
    op.drop_table('test')
