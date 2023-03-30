import subprocess
import logging

from fastapi import FastAPI

from project import routers
from project.db import init_db, dispose_db

app = FastAPI(title="tag-extractor", version="1.2")
app.include_router(routers.v1.router, prefix="/v1")


@app.on_event("startup")
async def startup():
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    await dispose_db()
