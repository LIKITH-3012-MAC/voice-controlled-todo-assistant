from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TODO_FILE = DATA_DIR / "todos.json"
LOG_FILE = BASE_DIR / "assistant.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)
