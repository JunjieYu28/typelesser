"""Prevent multiple instances via a Windows named mutex."""

from __future__ import annotations

import sys
import ctypes

from src.constants import MUTEX_NAME

ERROR_ALREADY_EXISTS = 183


class SingleInstance:
    """Acquire a system-wide named mutex. Exits if another instance holds it."""

    def __init__(self, mutex_name: str = MUTEX_NAME):
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._kernel32 = kernel32
        self._handle = kernel32.CreateMutexW(None, False, mutex_name)
        if ctypes.get_last_error() == ERROR_ALREADY_EXISTS:
            print("Typelesser is already running.")
            sys.exit(0)

    def release(self) -> None:
        if self._handle:
            self._kernel32.CloseHandle(self._handle)
            self._handle = None
