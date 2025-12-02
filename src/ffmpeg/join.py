from os import path
from ffmpy import FFmpeg

from helpers.file import get_file_data

def merge_and_convert_mp3(audio_files:list[str], source_file:str):
    """
    Merge all files and convert to mp3

    :param list[str] audio_files: list of string audios
    :param str source_file: original file path.
    """
    inputs = {f: None for f in audio_files}
    n = len(audio_files)
    filter_complex = f"concat=n={n}:v=0:a=1"

    (folder, name, _) = get_file_data(source_file)
    output_path = path.join(folder, f"{name}.mp3")

    ff = FFmpeg(
        inputs=inputs,
        outputs={output_path: f"-filter_complex {filter_complex} -c:a libmp3lame -q:a 2"}
    )
    ff.run()