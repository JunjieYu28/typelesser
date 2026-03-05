"""Custom dictionary management and prompt-context generation.

The dictionary helps the LLM correctly handle domain-specific terms,
names, and jargon that Whisper might mis-transcribe.

TODO (round 2):
- Load words from DictionaryRepo on init.
- Build a context string appended to the LLM system prompt.
- Support add/remove/search operations.
- Auto-learn words from user edits (round 3+).
"""

import logging
from typing import Optional

from src.constants import APP_NAME

logger = logging.getLogger(APP_NAME)


class DictionaryEngine:
    """Manages the user's custom dictionary and generates LLM context."""

    def __init__(self):
        self._words: dict[str, str] = {}  # word → description/context

    def load(self) -> None:
        """Load dictionary entries from the database.

        TODO: query DictionaryRepo, populate self._words
        """
        logger.info("DictionaryEngine: load (TODO)")

    def add_word(self, word: str, description: str = "") -> None:
        """Add or update a word in the dictionary."""
        self._words[word] = description

    def remove_word(self, word: str) -> None:
        """Remove a word from the dictionary."""
        self._words.pop(word, None)

    def search(self, query: str) -> list[tuple[str, str]]:
        """Search dictionary entries matching *query*."""
        q = query.lower()
        return [
            (w, d) for w, d in self._words.items()
            if q in w.lower() or q in d.lower()
        ]

    def build_prompt_context(self) -> str:
        """Generate a context string for the LLM system prompt.

        Returns
        -------
        str
            A formatted list of dictionary words and descriptions
            to be appended to the polishing system prompt.

        TODO: format as a natural-language instruction block
        """
        if not self._words:
            return ""
        lines = [f"- {word}: {desc}" if desc else f"- {word}" for word, desc in self._words.items()]
        return "以下是用户的自定义词典，请在润色时优先使用这些词汇：\n" + "\n".join(lines)

    @property
    def word_count(self) -> int:
        return len(self._words)
