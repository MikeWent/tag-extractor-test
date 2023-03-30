from pydantic import AnyHttpUrl, BaseModel, Field

from project import models


class ParseTask(BaseModel):
    id: int
    url: str
    status: models.ParseTask.TaskStatus

    tags: dict[str, int] | None = {}
    scripts: list[str] | None = []

    class Config:
        orm_mode = True


class ParseTaskCreate(BaseModel):
    url: AnyHttpUrl


class ParseTaskUpdate(BaseModel):
    status: models.ParseTask.TaskStatus | None = Field(default=None)
    tags: dict[str, int] | None = Field(default=None)
    scripts: list[str] | None = Field(default=None)


class ParseTaskCreated(BaseModel):
    id: int

    class Config:
        orm_mode = True
