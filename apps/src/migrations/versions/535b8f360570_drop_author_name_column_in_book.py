"""drop author, name column in book

Revision ID: 535b8f360570
Revises: cf7679866751
Create Date: 2022-02-21 21:35:24.937970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '535b8f360570'
down_revision = 'cf7679866751'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    if bind.engine.name not in ['sqlite']:
        op.drop_column('book', 'author')
        op.drop_column('book', 'name')
        op.drop_column('book', 'detailUrl')
        op.add_column('book', 'authors', sa.String(length=120), nullable=False)
        op.add_column('book', 'title', sa.String(length=120), nullable=False)
        op.add_column('book', 'url', sa.String(length=180), nullable=False)
        return
    op.rename_table('book', '_book')
    op.create_table('book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=120), nullable=False),
        sa.Column('authors', sa.String(length=120), nullable=False),
        sa.Column('publisher', sa.String(length=120), nullable=False),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('thumbnail', sa.String(length=180), nullable=False),
        sa.Column('url', sa.String(length=180), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('_book')


def downgrade():
    bind = op.get_bind()
    if bind.engine.name not in ['sqlite']:
        op.add_column('book', 'author', sa.String(length=120), nullable=False)
        op.add_column('book', 'name', sa.String(length=120), nullable=False)
        op.add_column('book', 'detailUrl', sa.String(length=180), nullable=False)
        op.drop_column('book', 'authors')
        op.drop_column('book', 'title')
        op.drop_column('book', 'url')
        return
    op.rename_table('book', '_book')
    op.create_table('book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('author', sa.String(length=120), nullable=False),
        sa.Column('publisher', sa.String(length=120), nullable=False),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('thumbnail', sa.String(length=180), nullable=False),
        sa.Column('detailUrl', sa.String(length=180), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('_book')
    pass
