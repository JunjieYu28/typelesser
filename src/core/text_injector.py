"""Inject text into the currently focused input via Win32 SendInput.

Must run on the main (foreground) thread so that SendInput targets the
correct window.

TODO (round 2):
- Implement inject_text using send_unicode_char from win32_helpers.
- Add configurable inter-character delay.
- Handle newlines (Enter key simulation).
"""

import logging
import time

from src.constants import APP_NAME

logger = logging.getLogger(APP_NAME)


class TextInjector:
    """Types text into the active window via simulated keyboard input."""

    def __init__(self, char_delay_ms: int = 5):
        self._char_delay = char_delay_ms / 1000.0

    def inject_text(self, text: str) -> None:
        """Inject each character of *text* into the focused input field.

        TODO:
        - Import send_unicode_char from src.utils.win32_helpers
        - Loop over characters, call send_unicode_char for each
        - Handle '\\n' → simulate Enter key
        - Small sleep between chars for reliability
        """
        logger.info("TextInjector: inject_text (TODO) — %d chars", len(text))

    def set_char_delay(self, ms: int) -> None:
        self._char_delay = ms / 1000.0
