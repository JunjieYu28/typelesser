"""Application-wide constants, enums, and default values."""

from __future__ import annotations

import sys
from enum import Enum, auto
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
APP_NAME = "Typelesser"
APP_VERSION = "0.1.0"


def _get_bundle_dir() -> Path:
    """Return the base directory for bundled assets.

    When running from a PyInstaller onefile bundle, assets are extracted
    to a temporary ``sys._MEIPASS`` directory.  Otherwise fall back to
    the project root (parent of ``src/``).
    """
    if getattr(sys, "frozen", False):
        # Running inside a PyInstaller bundle
        return Path(sys._MEIPASS)          # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent  # typelesser/


BUNDLE_DIR = _get_bundle_dir()
ASSETS_DIR = BUNDLE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
STYLES_DIR = ASSETS_DIR / "styles"

DATA_DIR = Path.home() / ".typelesser"                    # %USERPROFILE%/.typelesser
CONFIG_PATH = DATA_DIR / "config.json"
DB_PATH = DATA_DIR / "typelesser.db"
LOG_PATH = DATA_DIR / "typelesser.log"

MUTEX_NAME = "Global\\TypelesserSingleInstance"


# ── Enums ──────────────────────────────────────────────────────────────
class AppState(Enum):
    """Top-level application state."""
    IDLE = auto()
    RECORDING = auto()
    TRANSCRIBING = auto()
    POLISHING = auto()
    INJECTING = auto()
    ERROR = auto()


class NavPage(Enum):
    """Sidebar navigation targets."""
    HOME = 0
    HISTORY = 1
    DICTIONARY = 2


class DictWordSource(Enum):
    """How a dictionary word was added."""
    AUTO = "auto"
    MANUAL = "manual"


# ── Defaults ───────────────────────────────────────────────────────────
DEFAULT_HOTKEY = "right alt"
DEFAULT_WHISPER_MODEL = "whisper-1"
DEFAULT_LLM_MODEL = "gpt-4o-mini"

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 680
SIDEBAR_WIDTH = 230

AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
