import json
from pathlib import Path
from app.models import Todo


class TodoRepository:
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write([])

    def _read(self) -> list[Todo]:
        try:
            raw = json.loads(self.file_path.read_text(encoding="utf-8"))
            return [Todo.from_dict(item) for item in raw]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write(self, todos: list[Todo]) -> None:
        payload = [todo.to_dict() for todo in todos]
        self.file_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def find_all(self) -> list[Todo]:
        return self._read()

    def add(self, todo: Todo) -> Todo:
        todos = self._read()
        todos.append(todo)
        self._write(todos)
        return todo

    def update(self, todo: Todo) -> None:
        todos = self._read()
        for index, existing in enumerate(todos):
            if existing.id == todo.id:
                todos[index] = todo
                break
        self._write(todos)

    def delete(self, todo_id: int) -> bool:
        todos = self._read()
        filtered = [todo for todo in todos if todo.id != todo_id]
        changed = len(filtered) != len(todos)
        self._write(filtered)
        return changed

    def clear(self) -> None:
        self._write([])
