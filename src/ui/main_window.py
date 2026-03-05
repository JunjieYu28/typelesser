"""Main application window — sidebar + stacked pages."""

import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget,
)

from src.constants import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, NavPage,
)
from src.ui.components.sidebar import Sidebar
from src.ui.pages.home_page import HomePage
from src.ui.pages.history_page import HistoryPage
from src.ui.pages.dictionary_page import DictionaryPage

logger = logging.getLogger(APP_NAME)


class MainWindow(QMainWindow):
    """960×680 main window: left sidebar (230 px) + right page stack."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(APP_NAME)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(800, 500)

        # ── Central widget ────────────────────────────────────
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────
        self._sidebar = Sidebar(self)
        root_layout.addWidget(self._sidebar)

        # ── Page stack ────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.setObjectName("pageContainer")

        self._home_page = HomePage()
        self._history_page = HistoryPage()
        self._dictionary_page = DictionaryPage()

        self._stack.addWidget(self._home_page)       # index 0
        self._stack.addWidget(self._history_page)     # index 1
        self._stack.addWidget(self._dictionary_page)  # index 2

        root_layout.addWidget(self._stack, 1)

        # ── Signals ───────────────────────────────────────────
        self._sidebar.page_changed.connect(self._switch_page)

    # ── Public API ────────────────────────────────────────────
    @property
    def home_page(self) -> HomePage:
        return self._home_page

    @property
    def history_page(self) -> HistoryPage:
        return self._history_page

    @property
    def dictionary_page(self) -> DictionaryPage:
        return self._dictionary_page

    @property
    def sidebar(self) -> Sidebar:
        return self._sidebar

    # ── Slots ─────────────────────────────────────────────────
    def _switch_page(self, page: NavPage) -> None:
        self._stack.setCurrentIndex(page.value)
        logger.debug("Switched to page: %s", page.name)

    # ── Override close → minimize to tray ─────────────────────
    def closeEvent(self, event) -> None:
        """Hide to tray instead of quitting."""
        event.ignore()
        self.hide()
        logger.info("Window hidden to tray")
