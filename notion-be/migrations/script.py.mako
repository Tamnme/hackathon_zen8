"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
<<<<<<< HEAD
    ${downgrades if downgrades else "pass"}
=======
    ${downgrades if downgrades else "pass"} 
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0
