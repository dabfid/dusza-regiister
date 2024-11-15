"""empty message

Revision ID: 8c1ce62e7db6
Revises: 11d5aeadba95
Create Date: 2024-11-10 15:09:17.483470

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '8c1ce62e7db6'
down_revision = '11d5aeadba95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deadline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('deadline', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_deadline_id'), ['id'], unique=False)
    
    op.bulk_insert(
        sa.table(
            'deadline',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('date', sa.DateTime, nullable=False),
        ),
        [
            {'id': 1, 'date': datetime.utcnow()},
        ]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('deadline', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_deadline_id'))
    
    op.drop_table('deadline')
    # ### end Alembic commands ###
