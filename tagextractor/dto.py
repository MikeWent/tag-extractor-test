import enum

from pydantic import AnyHttpUrl, BaseModel


class TaskStatus(str, enum.Enum):
    NEW = "new"
    PROCESSING = "processing"
    FINISHED = "finished"


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


class ParseTaskCreated(BaseModel):
    id: int

    class Config:
        orm_mode = True
