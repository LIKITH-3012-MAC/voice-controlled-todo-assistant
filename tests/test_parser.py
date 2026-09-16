import unittest
from app.models import Intent
from app.nlp.parser import CommandParser


class TestCommandParser(unittest.TestCase):
    def setUp(self):
        self.parser = CommandParser()

    def test_add_todo(self):
        command = self.parser.parse("Add complete NLP assignment tomorrow")
        self.assertEqual(command.intent, Intent.ADD_TODO)
        self.assertEqual(command.task, "complete nlp assignment")
        self.assertIsNotNone(command.due_date)

    def test_list(self):
        command = self.parser.parse("Show my tasks")
        self.assertEqual(command.intent, Intent.LIST_TODOS)

    def test_complete(self):
        command = self.parser.parse("Complete study DSA")
        self.assertEqual(command.intent, Intent.COMPLETE_TODO)
        self.assertEqual(command.task, "study dsa")

    def test_delete(self):
        command = self.parser.parse("Delete DBMS assignment")
        self.assertEqual(command.intent, Intent.DELETE_TODO)

    def test_clear(self):
        command = self.parser.parse("Clear all tasks")
        self.assertEqual(command.intent, Intent.CLEAR_TODOS)

    def test_exit(self):
        command = self.parser.parse("Exit")
        self.assertEqual(command.intent, Intent.EXIT)


if __name__ == "__main__":
    unittest.main()
