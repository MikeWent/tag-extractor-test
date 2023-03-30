from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from project import schemas, services, tasks, models
from project.db import get_db

router = APIRouter(prefix="/parse_tasks")


@router.post(
    "/",
    responses={201: {"model": schemas.parse_task.ParseTaskCreated}, 403: {}, 404: {}},
    status_code=201,
)
async def create_parse_task(
    new_task: schemas.parse_task.ParseTaskCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    await services.ParseTaskService(db=db).check_unfinished_same_url(url=new_task.url)
    created_task = await services.ParseTaskService(db=db).create(obj_in=new_task)
    background_tasks.add_task(tasks.parse_task, db_task=created_task, db=db)
    return created_task


@router.get(
    "/{task_id}", responses={200: {"model": schemas.parse_task.ParseTask}, 404: {}}
)
async def get_parse_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await services.ParseTaskService(db=db).get(id=task_id)
