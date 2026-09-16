# 🎙️ Voice-Controlled Todo List Assistant

<div align="center">

### 🧠 Speak Naturally. Understand Intelligently. Get Things Done.

**An NLP-powered voice assistant that transforms natural language commands into actionable Todo operations.**

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Intent%20%26%20Entity%20Extraction-8A2BE2?style=for-the-badge)
![Speech](https://img.shields.io/badge/Speech-Recognition-00A67E?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-Unittest-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-black?style=for-the-badge)

<br>

> 🎤 **"Add complete my NLP assignment tomorrow."**

↓

> 🧠 **Intent:** `ADD_TODO`
> 📝 **Task:** `complete my NLP assignment`
> 📅 **Due:** `Tomorrow`

↓

> ✅ **Task Added Successfully**

</div>

---

## ✨ What Is This?

**Voice-Controlled Todo List Assistant** is an NLP laboratory project that allows users to manage their Todo list using **natural voice commands**.

Instead of clicking buttons or typing commands, the user simply speaks naturally.

```text
                 🎙️ USER VOICE
                       │
                       ▼
              ┌─────────────────┐
              │ Speech-to-Text  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ NLP Processing  │
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
        🎯 Intent          🧩 Entities
        Detection          Extraction
              │                 │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Todo Service    │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ JSON Storage    │
              └─────────────────┘
```

The core idea is simple:

> **Human Language → NLP Understanding → Structured Action**

---

# 🚀 Features

| Feature                  | Description                                   |
| ------------------------ | --------------------------------------------- |
| 🎤 Voice Commands        | Control the Todo list using speech            |
| ⌨️ Text Mode             | Keyboard fallback for reliable demonstrations |
| 🧠 NLP Processing        | Normalize and tokenize natural language       |
| 🎯 Intent Detection      | Understand what the user wants                |
| 🧩 Entity Extraction     | Extract task names and dates                  |
| 📅 Date Understanding    | Supports today, tomorrow and weekdays         |
| ➕ Add Tasks              | Create new Todo items                         |
| 📋 List Tasks            | Display all saved tasks                       |
| ✅ Complete Tasks         | Mark tasks as completed                       |
| 🗑️ Delete Tasks         | Remove individual tasks                       |
| 🧹 Clear Tasks           | Remove the entire Todo list                   |
| 🔊 Text-to-Speech        | Assistant responds using voice                |
| 💾 Persistence           | Tasks survive application restarts            |
| 🧪 Unit Tests            | Automated parser and service tests            |
| 📜 Logging               | Application events and errors are logged      |
| 🏗️ Layered Architecture | Separates NLP, business logic and storage     |

---

# 🧠 NLP Pipeline

This project demonstrates the fundamental NLP workflow.

## 1️⃣ Speech Recognition

The user's voice is converted into text.

```text
🎤 "Add study DSA tomorrow"

                ↓

"Add study DSA tomorrow"
```

---

## 2️⃣ Text Normalization

The text is converted into a consistent format.

```text
"ADD!!! Study DSA Tomorrow"

                ↓

"add study dsa tomorrow"
```

This removes unnecessary punctuation and normalizes the text.

---

## 3️⃣ Tokenization

The sentence is divided into individual tokens.

```text
"add study dsa tomorrow"

                ↓

["add", "study", "dsa", "tomorrow"]
```

---

## 4️⃣ Intent Detection

The system determines **what the user wants to do**.

```text
"add study dsa tomorrow"

                ↓

Intent = ADD_TODO
```

Supported intents:

```text
ADD_TODO
LIST_TODOS
COMPLETE_TODO
DELETE_TODO
CLEAR_TODOS
HELP
EXIT
UNKNOWN
```

---

## 5️⃣ Entity Extraction

Important information is extracted from the sentence.

```text
"add complete nlp assignment tomorrow"

                ↓

Task:
"complete nlp assignment"

Date:
"tomorrow"
```

The system resolves relative dates into actual dates.

Example:

```text
tomorrow
      ↓
2026-09-17
```

---

## 6️⃣ Structured Command

The natural language is converted into a structured representation.

```text
{
    "intent": "ADD_TODO",
    "task": "complete nlp assignment",
    "due_date": "2026-09-17"
}
```

---

## 7️⃣ Action

The Todo service executes the requested operation.

```text
ADD_TODO
   ↓
Create Todo
   ↓
Save to JSON
   ↓
Return response
```

---

# 🎙️ Voice Command Examples

### ➕ Add a Todo

```text
"Add complete NLP assignment tomorrow"
```

Result:

```text
✅ Added task: complete nlp assignment
📅 Due: 2026-09-17
```

---

### 📋 List Todos

```text
"Show my tasks"
```

Result:

```text
📋 TODO LIST

1. ☐ complete nlp assignment
2. ☐ study DSA
3. ☐ prepare for viva
```

---

### ✅ Complete a Todo

```text
"Complete study DSA"
```

Result:

```text
✅ Completed: study DSA
```

---

### 🗑️ Delete a Todo

```text
"Delete study DSA"
```

Result:

```text
🗑️ Deleted: study DSA
```

---

### 🧹 Clear Everything

```text
"Clear all tasks"
```

Result:

```text
🧹 All tasks have been cleared.
```

---

# 🏗️ System Architecture

```text
┌────────────────────────────────────────────────────┐
│                    USER INPUT                      │
│                                                    │
│            🎤 Voice / ⌨️ Keyboard                 │
└────────────────────────┬───────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────┐
│               SPEECH PROCESSING                    │
│                                                    │
│          SpeechRecognition / STT                  │
└────────────────────────┬───────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────┐
│                   NLP LAYER                        │
│                                                    │
│  Normalization → Tokenization → Intent Detection │
│                              ↓                     │
│                       Entity Extraction            │
└────────────────────────┬───────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────┐
│                 SERVICE LAYER                      │
│                                                    │
│       Add / List / Complete / Delete / Clear      │
└────────────────────────┬───────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────┐
│                REPOSITORY LAYER                    │
│                                                    │
│                   JSON Storage                     │
└────────────────────────────────────────────────────┘
```

---

# 📁 Project Structure

```text
voice-controlled-todo-assistant/
│
├── 📂 app/
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   │
│   ├── 📂 nlp/
│   │   ├── __init__.py
│   │   ├── preprocessing.py
│   │   └── parser.py
│   │
│   ├── 📂 repositories/
│   │   ├── __init__.py
│   │   └── todo_repository.py
│   │
│   ├── 📂 services/
│   │   ├── __init__.py
│   │   └── todo_service.py
│   │
│   └── 📂 voice/
│       ├── __init__.py
│       ├── speech_to_text.py
│       └── text_to_speech.py
│
├── 📂 data/
│   └── todos.json
│
├── 📂 tests/
│   ├── test_parser.py
│   └── test_service.py
│
├── 📜 requirements.txt
├── 📜 README.md
└── 📜 assistant.log
```

---

# 🧩 Technology Stack

### Programming Language

```text
Python 3.10+
```

### NLP

```text
Text Normalization
Tokenization
Rule-Based Intent Detection
Entity Extraction
Regular Expressions
```

### Speech

```text
SpeechRecognition
Google Speech Recognition
PyAudio
```

### Text-to-Speech

```text
pyttsx3
```

### Storage

```text
JSON
```

### Testing

```text
Python unittest
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/voice-controlled-todo-assistant.git
```

```bash
cd voice-controlled-todo-assistant
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Run:

```bash
python -m app.main
```

You will see:

```text
============================================================
🎙️  VOICE-CONTROLLED TODO LIST ASSISTANT
    NLP Laboratory Experiment — Batch 6
============================================================

1. 🎤 Voice mode
2. ⌨️  Text mode
3. 🚪 Exit

Select:
```

---

# 🎤 Voice Mode

Choose:

```text
1
```

Then speak:

```text
"Add complete NLP assignment tomorrow"
```

The assistant processes the command and responds.

```text
🎤 Listening...

🗣️ You said:
Add complete NLP assignment tomorrow

🤖 Assistant:
Added task: complete nlp assignment.
Due on 2026-09-17.
```

---

# ⌨️ Text Mode

For a classroom demonstration, Text Mode provides a reliable fallback.

Choose:

```text
2
```

Then type:

```text
Add study DSA tomorrow
```

or:

```text
Show my tasks
```

---

# 🧪 Testing

Run all tests:

```bash
python -m unittest discover -s tests -v
```

Expected output:

```text
test_add_todo ... ok
test_clear ... ok
test_complete ... ok
test_delete ... ok
test_exit ... ok
test_list ... ok

----------------------------------------------------------------------
Ran 6 tests

OK
```

---

# 💾 Data Persistence

Todos are stored inside:

```text
data/todos.json
```

Example:

```json
[
  {
    "id": 1,
    "title": "complete nlp assignment",
    "due_date": "2026-09-17",
    "completed": false,
    "created_at": "2026-09-16T19:20:00"
  }
]
```

Because the data is persisted, restarting the application does not automatically remove existing tasks.

---

# 🧱 Architecture Principles

The project uses a simple layered architecture.

### `voice/`

Responsible for:

```text
Speech → Text
Text → Speech
```

### `nlp/`

Responsible for:

```text
Text preprocessing
Intent detection
Entity extraction
```

### `services/`

Responsible for:

```text
Business logic
Todo operations
```

### `repositories/`

Responsible for:

```text
Reading and writing Todo data
```

### `models.py`

Defines the application's data structures.

### `main.py`

Connects all components and handles the application flow.

---

# 🔬 NLP Concepts Covered

This project can be presented as an NLP laboratory experiment because it demonstrates:

```text
                    NLP
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
  Preprocessing   Intent       Entities
                 Detection     Extraction
        │            │            │
        ▼            ▼            ▼
   Normalize      ADD_TODO      Task
   Tokenize       DELETE_TODO   Date
                  COMPLETE
                  LIST
```

---

# 🎓 Viva Questions

### Q1. What is NLP?

**Answer:**

Natural Language Processing is a branch of Artificial Intelligence that enables computers to process and understand human language.

---

### Q2. Where is NLP used in this project?

**Answer:**

NLP is used after speech-to-text conversion. The system preprocesses the text, identifies the user's intent and extracts important entities such as the task name and due date.

---

### Q3. What is Intent Detection?

**Answer:**

Intent detection determines what action the user wants to perform.

Example:

```text
"Show my tasks"

        ↓

LIST_TODOS
```

---

### Q4. What is Entity Extraction?

**Answer:**

Entity extraction identifies useful information from the user's sentence.

Example:

```text
"Add study DSA tomorrow"

Task → study DSA
Date → tomorrow
```

---

### Q5. Why do we need Speech-to-Text?

**Answer:**

The NLP system works on text, so Speech-to-Text converts the user's spoken command into text before NLP processing.

---

### Q6. Why use JSON?

**Answer:**

JSON provides simple persistent storage for this small laboratory project. It can later be replaced by a relational database such as PostgreSQL or MySQL.

---

### Q7. Is this Machine Learning?

**Answer:**

The current version primarily uses **rule-based NLP**, not a trained machine-learning classifier. This makes the intent detection transparent and easy to demonstrate in a laboratory setting.

---

# ⚡ Example End-to-End Flow

Input:

```text
🎤 "Please add my DBMS assignment tomorrow"
```

### Step 1 — Speech Recognition

```text
"Please add my DBMS assignment tomorrow"
```

### Step 2 — Normalization

```text
"please add my dbms assignment tomorrow"
```

### Step 3 — Tokenization

```text
[
  "please",
  "add",
  "my",
  "dbms",
  "assignment",
  "tomorrow"
]
```

### Step 4 — Intent

```text
ADD_TODO
```

### Step 5 — Entities

```text
Task:
dbms assignment

Due:
tomorrow
```

### Step 6 — Structured Command

```text
{
    "intent": "ADD_TODO",
    "task": "dbms assignment",
    "due_date": "2026-09-17"
}
```

### Step 7 — Database

```text
Todo Created
```

### Step 8 — Response

```text
🤖 "Added task: dbms assignment.
    Due on 2026-09-17."
```

---

# 🛡️ Error Handling

The application handles common runtime problems such as:

* Invalid commands
* Unknown intents
* Missing task names
* Microphone failures
* Speech recognition failures
* Invalid JSON data
* Text-to-speech unavailability

Example:

```text
🎤 "asdfghjkl"

        ↓

UNKNOWN

        ↓

🤖 "I did not understand that.
    Try: add a task, show tasks,
    complete a task, or delete a task."
```

---

# 📊 Why This Project?

Traditional Todo applications require users to interact with graphical interfaces.

This project explores a more natural interaction model:

```text
Traditional

User → Keyboard → UI → Button → Todo
```

versus:

```text
Voice Assistant

User → Voice → NLP → Intent → Todo
```

The second approach demonstrates how **Natural Language Interfaces** can be built using fundamental NLP techniques.

---

# 🔮 Future Enhancements

The architecture can be extended with:

### 🧠 Advanced NLP

* Machine-learning intent classifier
* Transformer-based classification
* BERT embeddings
* Semantic similarity
* Named Entity Recognition

### 🎙️ Better Speech Recognition

* Local Whisper
* Offline speech recognition
* Telugu + English commands
* Multilingual support

### 🗄️ Database

Replace JSON with:

```text
PostgreSQL
MySQL
MongoDB
```

### 🌐 API

Add:

```text
FastAPI
REST APIs
Authentication
```

### 📅 Smart Scheduling

Integrate:

```text
Calendar
Reminders
Recurring Tasks
Priority Detection
```

### 🤖 Intelligent Assistant

Future versions could understand commands such as:

```text
"Show me everything I need to finish this week"

"What's overdue?"

"Move my DBMS assignment to Friday"

"Mark all today's tasks as completed"
```

---

# 📈 Project Evolution

```text
Version 1
   │
   ├── Basic Todo CRUD
   │
   ▼
Version 2
   │
   ├── NLP preprocessing
   ├── Intent detection
   └── Entity extraction
   │
   ▼
Version 3
   │
   ├── Voice input
   └── Voice output
   │
   ▼
Version 4
   │
   ├── ML intent classifier
   ├── Semantic understanding
   └── Multilingual support
   │
   ▼
Future
   │
   └── 🤖 Intelligent Personal Assistant
```

---

# 👨‍💻 Author

<div align="center">

### **Likith Naidu**

**Computer Science & Engineering — Artificial Intelligence**

🎓 NLP Laboratory Project

</div>

---

# 📜 License

This project is licensed under the **MIT License**.

---

<div align="center">

## 🎙️ Speak Naturally.

### 🧠 Let NLP Understand.

### ✅ Get Things Done.

<br>

**Built with Python + NLP + Speech Recognition**

⭐ Star the repository if you found it useful!

</div>
