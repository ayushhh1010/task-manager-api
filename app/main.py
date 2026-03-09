from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.routers import tasks, auth
from app.core.database import init_db
from app.models.task import Task
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Task, User])
    yield

app = FastAPI(title="Task Manager API", lifespan= lifespan)

app.include_router(tasks.router)
app.include_router(auth.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error on {request.method} {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An Unexpected Error Occured. Please try again later."}
    )

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Welcome to the Task Manager API"}


