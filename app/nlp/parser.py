import re
from datetime import date, timedelta
from app.models import Intent, ParsedCommand
from app.nlp.preprocessing import TextPreprocessor


class IntentDetector:
    """Rule-based intent classifier: deterministic and easy to explain in a viva."""

    PATTERNS = {
        Intent.ADD_TODO: [
            r"^(add|create|make|remember|remind|new)\b",
            r"\badd\b.*\btask\b",
        ],
        Intent.LIST_TODOS: [
            r"^(show|list|display|view)\b",
            r"\bwhat\b.*\b(tasks|todos)\b",
        ],
        Intent.COMPLETE_TODO: [
            r"^(complete|finish|done|mark)\b",
            r"\bmark\b.*\bcomplete\b",
        ],
        Intent.DELETE_TODO: [
            r"^(delete|remove|erase)\b",
        ],
        Intent.CLEAR_TODOS: [
            r"\b(clear|delete|remove|erase)\b.*\b(all|everything)\b",
        ],
        Intent.HELP: [r"^(help|commands?)\b"],
        Intent.EXIT: [r"^(exit|quit|bye|stop)\b"],
    }

    def detect(self, text: str) -> Intent:
        normalized = TextPreprocessor.normalize(text)

        # Clear-all must be checked before generic delete.
        for pattern in self.PATTERNS[Intent.CLEAR_TODOS]:
            if re.search(pattern, normalized):
                return Intent.CLEAR_TODOS

        for intent, patterns in self.PATTERNS.items():
            if intent == Intent.CLEAR_TODOS:
                continue
            if any(re.search(pattern, normalized) for pattern in patterns):
                return intent

        return Intent.UNKNOWN


class EntityExtractor:
    DATE_PATTERNS = {
        "today": lambda d: d,
        "tomorrow": lambda d: d + timedelta(days=1),
        "day after tomorrow": lambda d: d + timedelta(days=2),
    }

    WEEKDAYS = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
    }

    @classmethod
    def extract_due_date(cls, text: str) -> tuple[str | None, str]:
        normalized = TextPreprocessor.normalize(text)
        base = date.today()

        for phrase, resolver in sorted(cls.DATE_PATTERNS.items(), key=lambda x: -len(x[0])):
            if phrase in normalized:
                resolved = resolver(base).isoformat()
                cleaned = re.sub(rf"\b{re.escape(phrase)}\b", "", normalized)
                return resolved, re.sub(r"\s+", " ", cleaned).strip()

        for day, target_weekday in cls.WEEKDAYS.items():
            if re.search(rf"\b{day}\b", normalized):
                delta = (target_weekday - base.weekday()) % 7
                if delta == 0:
                    delta = 7
                resolved = (base + timedelta(days=delta)).isoformat()
                cleaned = re.sub(rf"\b{day}\b", "", normalized)
                return resolved, re.sub(r"\s+", " ", cleaned).strip()

        return None, normalized

    @classmethod
    def extract_task(cls, text: str, intent: Intent) -> str | None:
        normalized = TextPreprocessor.normalize(text)
        _, normalized = cls.extract_due_date(normalized)

        prefixes = {
            Intent.ADD_TODO: [
                r"^(add|create|make|remember|remind)\s+(a\s+)?(task\s+)?",
            ],
            Intent.COMPLETE_TODO: [
                r"^(complete|finish|done)\s+(task\s+)?",
                r"^mark\s+(.*?)\s+as\s+complete\s*$",
            ],
            Intent.DELETE_TODO: [
                r"^(delete|remove|erase)\s+(task\s+)?",
            ],
        }

        for pattern in prefixes.get(intent, []):
            cleaned = re.sub(pattern, "", normalized, count=1).strip()
            if cleaned:
                return cleaned

        return None


class CommandParser:
    def __init__(self):
        self.intent_detector = IntentDetector()

    def parse(self, text: str) -> ParsedCommand:
        intent = self.intent_detector.detect(text)

        if intent in {Intent.LIST_TODOS, Intent.CLEAR_TODOS, Intent.HELP,
                      Intent.EXIT, Intent.UNKNOWN}:
            return ParsedCommand(intent=intent)

        due_date, _ = EntityExtractor.extract_due_date(text)
        task = EntityExtractor.extract_task(text, intent)
        return ParsedCommand(intent=intent, task=task, due_date=due_date)
