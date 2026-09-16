from dataclasses import dataclass, asdict
from datetime import date, datetime
from enum import Enum
from typing import Optional


class Intent(str, Enum):
    ADD_TODO = "ADD_TODO"
    LIST_TODOS = "LIST_TODOS"
    COMPLETE_TODO = "COMPLETE_TODO"
    DELETE_TODO = "DELETE_TODO"
    CLEAR_TODOS = "CLEAR_TODOS"
    HELP = "HELP"
    EXIT = "EXIT"
    UNKNOWN = "UNKNOWN"


@dataclass
class Todo:
    id: int
    title: str
    due_date: Optional[str] = None
    completed: bool = False
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class ParsedCommand:
    intent: Intent
    task: Optional[str] = None
    due_date: Optional[str] = None
