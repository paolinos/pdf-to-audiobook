from enum import Enum
from typing import Callable, TypeVar

from marker.config.parser import ConfigParser
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.renderers.json import JSONOutput
from marker.renderers.markdown import MarkdownOutput


class MarkerOutputFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


T = TypeVar("T")


def run_converter(
    format: MarkerOutputFormat,
    filepath: str,
    transform: Callable[[MarkdownOutput | JSONOutput], T],
    debug: bool = False,
) -> T:
    """
    Run converter to generate markdown/json output

    :param format: type MARKDOWN or JSON
    :type format: MarkerOutputFormat
    :param filepath: pdf file to convert
    :type filepath: str
    :param transform: type to return
    :type transform: Callable[[MarkdownOutput | JSONOutput], T]
    :param page_range: Page range to convert, specify comma separated page numbers or ranges.  Example: 0,5-10,20
    :type page_range: Optional[str]
    :return: Description
    :rtype: T
    """

    config = {"output_format": format}

    if debug is True:
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
