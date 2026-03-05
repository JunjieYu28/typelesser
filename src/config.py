"""Configuration management — JSON-backed settings with dataclass defaults."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from src.constants import (
    CONFIG_PATH, DATA_DIR,
    DEFAULT_HOTKEY, DEFAULT_WHISPER_MODEL, DEFAULT_LLM_MODEL,
)


@dataclass
class AppConfig:
    """All user-configurable settings."""

    # Hotkey
    hotkey: str = DEFAULT_HOTKEY

    # Whisper / STT
    whisper_api_base: str = "https://api.openai.com/v1"
    whisper_api_key: str = ""
    whisper_model: str = DEFAULT_WHISPER_MODEL
    whisper_language: str = ""           # empty = auto-detect
    whisper_prompt: str = ""

    # LLM / polish
    llm_api_base: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = DEFAULT_LLM_MODEL
    llm_system_prompt: str = (
        "你是一个语音转文字的润色助手。请将用户口述的原始文本润色为通顺自然的书面语，"
        "保持原意不变，不要添加额外内容。只输出润色后的文本，不要有其他说明。"
    )

    # Audio
    audio_device: Optional[int] = None   # None = system default

    # UI
    start_minimized: bool = False
    show_floating_status: bool = True

    # History
    history_retention_days: int = 0      # 0 = forever

    # Dictionary
    use_dictionary: bool = True


class ConfigManager:
    """Read / write AppConfig as JSON."""

    def __init__(self, path: Path = CONFIG_PATH):
        self._path = path
        self.config = AppConfig()

    def load(self) -> AppConfig:
        if self._path.exists():
            try:
                data = json.loads(self._path.read_text(encoding="utf-8"))
                for key, value in data.items():
                    if hasattr(self.config, key):
                        setattr(self.config, key, value)
            except (json.JSONDecodeError, OSError):
                pass  # use defaults on corrupt file
        return self.config

    def save(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(asdict(self.config), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
