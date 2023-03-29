from fastapi import APIRouter
from .endpoints import parse_task

router = APIRouter()
router.include_router(parse_task.router, tags=["parse_tasks"])
