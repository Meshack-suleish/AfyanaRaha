"""sent_at updated

Revision ID: a065a4dbe290
Revises: 6805e2781da1
Create Date: 2025-05-08 10:03:03.388394

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a065a4dbe290'
down_revision = '6805e2781da1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.alter_column('sent_at',
               existing_type=mysql.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.alter_column('sent_at',
               existing_type=mysql.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###
