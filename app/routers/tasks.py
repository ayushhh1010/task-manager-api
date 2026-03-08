from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.task import CreateTaskRequest, TaskResponse
from app.models.task import Task
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/", response_model=list[TaskResponse])
async def get_tasks(current_user: User = Depends(get_current_user)):
    tasks = await Task.find_all().to_list()
    return [TaskResponse.from_task(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, current_user: User = Depends(get_current_user)):
    task= await Task.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse.from_task(task)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= TaskResponse)
async def create_task(data: CreateTaskRequest, current_user: User=Depends(get_current_user)):
    task = Task(
        title=data.title,
        description=data.description,
        priority=data.priority,
        status=data.status
    )
    await task.insert()
    return TaskResponse.from_task(task)
