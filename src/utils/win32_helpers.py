"""Win32 API helpers via ctypes for text injection."""

import ctypes
from ctypes import wintypes

# TODO: Implement SendInput-based unicode text injection.
# The TextInjector in src/core/text_injector.py will call these helpers.

INPUT_KEYBOARD = 1
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_KEYUP = 0x0002


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class INPUT(ctypes.Structure):
    class _INPUT_UNION(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]

    _anonymous_ = ("_union",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("_union", _INPUT_UNION),
    ]


def send_unicode_char(char: str) -> None:
    """Send a single unicode character via SendInput (key down + key up)."""
    user32 = ctypes.windll.user32

    inputs = (INPUT * 2)()

    # Key down
    inputs[0].type = INPUT_KEYBOARD
    inputs[0].ki.wVk = 0
    inputs[0].ki.wScan = ord(char)
    inputs[0].ki.dwFlags = KEYEVENTF_UNICODE
    inputs[0].ki.time = 0
    inputs[0].ki.dwExtraInfo = None

    # Key up
    inputs[1].type = INPUT_KEYBOARD
    inputs[1].ki.wVk = 0
    inputs[1].ki.wScan = ord(char)
    inputs[1].ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP
    inputs[1].ki.time = 0
    inputs[1].ki.dwExtraInfo = None

    user32.SendInput(2, ctypes.pointer(inputs[0]), ctypes.sizeof(INPUT))
