import shutil
from os import path

from ffmpy import FFmpeg

from helpers.file import delete_file, get_file_data


def change_speed(mp3_file: str, audio_speed: float):
    """
    Change speed of the mp3 file

    :param mp3_file: path of the mp3
    :type mp3_file: str
    :param audio_speed: Tempo must be in the [0.5, 100.0] range.
    :type audio_speed: float
    """

    print(
        f"\n change_speed:\n----------------\n mp3_file:{mp3_file}; audio_speed:{audio_speed};"
    )

    (folder, filename, ext) = get_file_data(mp3_file)
    tmp_audio = path.join(folder, f"{filename}_tmp.{ext}")
    shutil.copyfile(mp3_file, tmp_audio)

    ff = FFmpeg(
        global_options="-y",
        inputs={tmp_audio: None},
        outputs={mp3_file: f"-filter:a atempo={audio_speed}"},
    )
    ff.run()

    delete_file(tmp_audio)
