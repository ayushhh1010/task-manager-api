from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


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
    id: str
    title: str
    description: Optional[str]
    priority: TaskPriority
    status: TaskStatus
