"""Data models — plain dataclasses for database records."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.constants import DictWordSource


@dataclass
class HistoryRecord:
    """A single dictation history entry."""
    id: int = 0
    raw_text: str = ""
    polished_text: str = ""
    language: str = ""
    audio_duration_seconds: float = 0.0
    char_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DictWord:
    """A user dictionary entry."""
    id: int = 0
    word: str = ""
    description: str = ""
    source: DictWordSource = DictWordSource.MANUAL
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class UserStats:
    """Aggregated usage statistics for the home page dashboard."""
    total_dictations: int = 0
    total_duration_minutes: float = 0.0
    total_chars: int = 0
    time_saved_minutes: float = 0.0
    avg_chars_per_minute: float = 0.0
    personalization_pct: float = 0.0
