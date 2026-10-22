from fastapi import APIRouter, HTTPException, status

from app.models import Todo, TodoCreate, TodoUpdate
from app.repository import TodoRepository

router = APIRouter(prefix="/todos", tags=["todos"])
repository = TodoRepository()


@router.get("", response_model=list[Todo])
def get_todos() -> list[Todo]:
    return repository.get_all()


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED)
def add_todo(todo: TodoCreate) -> Todo:
    return repository.add(todo)


@router.patch("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoUpdate) -> Todo:
    updated = repository.update(todo_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return updated

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int) -> None:
    deleted = repository.delete(todo_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")