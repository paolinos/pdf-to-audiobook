from os import path

from ffmpy import FFmpeg

from helpers.file import get_file_data, is_file_exist


def merge_and_convert_mp3(
    audio_files: list[str], source_file: str, force: bool = False
) -> str:
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

    if is_file_exist(output_path) and force is False:
        print(f"mp3 file already exist with path: {output_path}")
        return output_path

    ff = FFmpeg(
        global_options="-y",
        inputs=inputs,
        outputs={
            output_path: f"-filter_complex {filter_complex} -c:a libmp3lame  -q:a 2"
        },
    )
    ff.run()
    return output_path
