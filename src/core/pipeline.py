"""Dictation pipeline — orchestrates record → transcribe → polish → inject.

Runs heavy work (API calls) in a QThread worker. Text injection is posted
back to the main thread via signal.

TODO (round 2):
- Wire up the actual AudioRecorder, WhisperTranscriber, TextPolisher,
  TextInjector, and DictionaryEngine.
- Emit state changes for the floating status window.
- Save results to HistoryRepo.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, QThread, Signal

from src.constants import AppState, APP_NAME
from src.core.audio_recorder import AudioRecorder
from src.core.transcriber import WhisperTranscriber
from src.core.polisher import TextPolisher
from src.core.text_injector import TextInjector
from src.core.dictionary_engine import DictionaryEngine

logger = logging.getLogger(APP_NAME)


class DictationWorker(QObject):
    """Runs transcription + polishing off the main thread."""

    finished = Signal(str, str)  # (raw_text, polished_text)
    error = Signal(str)
    state_changed = Signal(AppState)

    def __init__(
        self,
        wav_bytes: bytes,
        transcriber: WhisperTranscriber,
        polisher: TextPolisher,
        dictionary_engine: DictionaryEngine,
    ):
        super().__init__()
        self._wav_bytes = wav_bytes
        self._transcriber = transcriber
        self._polisher = polisher
        self._dict_engine = dictionary_engine

    def run(self) -> None:
        """Execute the transcribe → polish pipeline.

        TODO:
        - self.state_changed.emit(AppState.TRANSCRIBING)
        - result = self._transcriber.transcribe(self._wav_bytes)
        - self.state_changed.emit(AppState.POLISHING)
        - dict_ctx = self._dict_engine.build_prompt_context()
        - polished = self._polisher.polish(result.text, dict_ctx)
        - self.finished.emit(result.text, polished)
        """
        logger.info("DictationWorker: run (TODO)")
        self.finished.emit("", "")


class DictationPipeline(QObject):
    """High-level orchestrator connecting hotkey → record → worker → inject."""

    state_changed = Signal(AppState)
    dictation_complete = Signal(str, str)  # (raw, polished)
    error_occurred = Signal(str)

    def __init__(
        self,
        recorder: AudioRecorder,
        transcriber: WhisperTranscriber,
        polisher: TextPolisher,
        injector: TextInjector,
        dictionary_engine: DictionaryEngine,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._recorder = recorder
        self._transcriber = transcriber
        self._polisher = polisher
        self._injector = injector
        self._dict_engine = dictionary_engine
        self._worker: DictationWorker | None = None
        self._thread: QThread | None = None
        self._state = AppState.IDLE

    @property
    def state(self) -> AppState:
        return self._state

    def on_recording_start(self) -> None:
        """Called when the hotkey is pressed."""
        # TODO: start recording, update state
        logger.info("DictationPipeline: on_recording_start (TODO)")
        self._state = AppState.RECORDING
        self.state_changed.emit(self._state)

    def on_recording_stop(self) -> None:
        """Called when the hotkey is released."""
        # TODO: stop recording, launch DictationWorker in QThread
        logger.info("DictationPipeline: on_recording_stop (TODO)")
        self._state = AppState.TRANSCRIBING
        self.state_changed.emit(self._state)

    def _on_worker_finished(self, raw: str, polished: str) -> None:
        """Handle worker completion — inject text, save history."""
        # TODO: self._injector.inject_text(polished)
        # TODO: save to history repository
        self._state = AppState.IDLE
        self.state_changed.emit(self._state)
        self.dictation_complete.emit(raw, polished)
        logger.info("DictationPipeline: dictation complete")

    def _on_worker_error(self, msg: str) -> None:
        self._state = AppState.ERROR
        self.state_changed.emit(self._state)
        self.error_occurred.emit(msg)
        logger.error("DictationPipeline: %s", msg)
