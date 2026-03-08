from fastapi import FastAPI
from app.routers import tasks, auth
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.models.task import Task
from app.models.user import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Task, User])
    yield

app = FastAPI(title="Task Manager API", lifespan= lifespan)

app.include_router(tasks.router)
app.include_router(auth.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Welcome to the Task Manager API"}


