import logging

from app.config import TODO_FILE, LOG_FILE
from app.models import Intent
from app.nlp.parser import CommandParser
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService
from app.voice.text_to_speech import TextToSpeech


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


class TodoAssistant:
    def __init__(self):
        self.parser = CommandParser()
        self.service = TodoService(TodoRepository(TODO_FILE))
        self.tts = TextToSpeech(enabled=True)

    def execute(self, text: str) -> bool:
        command = self.parser.parse(text)
        logging.info("Input=%r Intent=%s Task=%r Due=%r",
                     text, command.intent.value, command.task, command.due_date)

        if command.intent == Intent.EXIT:
            self.tts.speak("Goodbye. Have a productive day!")
            return False

        if command.intent == Intent.UNKNOWN:
            self.tts.speak(
                "I did not understand that. Try: add a task, show tasks, "
                "complete a task, delete a task, or clear all tasks."
            )
            return True

        if command.intent == Intent.HELP:
            self.tts.speak(
                "You can say: add study DSA tomorrow, show my tasks, "
                "complete study DSA, delete study DSA, or clear all tasks."
            )
            return True

        if command.intent == Intent.ADD_TODO:
            if not command.task:
                self.tts.speak("Please tell me the task you want to add.")
                return True
            todo = self.service.add_task(command.task, command.due_date)
            due = f" Due on {todo.due_date}." if todo.due_date else ""
            self.tts.speak(f"Added task: {todo.title}.{due}")
            return True

        if command.intent == Intent.LIST_TODOS:
            todos = self.service.list_tasks()
            if not todos:
                self.tts.speak("Your todo list is empty.")
                return True

            print("\n📋 TODO LIST")
            for todo in todos:
                status = "✓" if todo.completed else "☐"
                due = f" — due {todo.due_date}" if todo.due_date else ""
                print(f"{todo.id}. {status} {todo.title}{due}")
            print()
            return True

        if command.intent == Intent.COMPLETE_TODO:
            if not command.task:
                self.tts.speak("Please tell me which task to complete.")
                return True
            todo = self.service.complete_task(command.task)
            self.tts.speak(
                f"Completed: {todo.title}." if todo
                else f"I could not find the task '{command.task}'."
            )
            return True

        if command.intent == Intent.DELETE_TODO:
            if not command.task:
                self.tts.speak("Please tell me which task to delete.")
                return True
            todo = self.service.delete_task(command.task)
            self.tts.speak(
                f"Deleted: {todo.title}." if todo
                else f"I could not find the task '{command.task}'."
            )
            return True

        if command.intent == Intent.CLEAR_TODOS:
            self.service.clear_tasks()
            self.tts.speak("All tasks have been cleared.")
            return True

        return True


def run_text_mode(assistant: TodoAssistant):
    print("\n⌨️  TEXT MODE — type a command.")
    print("Example: add complete NLP assignment tomorrow")
    print("Type 'help' for commands.\n")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if text and not assistant.execute(text):
            break


def run_voice_mode(assistant: TodoAssistant):
    from app.voice.speech_to_text import SpeechToText

    try:
        stt = SpeechToText()
    except RuntimeError as exc:
        print(f"⚠️ {exc}")
        print("Starting text mode instead.")
        run_text_mode(assistant)
        return

    print("\n🎙️ VOICE MODE")
    print("Say 'help' for commands or 'exit' to stop.\n")

    while True:
        try:
            text = stt.listen()
        except Exception as exc:
            logging.exception("Microphone failure")
            print(f"⚠️ Microphone error: {exc}")
            continue

        if text and not assistant.execute(text):
            break


def main():
    print("=" * 60)
    print("🎙️  VOICE-CONTROLLED TODO LIST ASSISTANT")
    print("    NLP Laboratory Experiment — Batch 6")
    print("=" * 60)

    assistant = TodoAssistant()

    while True:
        print("\n1. 🎤 Voice mode")
        print("2. ⌨️  Text mode")
        print("3. 🚪 Exit")

        choice = input("\nSelect: ").strip()

        if choice == "1":
            run_voice_mode(assistant)
        elif choice == "2":
            run_text_mode(assistant)
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
