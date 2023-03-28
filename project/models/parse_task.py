import enum

from sqlalchemy import Column, Enum, Integer, String

from sqlalchemy.dialects.postgresql import ARRAY, JSON
from project.models.base import Base


class ParseTask(Base):
    __tablename__ = "parse_tasks"

    id = Column(Integer, primary_key=True)
    url = Column(String)

    tags = Column(JSON)
    scripts = Column(ARRAY(String))

    class TaskStatus(str, enum.Enum):
        NEW = "new"
        PROCESSING = "processing"
        FINISHED = "finished"

    status = Column(Enum(TaskStatus), default=TaskStatus.NEW)
