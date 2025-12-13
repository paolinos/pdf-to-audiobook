from os import path

from marker.renderers.markdown import MarkdownOutput

from helpers.file import get_file_data, write_file_async
from models import ProcessOptions, TextAudioPayload
from pdf_converter.converter import MarkerOutputFormat, run_converter
from processor.pdf_mp3_converter import TEMP_FOLDER
from utils.logging import Logger
from workers.base import BaseWorker, WorkerTopic


class PdfMarkdownWorker(BaseWorker):
    """
    Pdf to Markdown using marker-pdf model
    """

    def __init__(self, logger: Logger):
        super().__init__(logger)

    async def run(self):
        self._logger.debug("listening for PROCESS_PDF_TO_MARKDOWN")
        payload = await self._sub.listening_once(
            WorkerTopic.PROCESS_PDF_TO_MARKDOWN, ProcessOptions
        )
        self._logger.debug(
            f"Message received group:{self.__class__.__name__} - ", payload
        )

        markdown_content = run_converter(
            MarkerOutputFormat.MARKDOWN, payload.input_path, MarkdownOutput
        )

        (_, name, _) = get_file_data(payload.input_path)
        output_file = path.join(TEMP_FOLDER, f"{name}.md")
        await write_file_async(output_file, markdown_content.markdown)

        convert_audio_payload = TextAudioPayload(
            input_path=payload.input_path,
            audio_speed=payload.audio_speed,
            tmp_folder=payload.tmp_folder,
            content=markdown_content.markdown,
        )
        self._pub.publish(WorkerTopic.PROCESS_MARKDOWN_AUDIO, convert_audio_payload)

    def stop(self):
        pass
