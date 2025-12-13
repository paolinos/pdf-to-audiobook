import gc
from os import path

import markdown
import torch
from bs4 import BeautifulSoup

from helpers.file import get_file_data
from models import Mp3ConverterPayload, TextAudioPayload
from tts.coqui_tts import TTS_MODEL, CoquiTTS, get_speaker
from utils.logging import Logger
from workers.base import BaseWorker, WorkerTopic


class MarkdownAudioCoquiTTSWorker(BaseWorker):
    """
    Markdown to Audio, using Coqui TTS

    """

    __tts: CoquiTTS

    def __init__(self, logger: Logger):
        super().__init__(logger)
        self.__tts = CoquiTTS(TTS_MODEL.VITS)

    async def __pre_process(self, md_content: str) -> list[str]:
        """
        pre process markdown file, clean and convert to text, to not generate unnecessary audios.

        :param md_content: markdown content
        :type md_content: str
        :return: paragraphs/blocks of text
        :rtype: list[str]
        """

        html = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])
        soup = BeautifulSoup(html, features="html.parser")

        # Convert to text all tags, leaving only the `<code>....</code>`
        for tag in soup.find_all(True):  # True = all tags
            if tag.name != "code":
                tag.unwrap()

        #  Change code block from <code>....</code> to ```....```
        for tag in soup.find_all("code"):
            code_text = tag.get_text()
            tag.string = f"\n(code)```\n{code_text}```\n"

        content = soup.get_text()
        return content.split(". ")

    async def __generate_audios(
        self, input_path: str, tmp: str, paragraphs: list[str]
    ) -> list[str]:
        """
        Docstring for __generate_audios

        :param input_path: file path
        :type input_path: str
        :param tmp: temporary folder to work
        :type tmp: str
        :param paragraphs: paragraphs/blocks of text to convert
        :type paragraphs: list[str]
        :return: list of audio path, relative to the 'tmp' path
        :rtype: list[str]
        """
        audios: list[str] = []
        i = 0
        (_, name, _) = get_file_data(input_path)

        for paragraph in paragraphs:
            if paragraph == "":
                continue

            i += 1
            output_audio = path.join(tmp, f"{name}_{i}.wav")
            if path.isfile(output_audio):
                self._logger.debug(
                    f"audio index: {i} already exist, path:{output_audio}"
                )
                audios.append(output_audio)
                continue

            self._logger.debug(f"audio index: {i}")
            self.__tts.process(paragraph, output_audio, get_speaker(TTS_MODEL.VITS))
            audios.append(output_audio)

        return audios

    async def run(self):
        self._logger.debug("worker listening for WorkerTopic.PROCESS_MARKDOWN_AUDIO")
        payload = await self._sub.listening_once(
            WorkerTopic.PROCESS_MARKDOWN_AUDIO, TextAudioPayload
        )

        self._logger.info("TextAudioWorker listen:", payload.input_path)
        paragraphs = await self.__pre_process(payload.content)
        audio_files = await self.__generate_audios(
            payload.input_path, payload.tmp_folder, paragraphs
        )

        self.stop()

        self._pub.publish(
            WorkerTopic.PROCESS_MP3_CONVERTER,
            Mp3ConverterPayload(
                input_path=payload.input_path,
                audio_speed=payload.audio_speed,
                tmp_folder=payload.tmp_folder,
                audio_files=audio_files,
            ),
        )

    def stop(self):
        gc.collect()
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        # NOTE: uncomment if you need to check CUDA memory
        # self._logger.debug(torch.cuda.memory_summary())
