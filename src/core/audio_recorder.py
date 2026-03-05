"""Microphone recording via sounddevice — streams audio and returns WAV bytes.

TODO (round 2):
- Implement start_recording / stop_recording using sounddevice InputStream.
- Accumulate float32 frames in a list, concatenate on stop.
- Encode to WAV via src.utils.audio_utils.encode_wav().
- Emit level_changed for VU-meter display.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
from PySide6.QtCore import QObject, Signal

from src.constants import AUDIO_SAMPLE_RATE, AUDIO_CHANNELS, APP_NAME

logger = logging.getLogger(APP_NAME)


class AudioRecorder(QObject):
    """Push-to-talk microphone recorder."""

    recording_started = Signal()
    recording_stopped = Signal(bytes)   # WAV bytes
    level_changed = Signal(float)       # RMS level 0.0–1.0
    error_occurred = Signal(str)

    def __init__(
        self,
        sample_rate: int = AUDIO_SAMPLE_RATE,
        channels: int = AUDIO_CHANNELS,
        device: Optional[int] = None,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._sample_rate = sample_rate
        self._channels = channels
        self._device = device
        self._stream = None
        self._frames: list[np.ndarray] = []
        self._is_recording = False

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    def start_recording(self) -> None:
        """Begin capturing audio from the microphone."""
        # TODO: open sounddevice.InputStream, set self._is_recording = True
        logger.info("AudioRecorder: start_recording (TODO)")
        self._is_recording = True
        self._frames.clear()
        self.recording_started.emit()

    def stop_recording(self) -> bytes:
        """Stop capture and return WAV-encoded bytes."""
        # TODO: close stream, concatenate frames, encode WAV
        logger.info("AudioRecorder: stop_recording (TODO)")
        self._is_recording = False
        wav_bytes = b""  # placeholder
        self.recording_stopped.emit(wav_bytes)
        return wav_bytes

    def set_device(self, device: Optional[int]) -> None:
        """Change the input device (takes effect on next recording)."""
        self._device = device

    def _audio_callback(self, indata: np.ndarray, frames: int, time_info, status) -> None:
        """sounddevice stream callback — accumulates frames."""
        # TODO: append indata.copy(), compute RMS, emit level_changed
        pass
