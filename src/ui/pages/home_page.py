"""Home page — dashboard with stats, hotkey hint, and info cards."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea,
)

from src.constants import DEFAULT_HOTKEY
from src.ui.components.stat_card import StatCard
from src.ui.components.info_card import InfoCard


class HomePage(QScrollArea):
    """Main dashboard page matching the Typeless home screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("pageContainer")
        self.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(16)

        # ── Title ─────────────────────────────────────────────
        title = QLabel("自然说话，完美书写 – 在任何应用中")
        title.setProperty("class", "pageTitle")
        layout.addWidget(title)

        # ── Hotkey hint ───────────────────────────────────────
        hint_row = QHBoxLayout()
        hint_row.setSpacing(6)
        hint_row.addWidget(QLabel("按住"))

        hotkey_badge = QLabel(f" {DEFAULT_HOTKEY.title()} ")
        hotkey_badge.setProperty("class", "hotkeyBadge")
        hint_row.addWidget(hotkey_badge)

        hint_row.addWidget(QLabel("键，讲话，松开以插入语音文本。"))
        hint_row.addStretch()
        layout.addLayout(hint_row)

        layout.addSpacing(16)

        # ── Stat cards grid ───────────────────────────────────
        grid = QGridLayout()
        grid.setSpacing(12)

        self._stat_personalization = StatCard("\U0001F464", "0%", "", "个性化", self)
        self._stat_duration = StatCard("\u23F0", "0", "min", "总口述时间", self)
        self._stat_chars = StatCard("\U0001F399", "0", "字", "口述字数", self)
        self._stat_saved = StatCard("\u26A1", "0", "min", "节省时间", self)
        self._stat_speed = StatCard("\u26A1", "0", "每分钟字数", "平均口述速度", self)

        grid.addWidget(self._stat_personalization, 0, 0)
        grid.addWidget(self._stat_duration, 0, 1)
        grid.addWidget(self._stat_chars, 0, 2)
        grid.addWidget(self._stat_saved, 1, 0)
        grid.addWidget(self._stat_speed, 1, 1)

        layout.addLayout(grid)

        layout.addSpacing(16)

        # ── Info cards row ────────────────────────────────────
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        cards_row.addWidget(InfoCard(
            title="推荐朋友",
            description="每邀请一位朋友即可获得代金券。",
            button_text="邀请朋友",
            variant="blue",
        ))
        cards_row.addWidget(InfoCard(
            title="联盟计划",
            description="赚取 25% 的持续佣金，分享 Typelesser。",
            button_text="立即加入",
            variant="pink",
        ))
        layout.addLayout(cards_row)

        layout.addStretch()

    def update_stats(self, personalization: str, duration: str, chars: str,
                     saved: str, speed: str) -> None:
        self._stat_personalization.set_value(personalization)
        self._stat_duration.set_value(duration)
        self._stat_chars.set_value(chars)
        self._stat_saved.set_value(saved)
        self._stat_speed.set_value(speed)
