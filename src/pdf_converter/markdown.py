from os.path import join
from typing import Optional
from bs4 import BeautifulSoup
import markdown
from marker.renderers.markdown import MarkdownOutput
from marker.renderers.json import JSONOutput

from helpers.file import get_file_data, write_file
from pdf_converter.converter import MarkerOutputFormat, run_converter


def convert_pdf_to_txt(filepath:str)->str:
    """
    Read pdf file and convert to text only having <code> block

    :param str filepath: pdf file path
    """
    format:MarkerOutputFormat = MarkerOutputFormat.MARKDOWN
    output_format = MarkdownOutput

    data = run_converter(format, filepath, output_format)

    tmp = clean_markdown(data.markdown)
    
    return tmp




def clean_markdown(md: str) -> str:
    """
    Clean markdown file only leaving the code tag and return a new string

    :param str md: markdown string to transform to text
    """
    html = markdown.markdown(md, extensions=["fenced_code", "codehilite"])
    soup = BeautifulSoup(html, features='html.parser')

    # Convert to text all tags, leaving only the `<code>....</code>`
    for tag in soup.find_all(True):  # True = all tags
        if tag.name != "code":
            tag.unwrap()

    #  Change code block from <code>....</code> to ```....```
    for tag in soup.find_all("code"):
        code_text = tag.get_text()
        tag.string = f"\n```\n{code_text}```\n"

    return soup.get_text()