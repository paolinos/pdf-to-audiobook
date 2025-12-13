from dataclasses import dataclass

from models.cli_options import ProcessOptions


@dataclass(frozen=True)
class PdfMarkdownInput(ProcessOptions):
    path: str

    def __str__(self):
        return self.path


@dataclass(frozen=True)
class TextAudioPayload(ProcessOptions):
    content: str


@dataclass(frozen=True)
class Mp3ConverterPayload(ProcessOptions):
    audio_files: list[str]
