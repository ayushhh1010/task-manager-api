from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class User(Document):
    email: str
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"