from fastapi import Depends, FastAPI

from tagextractor import services
from tagextractor import dto
from tagextractor.db import init_db

app = FastAPI(title="tag-extractor", version="0.1")


@app.on_event("startup")
async def startup():
    await init_db()


@app.post(
    "/tasks/parse_page",
    responses={201: {"model": dto.ParseTaskCreated}, 403: {}, 404: {}},
    status_code=201,
)
async def create_parse_task(
    new_task: dto.ParseTaskCreate,
    parse_task_service: services.ParseTaskService = Depends(),
) -> dto.ParseTaskCreated:
    return await parse_task_service.create(new_task)


@app.get("/task/{task_id}", responses={200: {"model": dto.ParseTask}, 404: {}})
async def get_task(
    task_id: int,
    parse_task_service: services.ParseTaskService = Depends(),
) -> dto.ParseTask:
    return await parse_task_service.get_by_id(task_id)
