import enum

from pydantic import AnyHttpUrl, BaseModel


class TaskStatus(str, enum.Enum):
    NEW = "new"
    PROCESSING = "processing"
    FINISHED = "finished"
    FAILED = "failed"


class ParseTask(BaseModel):
    id: int
    url: str
    status: TaskStatus

    tags: dict[str, int] | None = {}
    scripts: list[str] | None = []

    class Config:
        orm_mode = True


class ParseTaskCreate(BaseModel):
    url: AnyHttpUrl


class ParseTaskUpdate(BaseModel):
    status: TaskStatus | None
    tags: dict[str, int] | None
    scripts: list[str] | None


class ParseTaskCreated(BaseModel):
    id: int

    class Config:
        orm_mode = True