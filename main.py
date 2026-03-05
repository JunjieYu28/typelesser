"""Typelesser — AI voice dictation tool.

Entry point: single-instance guard, config load, logging, app launch.
"""

from __future__ import annotations

import sys
import os
import traceback

# Ensure the project root is on sys.path so `src.*` imports work both when
# running as `python main.py` and from a PyInstaller bundle.
if getattr(sys, "frozen", False):
    # Inside PyInstaller bundle: _MEIPASS is the temp extraction folder.
    sys.path.insert(0, sys._MEIPASS)  # type: ignore[attr-defined]
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    from src.utils.logger import setup_logging
    from src.config import ConfigManager

    logger = setup_logging(debug="--debug" in sys.argv)

    # Single-instance lock (Windows only)
    _guard = None
    if sys.platform == "win32":
        from src.utils.single_instance import SingleInstance
        _guard = SingleInstance()

    config_manager = ConfigManager()
    config_manager.load()

    from src.app import TypelesserApp
    app = TypelesserApp(config_manager)
    sys.exit(app.run())


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # When running as a windowed exe (console=False) uncaught exceptions
        # would silently vanish. Write them to a crash log next to the exe
        # so the user can report bugs.
        crash_path = os.path.join(
            os.path.expanduser("~"), ".typelesser", "crash.log"
        )
        os.makedirs(os.path.dirname(crash_path), exist_ok=True)
        with open(crash_path, "a", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        raise
