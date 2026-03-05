"""Floating status overlay — small borderless window showing current state.

Appears near the cursor or screen corner during recording / processing.

TODO (round 2):
- Position near the text cursor or at a fixed screen corner.
- Animate show/hide with fade.
- Show waveform or pulsing dot during recording.
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame

from src.constants import AppState


_STATE_TEXT = {
    AppState.IDLE: "",
    AppState.RECORDING: "🎙  录音中…",
    AppState.TRANSCRIBING: "⏳  转录中…",
    AppState.POLISHING: "✨  润色中…",
    AppState.INJECTING: "⌨  输入中…",
    AppState.ERROR: "❌  出错了",
}


class FloatingStatus(QWidget):
    """Small overlay showing the current pipeline state."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(44)

        frame = QFrame(self)
        frame.setObjectName("floatingStatus")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 8, 16, 8)

        self._label = QLabel()
        self._label.setObjectName("floatingStatusText")
        layout.addWidget(self._label)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(frame)

        self._auto_hide_timer = QTimer(self)
        self._auto_hide_timer.setSingleShot(True)
        self._auto_hide_timer.timeout.connect(self.hide)

    def set_state(self, state: AppState) -> None:
        """Update displayed state. Auto-hides for IDLE after a brief delay."""
        text = _STATE_TEXT.get(state, "")
        self._label.setText(text)

        if state == AppState.IDLE:
            self._auto_hide_timer.start(1500)
        else:
            self._auto_hide_timer.stop()
            if text:
                self._position_on_screen()
                self.show()

    def _position_on_screen(self) -> None:
        """Place the widget at the bottom-right of the primary screen."""
        from PySide6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            x = geo.right() - self.width() - 20
            y = geo.bottom() - self.height() - 20
            self.move(x, y)
