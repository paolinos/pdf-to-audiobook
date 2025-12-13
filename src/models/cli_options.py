from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProcessOptions:
    input_path: str
    audio_speed: float
    """
    audio speed. Tempo must be in the [0.5, 100.0] range.
    https://www.ffmpeg.org/ffmpeg-filters.html#atempo
    """
    tmp_folder: str


@dataclass(frozen=True)
class CliOptions(ProcessOptions):
    debug: Optional[str]
