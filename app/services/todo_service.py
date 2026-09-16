from app.models import Todo
from app.repositories.todo_repository import TodoRepository


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def add_task(self, title: str, due_date: str | None = None) -> Todo:
        todos = self.repository.find_all()
        next_id = max((todo.id for todo in todos), default=0) + 1
        todo = Todo(id=next_id, title=title, due_date=due_date)
        return self.repository.add(todo)

    def list_tasks(self) -> list[Todo]:
        return self.repository.find_all()

    def _find_by_title(self, title: str, include_completed=False):
        query = title.lower().strip()
        candidates = self.repository.find_all()
        if not include_completed:
            candidates = [t for t in candidates if not t.completed]

        # Exact match first, then substring match.
        for todo in candidates:
            if todo.title.lower() == query:
                return todo

        for todo in candidates:
            if query in todo.title.lower() or todo.title.lower() in query:
                return todo

        return None

    def complete_task(self, title: str) -> Todo | None:
        todo = self._find_by_title(title)
        if not todo:
            return None
        todo.completed = True
        self.repository.update(todo)
        return todo

    def delete_task(self, title: str) -> Todo | None:
        todo = self._find_by_title(title, include_completed=True)
        if not todo:
            return None
        self.repository.delete(todo.id)
        return todo

    def clear_tasks(self) -> None:
        self.repository.clear()
