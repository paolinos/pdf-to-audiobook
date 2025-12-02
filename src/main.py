import asyncio
import time
from os import path
from pathlib import Path

from ffmpeg.join import merge_and_convert_mp3
from helpers.file import get_file_data, read_file_async, write_file_async
from pdf_converter.markdown import convert_pdf_to_txt
from tts.tts import TextToAudio

OUTPUT_FOLDER = "./tmp"

async def pdf_to_text(pdf_path: str, force: bool = False) -> str:
    """
    Read pdf file and convert to text file.
    
    :param pdf_path: path of the pdf file to convert
    :type pdf_path: str
    :param force: force to recreate. Default option False
    :type force: bool
    :return: path of the file
    :rtype: str
    """

    (folder, name, _) = get_file_data(pdf_path)
    output_file = path.join(OUTPUT_FOLDER, f"{name}.txt")
    if path.isfile(output_file) and force is False:
        return output_file

    txt = convert_pdf_to_txt(pdf_path)
    await write_file_async(output_file, txt)
    return output_file

async def text_to_audio(text_path: str, force: bool = False) -> list[str]:
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
    print(f"text_path:{text_path}, folder:{folder}, name:{name}, blocks:{len(blocks)}")


    audiogen = TextToAudio()

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


def check_tmp_folder(path:str):
    """
    Docstring for check_tmp_folder
    
    :param path: Description
    :type path: str
    """
    Path(path).mkdir(parents=True, exist_ok=True)


async def main():
    dt = time.time()
    # TODO: missing to receive the input from args
    pdf_path = "./file.pdf"


    check_tmp_folder(OUTPUT_FOLDER)
    
    text_path = await pdf_to_text(pdf_path)
    audios = await text_to_audio(text_path)
    merge_and_convert_mp3(audios, pdf_path)

    print(f"Total processing time: {time.time() - dt} seconds")


if __name__ == "__main__":
    asyncio.run(main())
