from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from tagextractor import dto
from tagextractor import models
from tagextractor.db import AsyncSession, get_session


class ParseTaskService(object):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def create(self, dto: dto.ParseTaskCreate) -> models.ParseTask:
        new_task = models.ParseTask(**dto.dict())
        existing_task: models.ParseTask = (
            await self.session.execute(
                select(models.ParseTask)
                .where(models.ParseTask.url == new_task.url)
                .where(models.ParseTask.status != models.ParseTask.TaskStatus.FINISHED),
            )
        ).scalar()
        if existing_task:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unfinished task with the same URL already exists.",
            )
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        return new_task

    async def get_by_id(self, task_id: int) -> models.ParseTask:
        task: models.ParseTask = await self.session.get(models.ParseTask, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found.",
            )
        return task
