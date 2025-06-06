"""insert_settings_default

Revision ID: 7cd894a6b3ba
Revises: cb184292b797
Create Date: 2025-06-05 20:43:16.272159

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql.expression import table, column
from sqlalchemy.sql.sqltypes import Integer

# revision identifiers, used by Alembic.
revision: str = '7cd894a6b3ba'
down_revision: Union[str, None] = 'cb184292b797'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define a "virtual" table (without a model) to insert data
settings_table = table(
    'settings',
    column('first_day_of_week', Integer),
    column('first_day_of_month', Integer),
)

def upgrade() -> None:
    op.bulk_insert(settings_table, [
        {
            'first_day_of_week': 0,
            'first_day_of_month': 1,
        }
    ])


def downgrade() -> None:
    op.execute(settings_table.delete())