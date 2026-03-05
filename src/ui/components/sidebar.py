"""Left sidebar — logo, navigation items, bottom icon bar."""

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy,
)

from src.constants import NavPage, SIDEBAR_WIDTH, APP_NAME, APP_VERSION
from src.ui.components.nav_item import NavItem


class Sidebar(QWidget):
    """Sidebar matching the Typeless design: logo top, nav middle, icons bottom."""

    page_changed = Signal(NavPage)
    settings_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)

        self._nav_items: list[NavItem] = []
        self._setup_ui()
        self.set_active_page(NavPage.HOME)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 12)
        layout.setSpacing(0)

        # ── Logo row ──────────────────────────────────────────
        logo_row = QHBoxLayout()
        logo_row.setContentsMargins(8, 24, 8, 16)

        logo_icon = QLabel("\U0001F399")  # 🎙 microphone emoji as placeholder
        logo_icon.setStyleSheet("font-size: 22px;")

        logo_text = QLabel(APP_NAME)
        logo_text.setObjectName("sidebarLogo")

        logo_row.addWidget(logo_icon)
        logo_row.addWidget(logo_text)
        logo_row.addStretch()
        layout.addLayout(logo_row)

        # ── Navigation items ──────────────────────────────────
        layout.addSpacing(8)
        for page in NavPage:
            item = NavItem(page, self)
            item.page_requested.connect(self._on_page_requested)
            self._nav_items.append(item)
            layout.addWidget(item)
            layout.addSpacing(2)

        # ── Spacer ────────────────────────────────────────────
        layout.addStretch()

        # ── Version label ─────────────────────────────────────
        version_label = QLabel(f"版本 v{APP_VERSION}")
        version_label.setProperty("class", "versionLabel")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        layout.addSpacing(8)

        # ── Bottom icon bar ───────────────────────────────────
        bottom_bar = QHBoxLayout()
        bottom_bar.setSpacing(4)

        for icon, tooltip in [
            ("\u2699", "设置"),       # ⚙ gear
            ("\u2753", "帮助"),       # ❓ help
        ]:
            btn = QPushButton(icon)
            btn.setProperty("class", "bottomIcon")
            btn.setFixedSize(36, 36)
            btn.setToolTip(tooltip)
            if tooltip == "设置":
                btn.clicked.connect(self.settings_requested.emit)
            bottom_bar.addWidget(btn)

        bottom_bar.addStretch()
        layout.addLayout(bottom_bar)

    def _on_page_requested(self, page: NavPage) -> None:
        self.set_active_page(page)
        self.page_changed.emit(page)

    def set_active_page(self, page: NavPage) -> None:
        for item in self._nav_items:
            item.set_active(item.page == page)
