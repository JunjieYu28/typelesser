"""Stat card widget for the home page dashboard."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel


class StatCard(QFrame):
    """Displays a single statistic: icon + value + unit on top, label below."""

    def __init__(
        self,
        icon: str,
        value: str,
        unit: str,
        label: str,
        parent=None,
    ):
        super().__init__(parent)
        self.setProperty("class", "statCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(4)

        # Top row: icon + value + unit
        top = QHBoxLayout()
        top.setSpacing(6)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 18px; color: #7a7a8a;")

        self._value_lbl = QLabel(value)
        self._value_lbl.setProperty("class", "statValue")

        unit_lbl = QLabel(unit)
        unit_lbl.setProperty("class", "statUnit")
        unit_lbl.setAlignment(Qt.AlignmentFlag.AlignBottom)

        top.addWidget(icon_lbl)
        top.addWidget(self._value_lbl)
        top.addWidget(unit_lbl)
        top.addStretch()
        layout.addLayout(top)

        # Label
        self._label_lbl = QLabel(label)
        self._label_lbl.setProperty("class", "statLabel")
        layout.addWidget(self._label_lbl)

    def set_value(self, value: str) -> None:
        self._value_lbl.setText(value)
