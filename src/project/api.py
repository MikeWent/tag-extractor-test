import subprocess

from fastapi import FastAPI
from project import routers

app = FastAPI(title="tag-extractor", version="1.1")
app.include_router(routers.v1.router, prefix="/v1")


@app.on_event("startup")
def apply_alembic_migrations_before_start():
    subprocess.run(["python3", "-m", "alembic", "upgrade", "head"])
