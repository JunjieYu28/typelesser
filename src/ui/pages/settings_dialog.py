"""Settings dialog — configure API keys, hotkey, audio device, etc.

TODO (round 2):
- Build the full settings form with tabs/sections.
- Wire up ConfigManager save on accept.
- Add audio device enumeration.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel

from src.config import AppConfig


class SettingsDialog(QDialog):
    """Application settings dialog (placeholder)."""

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self._config = config
        self.setWindowTitle("设置")
        self.setMinimumSize(480, 400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)

        title = QLabel("设置")
        title.setProperty("class", "pageTitle")
        layout.addWidget(title)

        placeholder = QLabel("设置面板将在后续版本中实现。\n\n"
                             "可配置项：API 密钥、热键、音频设备、LLM 模型等。")
        placeholder.setWordWrap(True)
        placeholder.setStyleSheet("color: #7a7a8a; font-size: 14px; padding: 24px 0;")
        layout.addWidget(placeholder)

        layout.addStretch()
