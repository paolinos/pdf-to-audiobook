import os
from pathlib import Path


def get_file_data(path: str) -> tuple[str, str, str]:
    p = Path(path)
    return (p.parent, p.stem, p.suffix)


def write_file(path: str, content: str):
    with open(path, "a") as f:
        f.write(content)


async def write_file_async(path: str, content: str):
    # TODO: improve with real async
    with open(path, "a") as f:
        f.write(content)


async def read_file_async(path: str) -> str:
    # TODO: improve with real async
    with open(path, "r") as content_file:
        content = content_file.read()
        return content
    
def delete_file(p:str):
    if os.path.exists(p):
        os.remove(p)

def is_file_exist(p:str) -> bool:
    return os.path.isfile(p)