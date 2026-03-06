from beanie import Document
from pydantic import Field
from typing import Optional
from datatime import datetime
from app.schemas.task import TaskPriority, TaskStatus

class Task(Document):
    title: str
    description: Optional[str]=None
    priority: TaskPriority= TaskPriority.medium
    status: TaskStatus = TaskStatus.pending
    created_at: datetime= Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tasks"

