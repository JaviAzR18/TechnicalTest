from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
    favorite: bool = False

class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    favorite: bool | None = None

class Todo(TodoBase):
    id: int = Field(..., ge=1)
