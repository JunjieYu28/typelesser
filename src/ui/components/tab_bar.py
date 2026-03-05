"""Pill-style filter tab bar (e.g. 所有 / 自动添加 / 手动添加)."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton


class TabBar(QWidget):
    """Horizontal row of toggle-able pill tabs."""

    tab_changed = Signal(str)  # emits the tab key

    def __init__(self, tabs: list[tuple[str, str]], parent=None):
        """
        Parameters
        ----------
        tabs : list of (key, label)
            e.g. [("all", "所有"), ("auto", "✦ 自动添加"), ("manual", "✎ 手动添加")]
        """
        super().__init__(parent)
        self._buttons: dict[str, QPushButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        for key, label in tabs:
            btn = QPushButton(label)
            btn.setProperty("class", "tabItem")
            btn.clicked.connect(lambda checked=False, k=key: self._on_click(k))
            self._buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()

        # Activate first tab
        if tabs:
            self._set_active(tabs[0][0])

    def _on_click(self, key: str) -> None:
        self._set_active(key)
        self.tab_changed.emit(key)

    def _set_active(self, active_key: str) -> None:
        for key, btn in self._buttons.items():
            btn.setProperty("active", key == active_key)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
