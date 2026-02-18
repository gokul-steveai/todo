from pydantic import BaseModel, Field
from models.todo import Status

class CreateToDoItem(BaseModel):
    title: str = Field(..., description="Title of the to-do item", example="Buy groceries", max_length=100)
    description: str | None = Field(default=None, description="Optional description of the to-do item", example="Milk, Bread, Eggs", max_length=200)
    
    model_config = {'extra': 'forbid'}

class ToDoItem(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    status: Status = Status.PENDING
    completed: bool = False