# ============================================================
# SAKRA TODO AI
# Voice-Controlled Todo List Assistant
# Native Streamlit UI
# NLP Laboratory Experiment — Batch 6
#
# Existing project layers preserved:
#   NLP Parser
#   Todo Service
#   Todo Repository
#   Speech-to-Text
#   Text-to-Speech
#   JSON Persistence
#
# UI uses native Streamlit components only.
# ============================================================

import sys
import logging
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH FIX
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# EXISTING PROJECT IMPORTS
# ============================================================

from app.config import TODO_FILE, LOG_FILE
from app.models import Intent
from app.nlp.parser import CommandParser
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService
from app.voice.text_to_speech import TextToSpeech


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sakra Todo AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# TODO ASSISTANT
# ============================================================

class TodoAssistant:

    def __init__(self):
        self.parser = CommandParser()
        self.service = TodoService(
            TodoRepository(TODO_FILE)
        )
        self.tts = TextToSpeech(enabled=True)

    # --------------------------------------------------------
    # PROCESS COMMAND
    # --------------------------------------------------------

    def process_command(self, text: str):

        text = text.strip()

        if not text:
            return {
                "success": False,
                "message": "Please enter a command.",
                "intent": "EMPTY",
            }

        try:

            command = self.parser.parse(text)

            logging.info(
                "Input=%r Intent=%s Task=%r Due=%r",
                text,
                command.intent.value,
                command.task,
                command.due_date,
            )

            # ------------------------------------------------
            # EXIT
            # ------------------------------------------------

            if command.intent == Intent.EXIT:

                message = (
                    "Goodbye. Have a productive day!"
                )

                self.tts.speak(message)

                return {
                    "success": True,
                    "message": message,
                    "intent": "EXIT",
                }

            # ------------------------------------------------
            # UNKNOWN
            # ------------------------------------------------

            if command.intent == Intent.UNKNOWN:

                message = (
                    "I did not understand that. "
                    "Try adding, showing, completing, "
                    "deleting, or clearing tasks."
                )

                self.tts.speak(message)

                return {
                    "success": False,
                    "message": message,
                    "intent": "UNKNOWN",
                }

            # ------------------------------------------------
            # HELP
            # ------------------------------------------------

            if command.intent == Intent.HELP:

                message = (
                    "Try commands such as: "
                    "add study DSA tomorrow, "
                    "show my tasks, "
                    "complete study DSA, "
                    "delete study DSA, "
                    "or clear all tasks."
                )

                self.tts.speak(message)

                return {
                    "success": True,
                    "message": message,
                    "intent": "HELP",
                }

            # ------------------------------------------------
            # ADD TODO
            # ------------------------------------------------

            if command.intent == Intent.ADD_TODO:

                if not command.task:

                    message = (
                        "Please tell me the task "
                        "you want to add."
                    )

                    self.tts.speak(message)

                    return {
                        "success": False,
                        "message": message,
                        "intent": "ADD_TODO",
                    }

                todo = self.service.add_task(
                    command.task,
                    command.due_date,
                )

                due = (
                    f" Due on {todo.due_date}."
                    if todo.due_date
                    else ""
                )

                message = (
                    f"Added task: {todo.title}.{due}"
                )

                self.tts.speak(message)

                return {
                    "success": True,
                    "message": message,
                    "intent": "ADD_TODO",
                    "todo": todo,
                }

            # ------------------------------------------------
            # LIST TODOS
            # ------------------------------------------------

            if command.intent == Intent.LIST_TODOS:

                todos = self.service.list_tasks()

                if not todos:
                    message = (
                        "Your todo list is empty."
                    )
                else:
                    message = (
                        f"You have {len(todos)} task(s)."
                    )

                self.tts.speak(message)

                return {
                    "success": True,
                    "message": message,
                    "intent": "LIST_TODOS",
                    "todos": todos,
                }

            # ------------------------------------------------
            # COMPLETE TODO
            # ------------------------------------------------

            if command.intent == Intent.COMPLETE_TODO:

                if not command.task:

                    message = (
                        "Please tell me which task "
                        "to complete."
                    )

                    self.tts.speak(message)

                    return {
                        "success": False,
                        "message": message,
                        "intent": "COMPLETE_TODO",
                    }

                todo = self.service.complete_task(
                    command.task
                )

                if todo:

                    message = (
                        f"Completed: {todo.title}."
                    )

                    self.tts.speak(message)

                    return {
                        "success": True,
                        "message": message,
                        "intent": "COMPLETE_TODO",
                        "todo": todo,
                    }

                message = (
                    f"I could not find the task "
                    f"'{command.task}'."
                )

                self.tts.speak(message)

                return {
                    "success": False,
                    "message": message,
                    "intent": "COMPLETE_TODO",
                }

            # ------------------------------------------------
            # DELETE TODO
            # ------------------------------------------------

            if command.intent == Intent.DELETE_TODO:

                if not command.task:

                    message = (
                        "Please tell me which task "
                        "to delete."
                    )

                    self.tts.speak(message)

                    return {
                        "success": False,
                        "message": message,
                        "intent": "DELETE_TODO",
                    }

                todo = self.service.delete_task(
                    command.task
                )

                if todo:

                    message = (
                        f"Deleted: {todo.title}."
                    )

                    self.tts.speak(message)

                    return {
                        "success": True,
                        "message": message,
                        "intent": "DELETE_TODO",
                        "todo": todo,
                    }

                message = (
                    f"I could not find the task "
                    f"'{command.task}'."
                )

                self.tts.speak(message)

                return {
                    "success": False,
                    "message": message,
                    "intent": "DELETE_TODO",
                }

            # ------------------------------------------------
            # CLEAR TODOS
            # ------------------------------------------------

            if command.intent == Intent.CLEAR_TODOS:

                self.service.clear_tasks()

                message = (
                    "All tasks have been cleared."
                )

                self.tts.speak(message)

                return {
                    "success": True,
                    "message": message,
                    "intent": "CLEAR_TODOS",
                }

            return {
                "success": False,
                "message": "Command not handled.",
                "intent": "UNKNOWN",
            }

        except Exception as exc:

            logging.exception(
                "Command processing failed"
            )

            return {
                "success": False,
                "message": f"Processing error: {exc}",
                "intent": "ERROR",
            }

    # --------------------------------------------------------
    # VOICE INPUT
    # --------------------------------------------------------

    def listen_voice(self):

        try:

            from app.voice.speech_to_text import SpeechToText

            recognizer = SpeechToText()

            return recognizer.listen()

        except Exception as exc:

            logging.exception(
                "Voice input failed: %s",
                exc,
            )

            return None


# ============================================================
# SESSION STATE
# ============================================================

if "assistant" not in st.session_state:
    st.session_state.assistant = TodoAssistant()

if "history" not in st.session_state:
    st.session_state.history = []

if "voice_log" not in st.session_state:
    st.session_state.voice_log = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


assistant = st.session_state.assistant


# ============================================================
# HELPERS
# ============================================================

def get_tasks():

    try:

        return assistant.service.list_tasks()

    except Exception as exc:

        logging.exception(
            "Task loading failed"
        )

        st.error(
            f"Could not load tasks: {exc}"
        )

        return []


def run_command(text: str):

    return assistant.process_command(text)


def intent_icon(intent):

    icons = {
        "ADD_TODO": "➕",
        "LIST_TODOS": "📋",
        "COMPLETE_TODO": "✅",
        "DELETE_TODO": "🗑️",
        "CLEAR_TODOS": "🧹",
        "HELP": "💡",
        "EXIT": "👋",
        "UNKNOWN": "❔",
        "ERROR": "⚠️",
    }

    return icons.get(
        intent,
        "🧠",
    )


def execute_quick_command(command):

    result = run_command(command)

    st.session_state.history.append(
        {
            "role": "user",
            "content": command,
        }
    )

    st.session_state.history.append(
        {
            "role": "assistant",
            "content": result["message"],
        }
    )

    st.session_state.last_result = result

    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎙️ Sakra Todo AI")

    st.caption(
        "Intelligent Task Assistant"
    )

    st.divider()

    page = st.radio(
        "Workspace",
        [
            "⌂ Dashboard",
            "⚡ Command Center",
            "📋 My Tasks",
            "🎙️ Voice Assistant",
            "🧠 NLP Inspector",
            "ℹ️ Help",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    if st.button(
        "🔄 Refresh Data",
        use_container_width=True,
    ):
        st.rerun()

    st.divider()

    st.success(
        "System online",
        icon="✅",
    )

    st.caption(
        "NLP • Service • Repository • Voice"
    )

    st.divider()

    st.caption(
        "CURRENT ENGINE"
    )

    st.info(
        "🧠 Natural Language Processing\n\n"
        "🎙️ Voice Recognition\n\n"
        "🔊 Text-to-Speech\n\n"
        "📦 Persistent Todo Storage"
    )


# ============================================================
# APPLICATION HEADER
# ============================================================

st.title(
    "🎙️ Voice-Controlled Todo Assistant"
)

st.caption(
    "Speak naturally. Type naturally. "
    "Let NLP manage your tasks."
)

# FIX:
# st.badge() requires a valid single emoji.
# ✦ was rejected by Streamlit.
st.badge(
    "NLP LABORATORY • BATCH 6",
    icon="🧠",
    color="violet",
)

st.divider()


# ============================================================
# DASHBOARD
# ============================================================

if page == "⌂ Dashboard":

    todos = get_tasks()

    total = len(todos)

    completed = sum(
        1
        for todo in todos
        if todo.completed
    )

    pending = total - completed

    percentage = (
        round(
            (completed / total) * 100
        )
        if total
        else 0
    )

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    hero_left, hero_right = st.columns(
        [3, 1],
        vertical_alignment="center",
    )

    with hero_left:

        st.header(
            "Good to see you 👋"
        )

        st.write(
            "Your personal AI-powered "
            "task workspace."
        )

        st.caption(
            "Use natural language to create, "
            "manage, complete and remove tasks."
        )

    with hero_right:

        st.metric(
            "Productivity",
            f"{percentage}%",
            "completion",
        )

    st.divider()

    # --------------------------------------------------------
    # PRODUCTIVITY
    # --------------------------------------------------------

    st.subheader(
        "📊 Productivity Overview"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "📋 Total Tasks",
            total,
        )

    with c2:

        st.metric(
            "⏳ Pending",
            pending,
        )

    with c3:

        st.metric(
            "✅ Completed",
            completed,
        )

    with c4:

        st.metric(
            "🚀 Completion",
            f"{percentage}%",
        )

    st.progress(
        percentage / 100,
        text=(
            f"{percentage}% of your tasks completed"
        ),
    )

    st.divider()

    # --------------------------------------------------------
    # QUICK ACTIONS
    # --------------------------------------------------------

    st.subheader(
        "⚡ Quick Actions"
    )

    st.caption(
        "Execute common commands instantly."
    )

    quick_commands = [
        (
            "➕ Add Task",
            "add study DSA tomorrow",
        ),
        (
            "📋 Show Tasks",
            "show my tasks",
        ),
        (
            "❓ Help",
            "help",
        ),
        (
            "🧹 Clear All",
            "clear all tasks",
        ),
    ]

    cols = st.columns(4)

    for col, (label, command) in zip(
        cols,
        quick_commands,
    ):

        with col:

            if st.button(
                label,
                use_container_width=True,
                key=f"quick_{label}",
            ):

                execute_quick_command(
                    command
                )

    st.divider()

    # --------------------------------------------------------
    # RECENT TASKS
    # --------------------------------------------------------

    st.subheader(
        "📋 Recent Tasks"
    )

    if not todos:

        st.info(
            "Your workspace is empty. "
            "Create your first task from "
            "Command Center."
        )

    else:

        recent_tasks = (
            todos[-5:][::-1]
        )

        for todo in recent_tasks:

            with st.container(
                border=True,
            ):

                left, right = st.columns(
                    [5, 1],
                    vertical_alignment="center",
                )

                with left:

                    if todo.completed:

                        st.markdown(
                            f"### ✅ ~~{todo.title}~~"
                        )

                    else:

                        st.markdown(
                            f"### ⏳ {todo.title}"
                        )

                    st.caption(
                        f"Task #{todo.id} • "
                        f"{todo.due_date or 'No due date'}"
                    )

                with right:

                    if todo.completed:

                        st.success(
                            "Completed"
                        )

                    else:

                        st.warning(
                            "Pending"
                        )


# ============================================================
# COMMAND CENTER
# ============================================================

elif page == "⚡ Command Center":

    st.header(
        "⚡ Command Center"
    )

    st.caption(
        "Control your Todo list using "
        "natural language."
    )

    status_left, status_right = st.columns(
        [3, 1],
        vertical_alignment="center",
    )

    with status_left:

        st.info(
            "💬 Type a natural-language instruction "
            "below. The NLP engine will identify "
            "your intent."
        )

    with status_right:

        st.metric(
            "Commands",
            len(
                st.session_state.history
            ) // 2,
        )

    st.divider()

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    if not st.session_state.history:

        st.subheader(
            "👋 Start a conversation"
        )

        st.caption(
            "Try one of the commands below "
            "or type your own."
        )

    else:

        for turn in (
            st.session_state.history[-20:]
        ):

            with st.chat_message(
                turn["role"]
            ):

                st.write(
                    turn["content"]
                )

    # --------------------------------------------------------
    # SUGGESTIONS
    # --------------------------------------------------------

    st.subheader(
        "💡 Suggested Commands"
    )

    examples = [
        "add study DSA tomorrow",
        "show my tasks",
        "complete study DSA",
        "delete study DSA",
        "clear all tasks",
        "help",
    ]

    example_cols = st.columns(3)

    for index, example in enumerate(
        examples
    ):

        with example_cols[
            index % 3
        ]:

            if st.button(
                f"▶ {example}",
                key=f"example_{index}",
                use_container_width=True,
            ):

                execute_quick_command(
                    example
                )

    st.divider()

    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    command = st.chat_input(
        "Type a command, e.g. add study DSA tomorrow"
    )

    if command:

        st.session_state.history.append(
            {
                "role": "user",
                "content": command,
            }
        )

        result = run_command(
            command
        )

        st.session_state.history.append(
            {
                "role": "assistant",
                "content": result["message"],
            }
        )

        st.session_state.last_result = result

        st.rerun()

    # --------------------------------------------------------
    # LAST NLP ACTION
    # --------------------------------------------------------

    if st.session_state.last_result:

        result = (
            st.session_state.last_result
        )

        st.divider()

        st.subheader(
            "🧠 Last NLP Action"
        )

        a, b, c = st.columns(3)

        with a:

            st.metric(
                "Result",
                (
                    "Success"
                    if result["success"]
                    else "Needs Attention"
                ),
            )

        with b:

            st.metric(
                "Intent",
                result.get(
                    "intent",
                    "UNKNOWN",
                ),
            )

        with c:

            st.metric(
                "Engine",
                "NLP",
            )

        st.info(
            result["message"]
        )


# ============================================================
# MY TASKS
# ============================================================

elif page == "📋 My Tasks":

    todos = get_tasks()

    st.header(
        "📋 My Tasks"
    )

    st.caption(
        "Manage your complete task collection."
    )

    total = len(todos)

    completed = sum(
        1
        for todo in todos
        if todo.completed
    )

    pending = total - completed

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "All Tasks",
            total,
        )

    with c2:

        st.metric(
            "Pending",
            pending,
        )

    with c3:

        st.metric(
            "Completed",
            completed,
        )

    st.divider()

    # --------------------------------------------------------
    # TASK LIST
    # --------------------------------------------------------

    if not todos:

        st.info(
            "🎉 No tasks yet. "
            "Use Command Center to create "
            "your first task."
        )

    else:

        for todo in todos:

            with st.container(
                border=True,
            ):

                left, mid, right = st.columns(
                    [6, 1.4, 1.4],
                    vertical_alignment="center",
                )

                with left:

                    if todo.completed:

                        st.markdown(
                            f"### ✅ ~~{todo.title}~~"
                        )

                        st.caption(
                            f"Task #{todo.id} • Completed"
                        )

                    else:

                        st.markdown(
                            f"### ⏳ {todo.title}"
                        )

                        st.caption(
                            f"Task #{todo.id} • "
                            f"{todo.due_date or 'No due date'}"
                        )

                with mid:

                    if not todo.completed:

                        if st.button(
                            "✓ Complete",
                            key=f"complete_{todo.id}",
                            use_container_width=True,
                        ):

                            result = run_command(
                                f"complete {todo.title}"
                            )

                            if result["success"]:

                                st.toast(
                                    result["message"],
                                    icon="✅",
                                )

                            else:

                                st.error(
                                    result["message"]
                                )

                            st.rerun()

                    else:

                        st.success(
                            "Done"
                        )

                with right:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{todo.id}",
                        use_container_width=True,
                    ):

                        result = run_command(
                            f"delete {todo.title}"
                        )

                        if result["success"]:

                            st.toast(
                                result["message"],
                                icon="🗑️",
                            )

                        else:

                            st.error(
                                result["message"]
                            )

                        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # CLEAR ALL
    # --------------------------------------------------------

    if todos:

        if st.button(
            "🧹 Clear All Tasks",
            use_container_width=True,
        ):

            result = run_command(
                "clear all tasks"
            )

            if result["success"]:

                st.toast(
                    result["message"],
                    icon="🧹",
                )

            else:

                st.error(
                    result["message"]
                )

            st.rerun()


# ============================================================
# VOICE ASSISTANT
# ============================================================

elif page == "🎙️ Voice Assistant":

    st.header(
        "🎙️ Voice Assistant"
    )

    st.caption(
        "Speak naturally and let the NLP "
        "engine understand you."
    )

    st.info(
        "🎧 Press the button below and speak "
        "your task naturally. Your existing "
        "Speech-to-Text component will process "
        "the microphone input."
    )

    st.divider()

    voice_left, voice_right = st.columns(
        [2, 1],
        vertical_alignment="center",
    )

    with voice_left:

        if st.button(
            "🎙️ Start Listening",
            type="primary",
            use_container_width=True,
        ):

            with st.status(
                "🎧 Listening...",
                expanded=False,
            ) as status:

                spoken_text = (
                    assistant.listen_voice()
                )

                status.update(
                    label="Listening complete",
                    state="complete",
                )

            if spoken_text:

                st.session_state.voice_log.append(
                    {
                        "role": "user",
                        "content": (
                            f"🗣️ {spoken_text}"
                        ),
                    }
                )

                result = run_command(
                    spoken_text
                )

                st.session_state.voice_log.append(
                    {
                        "role": "assistant",
                        "content": (
                            result["message"]
                        ),
                    }
                )

                st.session_state.last_result = (
                    result
                )

            else:

                st.session_state.voice_log.append(
                    {
                        "role": "assistant",
                        "content": (
                            "I couldn't understand "
                            "the voice input. "
                            "Please try again."
                        ),
                    }
                )

            st.rerun()

    with voice_right:

        st.metric(
            "Voice Sessions",
            len(
                st.session_state.voice_log
            ) // 2,
        )

    st.divider()

    # --------------------------------------------------------
    # VOICE CONVERSATION
    # --------------------------------------------------------

    st.subheader(
        "💬 Voice Conversation"
    )

    if not st.session_state.voice_log:

        st.info(
            "Your voice conversation "
            "will appear here."
        )

    else:

        for turn in (
            st.session_state.voice_log[-20:]
        ):

            with st.chat_message(
                turn["role"]
            ):

                st.write(
                    turn["content"]
                )

    st.divider()

    # --------------------------------------------------------
    # EXAMPLES
    # --------------------------------------------------------

    st.subheader(
        "🗣️ Try Saying"
    )

    voice_examples = [
        "Add study DSA tomorrow",
        "Show my tasks",
        "Complete study DSA",
        "Delete study DSA",
        "Clear all tasks",
        "Help",
    ]

    cols = st.columns(3)

    for index, example in enumerate(
        voice_examples
    ):

        with cols[index % 3]:

            st.info(
                f"🎙️ {example}"
            )


# ============================================================
# NLP INSPECTOR
# ============================================================

elif page == "🧠 NLP Inspector":

    st.header(
        "🧠 NLP Inspector"
    )

    st.caption(
        "Inspect how the natural-language "
        "command is interpreted."
    )

    st.divider()

    inspect_text = st.text_input(
        "Enter a command",
        placeholder=(
            "Example: add study DSA tomorrow"
        ),
    )

    if st.button(
        "🔍 Analyze Command",
        type="primary",
        use_container_width=True,
    ):

        if not inspect_text.strip():

            st.warning(
                "Enter a command first."
            )

        else:

            try:

                parsed = assistant.parser.parse(
                    inspect_text
                )

                st.success(
                    "Command successfully parsed."
                )

                st.divider()

                # ------------------------------------------------
                # INTERPRETATION
                # ------------------------------------------------

                st.subheader(
                    "🔬 Interpretation"
                )

                a, b, c = st.columns(3)

                with a:

                    st.metric(
                        "Intent",
                        parsed.intent.value,
                    )

                with b:

                    st.metric(
                        "Task",
                        parsed.task or "None",
                    )

                with c:

                    st.metric(
                        "Due Date",
                        parsed.due_date or "None",
                    )

                st.divider()

                # ------------------------------------------------
                # PIPELINE
                # ------------------------------------------------

                st.subheader(
                    "🧠 Processing Pipeline"
                )

                p1, p2, p3, p4 = st.columns(4)

                with p1:

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            "💬 Input"
                        )

                        st.write(
                            inspect_text
                        )

                with p2:

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            "🧠 Parser"
                        )

                        st.write(
                            "Command analysis"
                        )

                with p3:

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            f"{intent_icon(parsed.intent.value)} Intent"
                        )

                        st.write(
                            parsed.intent.value
                        )

                with p4:

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            "📦 Entity"
                        )

                        st.write(
                            parsed.task or "None"
                        )

                st.divider()

                # ------------------------------------------------
                # EXTRACTED INFORMATION
                # ------------------------------------------------

                st.subheader(
                    "📌 Extracted Information"
                )

                e1, e2 = st.columns(2)

                with e1:

                    with st.container(
                        border=True
                    ):

                        st.caption(
                            "TASK"
                        )

                        st.markdown(
                            f"### {parsed.task or 'No task detected'}"
                        )

                with e2:

                    with st.container(
                        border=True
                    ):

                        st.caption(
                            "DUE DATE"
                        )

                        st.markdown(
                            f"### {parsed.due_date or 'No due date'}"
                        )

            except Exception as exc:

                logging.exception(
                    "NLP inspection failed"
                )

                st.error(
                    f"Parsing error: {exc}"
                )


# ============================================================
# HELP
# ============================================================

elif page == "ℹ️ Help":

    st.header(
        "ℹ️ How Sakra Todo AI Works"
    )

    st.caption(
        "A natural-language interface "
        "for intelligent task management."
    )

    st.divider()

    # --------------------------------------------------------
    # INTRODUCTION
    # --------------------------------------------------------

    st.subheader(
        "🧠 Natural Language Control"
    )

    st.write(
        "You don't need to remember complicated "
        "commands. Simply tell the assistant "
        "what you want to do."
    )

    example_left, example_right = st.columns(
        [1, 2],
        vertical_alignment="center",
    )

    with example_left:

        st.success(
            "💬 Example"
        )

    with example_right:

        st.info(
            "Add study DSA tomorrow"
        )

    st.divider()

    # --------------------------------------------------------
    # APPLICATION FLOW
    # --------------------------------------------------------

    st.subheader(
        "🏗️ Application Flow"
    )

    st.caption(
        "Your command moves through the "
        "following processing pipeline."
    )

    flow_items = [
        (
            "01",
            "🎙️ Voice Input",
            "Speak naturally using "
            "the voice assistant.",
        ),
        (
            "02",
            "⌨️ Text Input",
            "Type a natural-language "
            "command.",
        ),
        (
            "03",
            "🧠 NLP Parser",
            "CommandParser identifies "
            "intent and task information.",
        ),
        (
            "04",
            "⚙️ Todo Service",
            "Business logic performs "
            "the requested operation.",
        ),
        (
            "05",
            "🗄️ Repository",
            "TodoRepository handles "
            "persistent storage.",
        ),
        (
            "06",
            "📄 Todo Data",
            "Configured storage keeps "
            "your tasks available.",
        ),
    ]

    for start in range(
        0,
        len(flow_items),
        2,
    ):

        cols = st.columns(2)

        for col, item in zip(
            cols,
            flow_items[start:start + 2],
        ):

            number, title, description = item

            with col:

                with st.container(
                    border=True
                ):

                    st.caption(
                        f"STEP {number}"
                    )

                    st.subheader(
                        title
                    )

                    st.write(
                        description
                    )

    st.divider()

    # --------------------------------------------------------
    # COMMAND TYPES
    # --------------------------------------------------------

    st.subheader(
        "⚡ Supported Actions"
    )

    command_cards = [
        (
            "➕",
            "Add",
            "Create a new task",
            "add study DSA tomorrow",
        ),
        (
            "📋",
            "List",
            "View your tasks",
            "show my tasks",
        ),
        (
            "✅",
            "Complete",
            "Mark a task complete",
            "complete study DSA",
        ),
        (
            "🗑️",
            "Delete",
            "Remove a task",
            "delete study DSA",
        ),
        (
            "🧹",
            "Clear",
            "Remove all tasks",
            "clear all tasks",
        ),
        (
            "❓",
            "Help",
            "Get command guidance",
            "help",
        ),
    ]

    for start in range(
        0,
        len(command_cards),
        3,
    ):

        cols = st.columns(3)

        for col, item in zip(
            cols,
            command_cards[start:start + 3],
        ):

            icon, title, description, example = item

            with col:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        f"{icon} {title}"
                    )

                    st.caption(
                        description
                    )

                    st.info(
                        example
                    )

    st.divider()

    # --------------------------------------------------------
    # COMPONENTS
    # --------------------------------------------------------

    st.subheader(
        "🧩 System Components"
    )

    components = [
        (
            "🧠",
            "NLP Engine",
            "Natural-language "
            "command interpretation",
        ),
        (
            "🎙️",
            "Speech-to-Text",
            "Voice command recognition",
        ),
        (
            "🔊",
            "Text-to-Speech",
            "Spoken assistant responses",
        ),
        (
            "⚙️",
            "Todo Service",
            "Business logic for "
            "task operations",
        ),
        (
            "🗄️",
            "Todo Repository",
            "Persistent task management",
        ),
        (
            "📦",
            "JSON Persistence",
            "Configured task "
            "data storage",
        ),
    ]

    for start in range(
        0,
        len(components),
        3,
    ):

        cols = st.columns(3)

        for col, component in zip(
            cols,
            components[start:start + 3],
        ):

            icon, name, description = component

            with col:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        f"{icon} {name}"
                    )

                    st.caption(
                        description
                    )

    st.divider()

    # --------------------------------------------------------
    # VOICE PIPELINE
    # --------------------------------------------------------

    st.subheader(
        "🔊 Voice Processing Pipeline"
    )

    st.info(
        "🎙️ Voice Input  →  "
        "📝 Speech-to-Text  →  "
        "🧠 NLP Parser  →  "
        "⚙️ Todo Service  →  "
        "🗄️ Repository  →  "
        "🔊 Text-to-Speech"
    )

    st.write(
        "The application reuses the existing "
        "Speech-to-Text component for voice input "
        "and Text-to-Speech component for spoken "
        "responses."
    )

    st.divider()

    # --------------------------------------------------------
    # STORAGE
    # --------------------------------------------------------

    st.subheader(
        "💾 Storage"
    )

    st.write(
        "Tasks are persisted through the existing "
        "repository layer and stored in the "
        "configured Todo file."
    )

    st.success(
        "Persistent storage layer connected",
        icon="💾",
    )


# ============================================================
# RECENT COMMAND HISTORY
# ============================================================

combined_history = (
    st.session_state.history
    + st.session_state.voice_log
)

if combined_history:

    st.divider()

    with st.expander(
        "🕘 Recent Command History"
    ):

        for turn in (
            combined_history[-10:]
        ):

            role_icon = (
                "👤"
                if turn["role"] == "user"
                else "🤖"
            )

            st.write(
                f"{role_icon} "
                f"**{turn['role'].title()}**"
            )

            st.caption(
                turn["content"]
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

footer_left, footer_right = st.columns(
    [3, 1],
    vertical_alignment="center",
)

with footer_left:

    st.caption(
        "🎙️ Voice-Controlled Todo Assistant"
    )

    st.caption(
        "NLP Laboratory Experiment • Batch 6"
    )

with footer_right:

    st.caption(
        "Python • Streamlit • NLP • JSON"
    )