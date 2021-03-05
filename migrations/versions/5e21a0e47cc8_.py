"""empty message

Revision ID: 5e21a0e47cc8
Revises: 
Create Date: 2021-03-05 08:51:17.655044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e21a0e47cc8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=True),
    sa.Column('first_name', sa.String(length=150), nullable=True),
    sa.Column('last_name', sa.String(length=150), nullable=True),
    sa.Column('email_address', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    op.create_table('baby',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('parent_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['user.public_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sleep',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('sleep_type', sa.String(length=150), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('sleep_duration', sa.DateTime(), nullable=True),
    sa.Column('sleep_complete', sa.Boolean(), nullable=True),
    sa.Column('child_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['child_id'], ['baby.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sleep')
    op.drop_table('baby')
    op.drop_table('user')
    # ### end Alembic commands ###