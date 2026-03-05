"""TypelesserApp — top-level application object.

Owns the QApplication, wires up tray, window, hotkey, and pipeline.
"""

import logging
import sys

from PySide6.QtCore import QFile, QTextStream
from PySide6.QtWidgets import QApplication

from src.constants import APP_NAME, STYLES_DIR, AppState
from src.config import ConfigManager
from src.core.hotkey_manager import HotkeyManager
from src.ui.main_window import MainWindow
from src.ui.system_tray import SystemTray
from src.ui.floating_status import FloatingStatus
from src.ui.pages.settings_dialog import SettingsDialog

logger = logging.getLogger(APP_NAME)


class TypelesserApp:
    """Bootstrap and run the application."""

    def __init__(self, config_manager: ConfigManager):
        self._config_manager = config_manager
        self._config = config_manager.config

        self._qapp = QApplication.instance() or QApplication(sys.argv)
        self._qapp.setApplicationName(APP_NAME)
        self._qapp.setQuitOnLastWindowClosed(False)  # keep running in tray

        self._load_stylesheet()

        # ── UI components ─────────────────────────────────────
        self._window = MainWindow()
        self._tray = SystemTray()
        self._floating = FloatingStatus()

        # ── Core components ───────────────────────────────────
        self._hotkey = HotkeyManager(hotkey=self._config.hotkey)

        # ── Wire signals ──────────────────────────────────────
        self._tray.show_window_requested.connect(self._show_window)
        self._tray.settings_requested.connect(self._open_settings)
        self._tray.quit_requested.connect(self._quit)
        self._window.sidebar.settings_requested.connect(self._open_settings)

        self._hotkey.recording_started.connect(self._on_recording_start)
        self._hotkey.recording_stopped.connect(self._on_recording_stop)

    def run(self) -> int:
        """Show window (or tray-only), start hotkey listener, enter event loop."""
        self._tray.show()
        self._hotkey.start()

        if not self._config.start_minimized:
            self._window.show()

        logger.info("Typelesser started")
        return self._qapp.exec()

    # ── Slots ─────────────────────────────────────────────────
    def _show_window(self) -> None:
        self._window.showNormal()
        self._window.activateWindow()

    def _open_settings(self) -> None:
        dlg = SettingsDialog(self._config, self._window)
        dlg.exec()

    def _quit(self) -> None:
        logger.info("Quitting…")
        self._hotkey.stop()
        self._config_manager.save()
        self._qapp.quit()

    def _on_recording_start(self) -> None:
        logger.info("Recording started")
        self._floating.set_state(AppState.RECORDING)
        # TODO: self._pipeline.on_recording_start()

    def _on_recording_stop(self) -> None:
        logger.info("Recording stopped")
        self._floating.set_state(AppState.TRANSCRIBING)
        # TODO: self._pipeline.on_recording_stop()

    # ── Helpers ───────────────────────────────────────────────
    def _load_stylesheet(self) -> None:
        qss_path = STYLES_DIR / "theme.qss"
        if qss_path.exists():
            f = QFile(str(qss_path))
            if f.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(f)
                self._qapp.setStyleSheet(stream.readAll())
                f.close()
                logger.info("Loaded stylesheet: %s", qss_path)
