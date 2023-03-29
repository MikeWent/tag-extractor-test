# Import all the models, so that Base has them before being
# imported by Alembic
from project.models.base_class import Base  # noqa
from project.models.parse_task import ParseTask  # noqa
