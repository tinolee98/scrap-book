"""initial

Revision ID: 7f7a38a156f7
Revises: 
Create Date: 2022-02-08 16:09:26.952811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f7a38a156f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table()


def downgrade():
    pass
