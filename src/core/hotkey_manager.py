"""Global hotkey listener using the `keyboard` library.

Listens for Right Alt press/release and emits Qt signals.
Filters out auto-repeat events so each physical press produces
exactly one `recording_started` and one `recording_stopped`.
"""

from __future__ import annotations

import logging
from typing import Optional

import keyboard
from PySide6.QtCore import QObject, Signal

from src.constants import DEFAULT_HOTKEY, APP_NAME

logger = logging.getLogger(APP_NAME)


class HotkeyManager(QObject):
    """Monitors a global hotkey (default: Right Alt) for push-to-talk recording."""

    recording_started = Signal()
    recording_stopped = Signal()

    def __init__(self, hotkey: str = DEFAULT_HOTKEY, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._hotkey = hotkey
        self._is_pressed = False
        self._hook = None

    # ── public ────────────────────────────────────────────────────────
    def start(self) -> None:
        """Install the global keyboard hook."""
        logger.info("HotkeyManager: hooking key '%s'", self._hotkey)
        self._hook = keyboard.hook(self._on_event, suppress=False)

    def stop(self) -> None:
        """Remove the global keyboard hook."""
        if self._hook is not None:
            keyboard.unhook(self._hook)
            self._hook = None
            self._is_pressed = False
            logger.info("HotkeyManager: unhooked")

    def set_hotkey(self, hotkey: str) -> None:
        """Change the monitored hotkey at runtime."""
        was_running = self._hook is not None
        if was_running:
            self.stop()
        self._hotkey = hotkey
        if was_running:
            self.start()

    # ── internal ──────────────────────────────────────────────────────
    def _on_event(self, event: keyboard.KeyboardEvent) -> None:
        if event.name != self._hotkey:
            return

        if event.event_type == keyboard.KEY_DOWN:
            if not self._is_pressed:  # filter auto-repeat
                self._is_pressed = True
                logger.debug("HotkeyManager: key down → recording_started")
                self.recording_started.emit()
        elif event.event_type == keyboard.KEY_UP:
            if self._is_pressed:
                self._is_pressed = False
                logger.debug("HotkeyManager: key up → recording_stopped")
                self.recording_stopped.emit()
