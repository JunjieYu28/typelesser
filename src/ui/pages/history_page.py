"""History page — scrollable list of past dictation entries."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QComboBox,
    QPushButton,
)

from src.ui.components.history_entry import HistoryEntry
from src.data.models import HistoryRecord


class HistoryPage(QScrollArea):
    """Displays dictation history, matching the Typeless history screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("pageContainer")
        self.setWidget(content)

        self._layout = QVBoxLayout(content)
        self._layout.setContentsMargins(40, 32, 40, 32)
        self._layout.setSpacing(16)

        # ── Header row ────────────────────────────────────────
        header = QHBoxLayout()
        title = QLabel("历史记录")
        title.setProperty("class", "pageTitle")
        header.addWidget(title)
        header.addStretch()

        menu_btn = QPushButton("···")
        menu_btn.setProperty("class", "bottomIcon")
        menu_btn.setFixedSize(36, 36)
        header.addWidget(menu_btn)
        self._layout.addLayout(header)

        # ── Retention info card ───────────────────────────────
        retention_card = QWidget()
        retention_layout = QHBoxLayout(retention_card)
        retention_layout.setContentsMargins(0, 0, 0, 0)

        info_col = QVBoxLayout()
        info_col.addWidget(self._make_label("💾 保存历史", bold=True))
        info_col.addWidget(self._make_label("您希望在设备上保存口述历史多久？"))
        retention_layout.addLayout(info_col)
        retention_layout.addStretch()

        combo = QComboBox()
        combo.addItems(["永远", "30 天", "7 天", "1 天"])
        combo.setFixedWidth(100)
        retention_layout.addWidget(combo)
        self._layout.addWidget(retention_card)

        # ── Privacy notice ────────────────────────────────────
        privacy_col = QVBoxLayout()
        privacy_col.addWidget(self._make_label("🔒 您的数据保持私密", bold=True))
        privacy_col.addWidget(self._make_label(
            "您的语音口述是私密的，零数据保留。它们仅存储在您的设备上，无法从其他地方访问。"
        ))
        self._layout.addLayout(privacy_col)
        self._layout.addSpacing(8)

        # ── Entries container ─────────────────────────────────
        self._entries_layout = QVBoxLayout()
        self._entries_layout.setSpacing(6)

        # Placeholder empty state
        self._empty_label = QLabel("暂无历史记录")
        self._empty_label.setProperty("class", "emptyText")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._entries_layout.addWidget(self._empty_label)

        self._layout.addLayout(self._entries_layout)
        self._layout.addStretch()

    def load_entries(self, records: list[HistoryRecord]) -> None:
        """Replace displayed entries with *records*.

        TODO: call HistoryRepo.get_all() and populate.
        """
        # Clear existing
        while self._entries_layout.count():
            item = self._entries_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not records:
            self._empty_label = QLabel("暂无历史记录")
            self._empty_label.setProperty("class", "emptyText")
            self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._entries_layout.addWidget(self._empty_label)
        else:
            for rec in records:
                self._entries_layout.addWidget(HistoryEntry(rec, self))

    @staticmethod
    def _make_label(text: str, bold: bool = False) -> QLabel:
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        if bold:
            lbl.setStyleSheet("font-weight: 600; font-size: 14px;")
        else:
            lbl.setStyleSheet("font-size: 13px; color: #5a5a6a;")
        return lbl
