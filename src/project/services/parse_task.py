from sqlalchemy import select

from project import exceptions, models, schemas
from project.services.base import CRUDBase


class ParseTaskService(
    CRUDBase[
        models.ParseTask,
        schemas.parse_task.ParseTaskCreate,
        schemas.parse_task.ParseTaskUpdate,
    ]
):
    model = models.ParseTask

    async def get_by_url(self, *, url: str) -> models.ParseTask | None:
        results = await self.db.scalars(select(self.model).where(self.model.url == url))
        return results.one_or_none()

    async def check_unfinished_same_url(self, *, url: str) -> None:
        results = await self.db.scalars(
            select(self.model).where(
                self.model.url == url,
                self.model.status == self.model.TaskStatus.NEW,
            )
        )
        task = results.one_or_none()
        if task:
            raise exceptions.parse_task.SameURLUnfinishedExists(
                model=self.model, id=task.id
            )
