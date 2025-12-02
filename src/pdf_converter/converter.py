from enum import Enum
from typing import Callable, TypeVar

from marker.config.parser import ConfigParser
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.renderers.json import JSONOutput
from marker.renderers.markdown import MarkdownOutput

DEBUG = False
"""
Enable/disable `marker` debug
"""


class MarkerOutputFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


T = TypeVar("T")


def run_converter(
    format: MarkerOutputFormat,
    filepath: str,
    transform: Callable[[MarkdownOutput | JSONOutput], T],
) -> T:
    config = {
        "output_format": format,
    }

    if DEBUG is True:
        # enable debug. and export metadata in the `./tmp` folder
        config["output_dir"] = "./tmp"
        config["debug"] = True

    config_parser = ConfigParser(config)

    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service(),
    )

    return converter(filepath)
