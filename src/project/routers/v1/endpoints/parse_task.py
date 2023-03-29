from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from project import schemas, services, tasks
from project.db import get_db

router = APIRouter(prefix="/parse_tasks")


@router.post(
    "/",
    responses={201: {"model": schemas.parse_task.ParseTaskCreated}, 403: {}, 404: {}},
    status_code=201,
)
def create_parse_task(
    new_task: schemas.parse_task.ParseTaskCreate,
    db: Session = Depends(get_db),
) -> schemas.parse_task.ParseTaskCreated:
    if services.parse_task.does_same_url_unfinished_exist(db=db, url=new_task.url):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unfinished task with the same URL already exists.",
        )
    created_task = services.parse_task.create(db=db, obj_in=new_task)
    tasks.parse_task.delay(parse_task_id=created_task.id)
    return created_task


@router.get(
    "/{task_id}", responses={200: {"model": schemas.parse_task.ParseTask}, 404: {}}
)
def get_parse_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> schemas.parse_task.ParseTask:
    task = services.parse_task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task
