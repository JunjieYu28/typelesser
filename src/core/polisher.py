"""LLM-based text polishing via Chat Completions API.

TODO (round 2):
- Send raw transcription + system prompt to a Chat Completions endpoint.
- Incorporate dictionary context from DictionaryEngine.
- Support streaming for progressive display.
"""

from __future__ import annotations

import logging

from src.constants import APP_NAME

logger = logging.getLogger(APP_NAME)


class TextPolisher:
    """Polishes raw transcription text using an LLM."""

    def __init__(
        self,
        api_base: str = "https://api.openai.com/v1",
        api_key: str = "",
        model: str = "gpt-4o-mini",
        system_prompt: str = "",
    ):
        self._api_base = api_base.rstrip("/")
        self._api_key = api_key
        self._model = model
        self._system_prompt = system_prompt
        self._client = None  # TODO: httpx.Client

    def polish(self, raw_text: str, dictionary_context: str = "") -> str:
        """Send raw text to the LLM for polishing.

        Parameters
        ----------
        raw_text : str
            The raw Whisper transcription.
        dictionary_context : str
            Extra context from the user's custom dictionary,
            injected into the system prompt.

        Returns
        -------
        str
            Polished text.

        TODO:
        - POST to {api_base}/chat/completions
        - Handle streaming / non-streaming
        - Parse response
        """
        logger.info("TextPolisher: polish (TODO) — %d chars", len(raw_text))
        return raw_text  # passthrough until implemented

    def update_config(
        self,
        api_base: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        system_prompt: str | None = None,
    ) -> None:
        if api_base is not None:
            self._api_base = api_base.rstrip("/")
        if api_key is not None:
            self._api_key = api_key
        if model is not None:
            self._model = model
        if system_prompt is not None:
            self._system_prompt = system_prompt

    def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
