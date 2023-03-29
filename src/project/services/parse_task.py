from sqlalchemy.orm import Session

from project.services.base import CRUDBase
from project import models, schemas


class ParseTaskInterface(
    CRUDBase[
        models.ParseTask,
        schemas.parse_task.ParseTaskCreate,
        schemas.parse_task.ParseTaskUpdate,
    ]
):
    def get_by_url(self, db: Session, *, url: str) -> models.ParseTask:
        return db.query(self.model).filter(self.model.url == url).one()

    def does_same_url_unfinished_exist(self, db: Session, *, url: str) -> bool:
        if (
            db.query(self.model)
            .filter(
                self.model.url == url,
                self.model.status == self.model.TaskStatus.NEW,
            )
            .one_or_none()
        ):
            return True
        return False


parse_task = ParseTaskInterface(models.ParseTask)
