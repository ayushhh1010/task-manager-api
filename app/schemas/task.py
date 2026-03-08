from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class TaskPriority(str, Enum):
    low="low"
    medium="medium"
    high="high"


class TaskStatus(str, Enum):
    pending="pending"
    in_progress="in_progress"
    completed="completed"


class CreateTaskRequest(BaseModel):
    title: str = Field(...,min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: TaskPriority = TaskPriority.medium
    status: TaskStatus = TaskStatus.pending


class TaskResponse(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str]
    priority: TaskPriority
    status: TaskStatus
    created_at: Optional[datetime] =  None

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}

    @classmethod
    def from_task(cls, task):
        return cls(
            id= str(task.id),
            title= task.title,
            description= task.description,
            priority= task.priority,
            status= task.status,
            created_at= task.created_at
        )