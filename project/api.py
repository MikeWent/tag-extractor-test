from fastapi import FastAPI
from project import routers

app = FastAPI(title="tag-extractor", version="1")
app.include_router(routers.v1.router, prefix="/v1")
