"""Dictionary page — custom word list with tabs and search."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton,
)

from src.ui.components.tab_bar import TabBar
from src.ui.components.dictionary_entry import DictionaryEntry
from src.data.models import DictWord


class DictionaryPage(QScrollArea):
    """Dictionary management page matching the Typeless dictionary screen."""

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
        title = QLabel("词典")
        title.setProperty("class", "pageTitle")
        header.addWidget(title)
        header.addStretch()

        add_btn = QPushButton("新词")
        add_btn.setProperty("class", "primaryButton")
        add_btn.setFixedWidth(80)
        header.addWidget(add_btn)
        self._layout.addLayout(header)

        # ── Tab bar + search ──────────────────────────────────
        filter_row = QHBoxLayout()
        self._tab_bar = TabBar([
            ("all", "所有"),
            ("auto", "✦ 自动添加"),
            ("manual", "✎ 手动添加"),
        ])
        filter_row.addWidget(self._tab_bar)
        filter_row.addStretch()

        search_btn = QPushButton("🔍")
        search_btn.setProperty("class", "bottomIcon")
        search_btn.setFixedSize(36, 36)
        filter_row.addWidget(search_btn)
        self._layout.addLayout(filter_row)

        # ── Entries container ─────────────────────────────────
        self._entries_layout = QVBoxLayout()
        self._entries_layout.setSpacing(6)

        # Empty state
        empty_box = QVBoxLayout()
        empty_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        empty_title = QLabel("还没有词汇")
        empty_title.setProperty("class", "emptyTitle")
        empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_box.addWidget(empty_title)

        empty_desc = QLabel(
            "Typelesser 会记住您独特的名称和词汇，这些都是通过您的编辑自动学习或您手动添加的。"
        )
        empty_desc.setProperty("class", "emptyText")
        empty_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_desc.setWordWrap(True)
        empty_desc.setMaximumWidth(400)
        empty_box.addWidget(empty_desc)

        self._entries_layout.addLayout(empty_box)
        self._layout.addLayout(self._entries_layout)
        self._layout.addStretch()

    def load_entries(self, words: list[DictWord]) -> None:
        """Replace displayed entries with *words*.

        TODO: call DictionaryRepo and populate.
        """
        # Clear
        while self._entries_layout.count():
            item = self._entries_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Clear nested layouts
                sub = item.layout()
                while sub.count():
                    sub_item = sub.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()

        if not words:
            return  # keep showing empty state on fresh load

        for w in words:
            self._entries_layout.addWidget(DictionaryEntry(w, self))
