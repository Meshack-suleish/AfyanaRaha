"""sent_at added

Revision ID: edcfe1b12376
Revises: 68e1d0b3a6bb
Create Date: 2025-05-08 10:33:02.415298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edcfe1b12376'
down_revision = '68e1d0b3a6bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sent_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('sent_at')

    # ### end Alembic commands ###
