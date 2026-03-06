from fastapi import APIRouter, HTTPException, status
from app.schemas.task import CreateTaskRequest

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/")
def get_tasks(status_filter: str= "all", limit: int =10):
    return {
        "status_filter": status_filter,
        "limit": limit
    }


@router.get("/{task_id}")
def get_task(task_id: str):
    return { "task_id": task_id}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTaskRequest):
    return {
        "message": "Task Created",
        "task_title": task.title,
        "task_priority": task.priority
    }