import argparse
from dataclasses import dataclass
from os import path


@dataclass(frozen=True)
class CliOptions:
    input_path: str
    audio_speed: float

    # def __init__(self, input_path: str, audio_speed: float):
    #     self.input_path = input_path
    #     self.audio_speed = audio_speed


CLI_HELPER = """
Pdf to Audiobook
----------------

Usage:

	python ./src/main.py [options] [pdf file path]

Options:
	-speed
"""

CLI_DEFAULT_SPEED = 1.0


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

    args = parser.parse_args()

    if path.isfile(args.filepath) is False:
        raise FileNotFoundError("filepath was not found, review the path")

    if args.speed < 0.5 or args.speed > 2.0:
        raise ValueError(
            "speed had an invalid value. should be a float number from 0.5 to 2.0"
        )

    return CliOptions(args.filepath, args.speed)
