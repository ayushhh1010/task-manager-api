from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pydantic import Field
from typing import Optional
from datetime import datetime
from app.schemas.task import TaskPriority, TaskStatus

class Task(Document):
    title: str
    description: Optional[str]=None
    priority: TaskPriority= TaskPriority.medium
    status: TaskStatus = TaskStatus.pending
    created_by: Optional[str] = None
    created_at: datetime= Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tasks"

