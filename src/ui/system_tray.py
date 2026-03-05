"""System tray icon with context menu."""

import logging

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication

from src.constants import APP_NAME, AppState

logger = logging.getLogger(APP_NAME)


class SystemTray(QSystemTrayIcon):
    """Tray icon with right-click menu and double-click to show window."""

    show_window_requested = Signal()
    settings_requested = Signal()
    quit_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Use a built-in Qt icon as placeholder until we have custom icons
        self.setIcon(QApplication.style().standardIcon(
            QApplication.style().StandardPixmap.SP_MediaVolume
        ))
        self.setToolTip(APP_NAME)

        self._build_menu()
        self.activated.connect(self._on_activated)

    def _build_menu(self) -> None:
        menu = QMenu()

        show_action = QAction("显示窗口", menu)
        show_action.triggered.connect(self.show_window_requested.emit)
        menu.addAction(show_action)

        settings_action = QAction("设置", menu)
        settings_action.triggered.connect(self.settings_requested.emit)
        menu.addAction(settings_action)

        menu.addSeparator()

        quit_action = QAction("退出", menu)
        quit_action.triggered.connect(self.quit_requested.emit)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window_requested.emit()

    def update_icon_for_state(self, state: AppState) -> None:
        """Swap the tray icon to reflect the current app state.

        TODO: load custom icons from assets/icons/ per state.
        """
        # For now, keep the default icon
        logger.debug("SystemTray: state → %s (icon swap TODO)", state.name)
