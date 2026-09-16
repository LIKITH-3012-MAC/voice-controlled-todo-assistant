# 🎙️ Voice-Controlled Todo List Assistant

A production-style NLP lab project that converts voice commands into structured Todo actions.

## Features
- 🎤 Voice input using `SpeechRecognition` + Google Speech Recognition
- ⌨️ Text fallback for offline classroom demos
- 🧠 NLP pipeline: normalization, tokenization, intent detection, entity extraction
- Intents: `ADD_TODO`, `LIST_TODOS`, `COMPLETE_TODO`, `DELETE_TODO`, `CLEAR_TODOS`, `HELP`, `EXIT`
- Relative date extraction: today, tomorrow, weekdays
- Persistent JSON storage
- Text-to-speech response with optional `pyttsx3`
- Clean layered architecture
- Unit tests
- Logging and error handling

## Architecture

```text
Microphone / Keyboard
        ↓
 Speech-to-Text
        ↓
 TextPreprocessor
        ↓
 IntentDetector + EntityExtractor
        ↓
 CommandRouter
        ↓
 TodoService
        ↓
 JSON Repository
        ↓
 Human-readable response
```

## Project Structure

```text
voice_todo_assistant/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── preprocessing.py
│   │   └── parser.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── todo_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── todo_service.py
│   └── voice/
│       ├── __init__.py
│       ├── speech_to_text.py
│       └── text_to_speech.py
├── data/
│   └── todos.json
├── tests/
│   ├── test_parser.py
│   └── test_service.py
├── requirements.txt
└── README.md
```

## Setup

Python 3.10+ recommended.

```bash
python -m venv .venv
```

### macOS/Linux
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python -m app.main
```

Choose:
- `1` Voice mode
- `2` Text mode
- `3` Exit

### Demo commands

```text
Add complete NLP assignment tomorrow
Add study DSA at 7 PM
Show my tasks
Complete NLP assignment
Delete DSA
Clear all tasks
Help
Exit
```

For a reliable classroom demonstration, start with **Text mode**, then demonstrate Voice mode if the microphone and internet speech-recognition service are available.

## NLP Concepts Demonstrated

### 1. Normalization
```text
"ADD!!! Complete NLP Assignment Tomorrow"
→ "add complete nlp assignment tomorrow"
```

### 2. Tokenization
```text
"add complete nlp assignment"
→ ["add", "complete", "nlp", "assignment"]
```

### 3. Intent Detection
```text
"show my tasks"
→ LIST_TODOS
```

### 4. Entity Extraction
```text
"add complete nlp assignment tomorrow"
→ task = "complete nlp assignment"
→ due_date = tomorrow
```

### 5. Command Execution
The structured command is passed to the service layer, which performs CRUD operations.

## Notes on Voice Recognition

`SpeechRecognition` uses Google's online speech recognition endpoint in this implementation, so voice recognition requires an internet connection. Text mode does not require that service and is ideal as a fallback during a lab demo.

## Testing

```bash
python -m unittest discover -s tests -v
```

## Example Output

```text
You: Add complete NLP assignment tomorrow

Assistant: Added task: complete NLP assignment
           Due: 2026-09-17

You: Show my tasks

1. ☐ complete NLP assignment — 2026-09-17
```

## Viva Explanation

**Q: What is the role of NLP?**  
NLP converts natural human language into structured information that the application can understand and act upon.

**Q: What is intent detection?**  
It identifies what the user wants to do, such as adding, deleting, listing, or completing a task.

**Q: What are entities?**  
Entities are useful pieces of information extracted from the command, such as the task name and due date.

**Q: What happens after speech recognition?**  
The speech is converted to text. The NLP pipeline normalizes and tokenizes the text, identifies the intent, extracts entities, and sends a structured command to the Todo service.

**Q: Why use a repository layer?**  
It separates data persistence from business logic, making the application easier to test and extend.

## Production Extension Ideas

- Replace Google Speech Recognition with local Whisper
- Replace JSON storage with PostgreSQL
- Add authentication
- Add FastAPI REST endpoints
- Add a trained transformer intent classifier
- Add calendar integration
- Add multilingual Telugu/English voice commands
# voice-controlled-todo-assistant
