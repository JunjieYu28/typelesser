"""Audio encoding utilities."""

import io
import struct
import numpy as np

from src.constants import AUDIO_SAMPLE_RATE, AUDIO_CHANNELS


def encode_wav(audio_data: np.ndarray, sample_rate: int = AUDIO_SAMPLE_RATE) -> bytes:
    """Encode a float32 numpy array into WAV bytes (16-bit PCM).

    Parameters
    ----------
    audio_data : np.ndarray
        Mono float32 audio in [-1.0, 1.0].
    sample_rate : int
        Samples per second.

    Returns
    -------
    bytes
        Complete WAV file content.
    """
    # Clip and convert to 16-bit PCM
    pcm = np.clip(audio_data, -1.0, 1.0)
    pcm = (pcm * 32767).astype(np.int16)
    raw = pcm.tobytes()

    buf = io.BytesIO()
    # RIFF header
    buf.write(b"RIFF")
    buf.write(struct.pack("<I", 36 + len(raw)))
    buf.write(b"WAVE")
    # fmt chunk
    buf.write(b"fmt ")
    buf.write(struct.pack("<I", 16))            # chunk size
    buf.write(struct.pack("<H", 1))             # PCM format
    buf.write(struct.pack("<H", AUDIO_CHANNELS))
    buf.write(struct.pack("<I", sample_rate))
    buf.write(struct.pack("<I", sample_rate * AUDIO_CHANNELS * 2))  # byte rate
    buf.write(struct.pack("<H", AUDIO_CHANNELS * 2))                # block align
    buf.write(struct.pack("<H", 16))            # bits per sample
    # data chunk
    buf.write(b"data")
    buf.write(struct.pack("<I", len(raw)))
    buf.write(raw)

    return buf.getvalue()
