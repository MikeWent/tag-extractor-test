from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from project import schemas, services
from project.db import get_db

router = APIRouter()


@router.post(
    "/parse_page",
    responses={201: {"model": schemas.parse_task.ParseTaskCreated}, 403: {}, 404: {}},
    status_code=201,
)
def create_parse_task(
    new_task: schemas.parse_task.ParseTaskCreate,
    db: Session = Depends(get_db),
) -> schemas.parse_task.ParseTaskCreated:
    if services.parse_task.does_same_url_unfinished_exist(db, new_task.url):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unfinished task with the same URL already exists.",
        )
    return services.parse_task.create(db, new_task)


@router.get(
    "/{task_id}", responses={200: {"model": schemas.parse_task.ParseTask}, 404: {}}
)
def get_parse_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> schemas.parse_task.ParseTask:
    return services.parse_task.get(db, task_id)
