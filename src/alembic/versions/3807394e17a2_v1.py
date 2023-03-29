"""v1

Revision ID: 3807394e17a2
Revises: 
Create Date: 2023-03-28 18:59:33.711362

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3807394e17a2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "parse_tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("tags", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("scripts", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column(
            "status",
            sa.Enum("NEW", "PROCESSING", "FINISHED", name="taskstatus"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("parse_tasks")
    # ### end Alembic commands ###
