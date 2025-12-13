import time
from os import path
from pathlib import Path

from ffmpeg.join import merge_and_convert_mp3
from helpers.file import delete_file, get_file_data, read_file_async, write_file_async
from pdf_converter.markdown import convert_pdf_to_txt
from tts.coqui_tts import CoquiTTS

TEMP_FOLDER = "./tmp"


class PdfMp3Converter:
    def __init__(self):
        self._check_tmp_folder(TEMP_FOLDER)

    async def _pdf_to_text(self, pdf_path: str, force: bool = False) -> str:
        """
        Read pdf file and convert to text file.

        :param pdf_path: path of the pdf file to convert
        :type pdf_path: str
        :param force: force to recreate. Default option False
        :type force: bool
        :return: path of the file
        :rtype: str
        """

        (_, name, _) = get_file_data(pdf_path)
        output_file = path.join(TEMP_FOLDER, f"{name}.txt")
        if path.isfile(output_file) and force is False:
            return output_file

        txt = convert_pdf_to_txt(pdf_path)
        await write_file_async(output_file, txt)
        return output_file

    async def _text_to_audio(self, text_path: str, force: bool = False) -> list[str]:
        """
        Read text file and create the wav files
        We're going to open the markdown file, and generate N audio files.
        This is to make less intensive and use less VRAM & GPU.

        :param text_path: text file path
        :type text_path: str
        :param force: force to recreate. Default option False
        :type force: bool
        :return: list of the audios files
        :rtype: list[str]
        """
        text_content = await read_file_async(text_path)
        (folder, name, _) = get_file_data(text_path)
        blocks = text_content.split("\n\n")
        print(
            f"text_path:{text_path}, folder:{folder}, name:{name}, blocks:{len(blocks)}"
        )

        audiogen = CoquiTTS()

        audios: list[str] = []
        i = 0
        for block in blocks:
            if block == "":
                continue

            i += 1
            output_audio = path.join(folder, f"{name}_{i}.wav")
            if path.isfile(output_audio) and force is False:
                print(f"audio index: {i} already exist, path:{output_audio}")
                audios.append(output_audio)
                continue

            print(f"audio index: {i}")
            audiogen.process(block, output_audio)
            audios.append(output_audio)

        return audios

    def _check_tmp_folder(self, path: str):
        """
        Docstring for check_tmp_folder

        :param path: Description
        :type path: str
        """
        Path(path).mkdir(parents=True, exist_ok=True)

    def _validate(self, pdf_path: str) -> bool:
        """
        Docstring for _validate

        :param pdf_path: pdf path
        :type pdf_path: str
        :return:
        :rtype: bool
        """
        (_, _, ext) = get_file_data(pdf_path)
        return path.isfile(pdf_path) and ext.lower() == ".pdf"

    def _delete_temp_files(self, tmp_paths: list[str]):
        for fp in tmp_paths:
            delete_file(fp)

    async def run(self, pdf_path: str):
        dt = time.time()

        if self._validate(pdf_path) is False:
            raise ValueError(
                "Error: Invalid pdf file or path. Please review the path of the pdf file."
            )

        tmp_paths: list[str] = []

        text_path = await self._pdf_to_text(pdf_path)
        tmp_paths.append(text_path)

        audios = await self._text_to_audio(text_path)
        tmp_paths = tmp_paths + audios

        merge_and_convert_mp3(audios, pdf_path)

        # Delete files
        self._delete_temp_files(tmp_paths)

        print(f"Total processing time: {time.time() - dt} seconds")
