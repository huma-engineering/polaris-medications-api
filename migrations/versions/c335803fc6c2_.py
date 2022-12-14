"""empty message

Revision ID: c335803fc6c2
Revises: 955292e25fbc
Create Date: 2018-01-16 09:57:30.263809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c335803fc6c2'
down_revision = '955292e25fbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('only_one_active_medication', 'medication', [
                    'name'],
                    unique=True, postgresql_where=sa.text('deleted IS NULL'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('only_one_active_medication', table_name='medication')
    # ### end Alembic commands ###
