"""Data access repositories.

TODO (round 2):
- Implement CRUD operations for each repository.
- Add pagination and search for HistoryRepo.
"""

import logging
from datetime import datetime
from typing import Optional

from src.constants import APP_NAME
from src.data.database import Database
from src.data.models import HistoryRecord, DictWord, UserStats, DictWordSource

logger = logging.getLogger(APP_NAME)


class HistoryRepo:
    """CRUD for dictation history records."""

    def __init__(self, db: Database):
        self._db = db

    def insert(self, record: HistoryRecord) -> int:
        """Insert a new history record and return its ID.

        TODO: INSERT INTO history (...) VALUES (...)
        """
        logger.info("HistoryRepo: insert (TODO)")
        return 0

    def get_all(self, limit: int = 100, offset: int = 0) -> list[HistoryRecord]:
        """Fetch recent history entries.

        TODO: SELECT ... FROM history ORDER BY created_at DESC LIMIT ? OFFSET ?
        """
        return []

    def delete(self, record_id: int) -> None:
        """Delete a history record by ID.

        TODO: DELETE FROM history WHERE id = ?
        """
        pass

    def clear_before(self, before: datetime) -> int:
        """Delete all records older than *before*. Returns count deleted.

        TODO: DELETE FROM history WHERE created_at < ?
        """
        return 0


class DictionaryRepo:
    """CRUD for custom dictionary words."""

    def __init__(self, db: Database):
        self._db = db

    def insert(self, word: DictWord) -> int:
        """Insert or replace a dictionary word. Returns ID.

        TODO: INSERT OR REPLACE INTO dictionary (...)
        """
        return 0

    def get_all(self, source: Optional[DictWordSource] = None) -> list[DictWord]:
        """Fetch all dictionary entries, optionally filtered by source.

        TODO: SELECT ... FROM dictionary [WHERE source = ?]
        """
        return []

    def delete(self, word_id: int) -> None:
        """TODO: DELETE FROM dictionary WHERE id = ?"""
        pass

    def search(self, query: str) -> list[DictWord]:
        """TODO: SELECT ... WHERE word LIKE ? OR description LIKE ?"""
        return []


class StatsRepo:
    """Aggregated statistics from history data."""

    def __init__(self, db: Database):
        self._db = db

    def get_stats(self) -> UserStats:
        """Compute aggregate stats from the history table.

        TODO:
        - SELECT COUNT(*), SUM(audio_duration_seconds), SUM(char_count) FROM history
        - Compute derived metrics
        """
        return UserStats()
