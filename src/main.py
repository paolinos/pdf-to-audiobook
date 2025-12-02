import sys
import asyncio
import time
from os import path
from pathlib import Path

from processor.pdf_mp3_converter import PdfMp3Converter

OUTPUT_FOLDER = "./tmp"

def parse_args() -> str:
    """
    Parse args and return the first argument
    
    :return: first argument
    :rtype: str
    """
    p = sys.argv[1:]
    if len(p) == 1:
        return p[0]

    raise ValueError("Missing argument. To run the pdf-to-audiobook you need to pass the the path of the pdf file to convert")

async def main():
    # TODO: missing to receive the input from args
    #pdf_path = "./file.pdf"

    try:
        pdf_path = parse_args()

        converter = PdfMp3Converter()
        await converter.run(pdf_path)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    asyncio.run(main())
