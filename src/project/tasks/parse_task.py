import time
from collections import Counter

from sqlalchemy.ext.asyncio import AsyncSession

from project import models, schemas, services
from project.db import get_db


class ParseTaskBaseClass:
    async def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(kwargs)
        db: AsyncSession = await get_db().__anext__()
        task = await services.ParseTaskService(db=db).get(
            id=kwargs.get("parse_task_id")
        )
        task = await services.ParseTaskService(db=db).update(
            db_obj=task,
            obj_in=schemas.parse_task.ParseTaskUpdate(
                status=models.ParseTask.TaskStatus.FAILED
            ),
        )


async def parse_task(parse_task_id: int, db: AsyncSession):
    task = await services.ParseTaskService(db=db).get(id=parse_task_id)
    task = await services.ParseTaskService(db=db).update(
        db_obj=task,
        obj_in=schemas.parse_task.ParseTaskUpdate(
            status=models.ParseTask.TaskStatus.PROCESSING
        ),
    )

    # fetch webpage
    req = ""
    soup = ""

    # all html tags, including duplicates
    tags_raw: list[str] = []
    # src of each script
    scripts: list[str] = []

    # traverse through html
    # for tag in soup.find_all():
    #     tags_raw.append(tag.name)
    #     if tag.name == "script":
    #         src = tag.get("src")
    #         if src:
    #             scripts.append(src)

    # effectively count all occurences of each tag
    tags: dict[str, int] = Counter(tags_raw)

    # save results
    await services.ParseTaskService(db=db).update(
        db_obj=task,
        obj_in=schemas.parse_task.ParseTaskUpdate(
            scripts=scripts,
            tags=tags,
            status=models.ParseTask.TaskStatus.FINISHED,
        ),
    )
