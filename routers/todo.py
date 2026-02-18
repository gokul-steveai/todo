from fastapi import APIRouter, status, Response, Depends, HTTPException
from typing import Annotated
from utils import not_found_response
from schemas.todo import ToDoItem, CreateToDoItem
from utils import get_current_user_id
from sqlmodel import Session, select, delete
from models.connect import get_session
from models.todo import Todo, Status
from models.user import User


router = APIRouter(prefix="/todos", tags=["To-Do Operations"],dependencies=[Depends(get_current_user_id)])

TO_DOs: list[ToDoItem] = [
    ToDoItem(id=1, title="Buy groceries", description="Milk, Bread, Eggs", status=Status.PENDING, completed=False),
]

@router.get("", status_code=status.HTTP_200_OK, response_model=list[ToDoItem])
def get_todos(user_id: Annotated[int, Depends(get_current_user_id)], session: Annotated[Session, Depends(get_session)], status: Status | None = None, page: int = 1, size: int = 10) -> list[ToDoItem]:
    filtered_todos = session.exec(select(Todo).where(Todo.user_id == user_id)).all()
    if status:
        filtered_todos = [todo for todo in filtered_todos if todo.status == status]
    return filtered_todos[(page-1)*size : page*size]


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
def update_status(todo_id: int, status: Status, response: Response, user_id: Annotated[int, Depends(get_current_user_id)], session: Annotated[Session, Depends(get_session)]) -> dict[str, str]:

    todo = fetch_todo_by_id__user_id(session, user_id=user_id, todo_id=todo_id)
    
    if not todo:
        return not_found_response(response, "To Do not found")
    
    todo.status = status
    todo.completed = (status == Status.COMPLETED)
    
    save_todo(todo=todo)
    return {"message": "Status updated successfully"}

@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(todo: CreateToDoItem, user_id: Annotated[int, Depends(get_current_user_id)], session: Annotated[Session, Depends(get_session)]) -> dict[str, str | ToDoItem]:
    new_todo = Todo(**todo.model_dump(), user_id=user_id)
    
    new_todo = save_todo(session, new_todo)
    return {"message": "To-Do created successfully", "todo": new_todo}

@router.post("/{todo_id}/toggle", status_code=status.HTTP_200_OK)
def toggle_completion(todo_id: int, response: Response, user_id: Annotated[int, Depends(get_current_user_id)], session: Annotated[Session, Depends(get_session)]):
    todo = fetch_todo_by_id__user_id(session, user_id=user_id, todo_id=todo_id)
    
    if not todo:
        return not_found_response(response, message="To Do not found")  
    
    todo.completed = not todo.completed
    todo.status = Status.COMPLETED if todo.completed else Status.PENDING
    todo = save_todo(session, todo=todo)
    return {"message": "To-Do completion toggled successfully", "todo": todo}
        

@router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(todo_id: int, response: Response, session: Annotated[Session, Depends(get_session)]):
    session.exec(delete(Todo).where(Todo.id == todo_id)).rowcount
    for index, todo in enumerate(TO_DOs):
        if todo.id == todo_id:
            del TO_DOs[index]
            return {"message": "To-Do deleted successfully"}
    
    return not_found_response(response)

def fetch_todo_by_id__user_id(session: Annotated[Session, Depends(get_session)],*, user_id: int, todo_id: int) -> (Todo | None):
    return session.exec(select(Todo).where(User.id == user_id, Todo.id == todo_id)).first()

def save_todo(*, session: Session = Depends(get_session), todo: Todo):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo