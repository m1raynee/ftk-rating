"""add student to groups

Revision ID: 616c853ace5e
Revises: 27bd6b7b0f52
Create Date: 2023-04-19 19:45:39.346713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '616c853ace5e'
down_revision = '27bd6b7b0f52'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students_to_groups',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('group_id', 'student_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students_to_groups')
    # ### end Alembic commands ###
