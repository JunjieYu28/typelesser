"""SQLite database connection and schema management.

TODO (round 2):
- Implement actual table creation for history, dictionary, stats.
- Add migration support for schema upgrades.
"""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from src.constants import DB_PATH, DATA_DIR, APP_NAME

logger = logging.getLogger(APP_NAME)

SCHEMA_SQL = """\
CREATE TABLE IF NOT EXISTS history (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_text              TEXT    NOT NULL DEFAULT '',
    polished_text         TEXT    NOT NULL DEFAULT '',
    language              TEXT    NOT NULL DEFAULT '',
    audio_duration_seconds REAL   NOT NULL DEFAULT 0,
    char_count            INTEGER NOT NULL DEFAULT 0,
    created_at            TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS dictionary (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    word        TEXT    NOT NULL UNIQUE,
    description TEXT    NOT NULL DEFAULT '',
    source      TEXT    NOT NULL DEFAULT 'manual',
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS stats (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL DEFAULT ''
);
"""


class Database:
    """Thin wrapper around sqlite3 with schema init."""

    def __init__(self, db_path: Path = DB_PATH):
        self._db_path = db_path
        self._conn: sqlite3.Connection | None = None

    def connect(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._create_tables()
        logger.info("Database connected: %s", self._db_path)

    def _create_tables(self) -> None:
        self._conn.executescript(SCHEMA_SQL)
        self._conn.commit()

    @property
    def connection(self) -> sqlite3.Connection:
        if self._conn is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._conn

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
            logger.info("Database closed")
