"""Whisper API client for speech-to-text.

TODO (round 2):
- Send WAV bytes to the configured Whisper-compatible endpoint.
- Support OpenAI, Groq, and local whisper.cpp servers.
- Return raw transcription text.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from src.constants import APP_NAME

logger = logging.getLogger(APP_NAME)


@dataclass
class TranscriptionResult:
    text: str
    language: str = ""
    duration_seconds: float = 0.0


class WhisperTranscriber:
    """Async Whisper API client."""

    def __init__(
        self,
        api_base: str = "https://api.openai.com/v1",
        api_key: str = "",
        model: str = "whisper-1",
        language: str = "",
        prompt: str = "",
    ):
        self._api_base = api_base.rstrip("/")
        self._api_key = api_key
        self._model = model
        self._language = language
        self._prompt = prompt
        self._client = None  # TODO: httpx.Client

    def transcribe(self, wav_bytes: bytes) -> TranscriptionResult:
        """Send audio to the Whisper API and return the transcription.

        TODO:
        - POST multipart/form-data to {api_base}/audio/transcriptions
        - Handle errors and retries
        - Parse response JSON
        """
        logger.info("WhisperTranscriber: transcribe (TODO) — %d bytes", len(wav_bytes))
        return TranscriptionResult(text="")

    def update_config(
        self,
        api_base: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        language: str | None = None,
        prompt: str | None = None,
    ) -> None:
        """Update client configuration at runtime."""
        if api_base is not None:
            self._api_base = api_base.rstrip("/")
        if api_key is not None:
            self._api_key = api_key
        if model is not None:
            self._model = model
        if language is not None:
            self._language = language
        if prompt is not None:
            self._prompt = prompt

    def close(self) -> None:
        """Release HTTP client resources."""
        if self._client:
            self._client.close()
            self._client = None
