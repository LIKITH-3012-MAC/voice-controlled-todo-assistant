import tempfile
import unittest
from pathlib import Path

from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService


class TestTodoService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        path = Path(self.temp_dir.name) / "todos.json"
        self.service = TodoService(TodoRepository(path))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_crud(self):
        todo = self.service.add_task("learn nlp", "2026-09-17")
        self.assertEqual(len(self.service.list_tasks()), 1)

        completed = self.service.complete_task("learn nlp")
        self.assertTrue(completed.completed)

        deleted = self.service.delete_task("learn nlp")
        self.assertEqual(deleted.id, todo.id)
        self.assertEqual(len(self.service.list_tasks()), 0)


if __name__ == "__main__":
    unittest.main()
