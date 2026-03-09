from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.task import CreateTaskRequest, UpdateTaskRequest, TaskResponse
from app.models.task import Task
from app.models.user import User
from app.core.dependencies import get_current_user
from app.tasks import send_task_created_notification
from typing import Optional


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    query = Task.find()

    if status_filter:
        query = Task.find(Task.status == status_filter)

    if priority_filter:
        query = query.find(Task.priority == priority_filter)

    skip = (page - 1) * limit
    tasks = await query.skip(skip).limit(limit).to_list()

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
        status=data.status,
        created_by=str(current_user.id)
    )
    await task.insert()

    send_task_created_notification.delay(
        task_id=str(task.id),
        task_title=task.title,
        user_email=current_user.email
    )

    return TaskResponse.from_task(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, data: UpdateTaskRequest, current_user: User = Depends(get_current_user)):
    task = await Task.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    task.title = data.title
    task.description = data.description
    task.priority = data.priority
    task.status = data.status
    await task.save()

    return TaskResponse.from_task(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, current_user: User = Depends(get_current_user)):
    task = await Task.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    await task.delete()
    return {"message": "Task deleted successfully"}