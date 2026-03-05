"""Single history record row widget."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from src.data.models import HistoryRecord


class HistoryEntry(QFrame):
    """Displays time + polished text for one dictation."""

    def __init__(self, record: HistoryRecord, parent=None):
        super().__init__(parent)
        self.setProperty("class", "historyEntry")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(16)

        time_lbl = QLabel(record.created_at.strftime("%I:%M %p"))
        time_lbl.setProperty("class", "historyTime")
        time_lbl.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(time_lbl)

        text_lbl = QLabel(record.polished_text or record.raw_text)
        text_lbl.setProperty("class", "historyText")
        text_lbl.setWordWrap(True)
        layout.addWidget(text_lbl, 1)
