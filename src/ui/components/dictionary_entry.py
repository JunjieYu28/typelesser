"""Dictionary entry row widget."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton

from src.data.models import DictWord


class DictionaryEntry(QFrame):
    """Displays a single dictionary word with its description and source badge."""

    delete_requested = Signal(int)  # word id

    def __init__(self, word: DictWord, parent=None):
        super().__init__(parent)
        self._word_id = word.id
        self.setProperty("class", "historyEntry")  # reuse same card style

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(16)

        # Word + description
        text_col = QVBoxLayout()
        word_lbl = QLabel(word.word)
        word_lbl.setStyleSheet("font-weight: 600; font-size: 14px;")
        text_col.addWidget(word_lbl)

        if word.description:
            desc_lbl = QLabel(word.description)
            desc_lbl.setProperty("class", "historyText")
            desc_lbl.setWordWrap(True)
            text_col.addWidget(desc_lbl)

        layout.addLayout(text_col, 1)

        # Source badge
        source_lbl = QLabel(word.source.value)
        source_lbl.setStyleSheet(
            "font-size: 11px; color: #7a7a8a; border: 1px solid #e0e0e4; "
            "border-radius: 4px; padding: 2px 6px;"
        )
        layout.addWidget(source_lbl)

        # Delete button
        del_btn = QPushButton("✕")
        del_btn.setFixedSize(28, 28)
        del_btn.setStyleSheet(
            "border: none; color: #ccc; font-size: 14px; border-radius: 4px;"
        )
        del_btn.clicked.connect(lambda: self.delete_requested.emit(self._word_id))
        layout.addWidget(del_btn)
