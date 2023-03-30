import enum

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSON

from project.models.base_class import Base


class ParseTask(Base):
    __tablename__ = "parse_tasks"  # type: ignore

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)

    tags = Column(JSON)
    scripts = Column(ARRAY(String))

    class TaskStatus(str, enum.Enum):
        NEW = "new"
        PROCESSING = "processing"
        FINISHED = "finished"
        FAILED = "failed"

    status = Column(Enum(TaskStatus), default=TaskStatus.NEW)
