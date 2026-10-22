import json
from pathlib import Path

from app.models import Todo, TodoCreate, TodoUpdate

DATA_FILE = Path(__file__).parent / "todos.json"


class TodoRepository:
    """JSON-file persistence for todos."""

    def get_all(self) -> list[Todo]:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return [Todo(**todo) for todo in json.load(f)]

    def get_by_id(self, todo_id: int) -> Todo | None:
        return next((todo for todo in self.get_all() if todo.id == todo_id), None)

    def add(self, payload: TodoCreate) -> Todo:
        todos = self.get_all()
        next_id = max((todo.id for todo in todos), default=0) + 1
        todo = Todo(id=next_id, **payload.model_dump())
        todos.append(todo)
        self._save(todos)
        return todo

    def update(self, todo_id: int, payload: TodoUpdate) -> Todo | None:
        todos = self.get_all()
        for index, todo in enumerate(todos):
            if todo.id != todo_id:
                continue
            updated = todo.model_copy(update=payload.model_dump(exclude_unset=True))
            todos[index] = updated
            self._save(todos)
            return updated
        return None

    def delete(self, todo_id: int) -> bool:
        pass

    def _save(self, todos: list[Todo]) -> None:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([todo.model_dump() for todo in todos], f, indent=2)
