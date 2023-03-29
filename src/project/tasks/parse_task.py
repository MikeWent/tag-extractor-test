import time
from collections import Counter

import bs4
import requests
import celery
from sqlalchemy.orm import Session

from project import models, schemas, services
from project.db import get_db
from project.tasks.celery_app import celery_app


class ParseTaskBaseClass(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(kwargs)
        db: Session = get_db().__next__()
        task = services.parse_task.get(db=db, id=kwargs.get("parse_task_id"))
        task = services.parse_task.update(
            db=db,
            db_obj=task,
            obj_in=schemas.parse_task.ParseTaskUpdate(
                status=models.ParseTask.TaskStatus.FAILED
            ),
        )


@celery_app.task(acks_late=True, base=ParseTaskBaseClass)
def parse_task(parse_task_id: int, db: Session = get_db().__next__()):
    task = services.parse_task.get(db=db, id=parse_task_id)
    task = services.parse_task.update(
        db=db,
        db_obj=task,
        obj_in=schemas.parse_task.ParseTaskUpdate(
            status=models.ParseTask.TaskStatus.PROCESSING
        ),
    )

    # fetch webpage
    req = requests.get(task.url)
    soup = bs4.BeautifulSoup(req.text, features="html.parser")

    # imitate heavy work
    time.sleep(3)

    # all html tags, including duplicates
    tags_raw = []
    # src of each script
    scripts = []

    # traverse through html
    for tag in soup.find_all():
        tags_raw.append(tag.name)
        if tag.name == "script":
            src = tag.get("src")
            if src:
                scripts.append(src)

    # effectively count all occurences of each tag
    tags: dict[str, int] = Counter(tags_raw)

    # save results
    services.parse_task.update(
        db=db,
        db_obj=task,
        obj_in=schemas.parse_task.ParseTaskUpdate(
            scripts=scripts,
            tags=tags,
            status=models.ParseTask.TaskStatus.FINISHED,
        ),
    )
