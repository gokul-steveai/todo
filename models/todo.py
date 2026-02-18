from sqlmodel import SQLModel, Field
from enum import Enum

class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    user_id: int = Field(foreign_key="user.id", index=True)
    completed: bool = False
    status: Status = Status.PENDING