import subprocess

from fastapi import FastAPI
from contextlib import asynccontextmanager

from project import routers
from project.db import init_db, dispose_db

app = FastAPI(title="tag-extractor", version="1.1")
app.include_router(routers.v1.router, prefix="/v1")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await dispose_db()
