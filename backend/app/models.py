from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    title: str
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class Todo(TodoBase):
    id: int = Field(..., ge=1)
