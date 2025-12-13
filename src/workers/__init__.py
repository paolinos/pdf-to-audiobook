from .base import WorkerTopic
from .markdown_to_audio_coquitts_worker import MarkdownAudioCoquiTTSWorker
from .mp3_converter_worker import Mp3ConverterWorker
from .pdf_text_worker import PdfMarkdownWorker

__all__ = [
    WorkerTopic,
    # Workers
    PdfMarkdownWorker,
    # TTS workers
    MarkdownAudioCoquiTTSWorker,
    # Output workers
    Mp3ConverterWorker,
]
