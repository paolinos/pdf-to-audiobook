import argparse
from os import path
from pathlib import Path

from models import CliOptions

TEMP_FOLDER = "./tmp"

CLI_DEFAULT_SPEED = 1.0


def _check_tmp_folder(path: str):
    """
    Docstring for check_tmp_folder

    :param path: Description
    :type path: str
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def parse_args() -> CliOptions:
    """
    parse args, and validate values and file path

    :return: Description
    :rtype: ProcessOptions
    """
    parser = argparse.ArgumentParser(
        "Pdf to Audiobook",
        usage="python ./src/main.py [options] [pdf file path]",
        description="convert pdf file to mp3 files, from pdf to text, text to audio and convert to mp3 file.",
        exit_on_error=False,
    )
    parser.add_argument("filepath", type=str, help="file path to read")
    parser.add_argument(
        "--speed",
        help="to change audio speed, from 0.5 to 2.0",
        type=float,
        default=CLI_DEFAULT_SPEED,
        required=False,
    )
    parser.add_argument(
        "--debug",
        help="all is the default, but you can debug part of the pipeline like: all,pdf,tts,ffmpeg. Uou can use multiple options using ',' without space.",
        type=str,
        default=None,
        required=False,
    )
    parser.add_argument(
        "--temp",
        help="path of the temp folder that will be used to make parser, conversions, etc",
        type=str,
        default=TEMP_FOLDER,
        required=False,
    )

    args = parser.parse_args()

    if path.isfile(args.filepath) is False:
        raise FileNotFoundError("filepath was not found, review the path")

    if args.speed < 0.5 or args.speed > 2.0:
        raise ValueError(
            "speed had an invalid value. should be a float number from 0.5 to 2.0"
        )

    _check_tmp_folder(args.temp)

    return CliOptions(
        input_path=args.filepath,
        audio_speed=args.speed,
        tmp_folder=args.temp,
        debug=args.debug,
    )
