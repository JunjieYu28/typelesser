"""Coloured info card (referral / affiliate style)."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton


class InfoCard(QFrame):
    """A rounded gradient card with title, description, and action button."""

    def __init__(
        self,
        title: str,
        description: str,
        button_text: str,
        variant: str = "blue",   # "blue" | "pink"
        parent=None,
    ):
        super().__init__(parent)
        cls = "infoCard infoCardBlue" if variant == "blue" else "infoCard infoCardPink"
        self.setProperty("class", cls)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)

        title_lbl = QLabel(title)
        title_lbl.setProperty("class", "infoCardTitle")
        layout.addWidget(title_lbl)

        desc_lbl = QLabel(description)
        desc_lbl.setProperty("class", "infoCardText")
        desc_lbl.setWordWrap(True)
        layout.addWidget(desc_lbl)

        btn = QPushButton(button_text)
        btn.setProperty("class", "outlineButton")
        btn.setFixedWidth(100)
        layout.addWidget(btn)
