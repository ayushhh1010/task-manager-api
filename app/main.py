from fastapi import FastAPI
from app.routers import tasks
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.models.task import Task

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Task])
    yield

app = FastAPI(title="Task Manager API")

app.include_router(tasks.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Welcome to the Task Manager API"}


