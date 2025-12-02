# PDF to Audiobook

This project is going to use different libraries, to read a PDF file and generate a audiobook in mp3 format.

- [marker-pdf](https://github.com/datalab-to/marker): 
    Marker converts documents to markdown, JSON, chunks, and HTML quickly and accurately.

    is going to download 
    `/home/{user}/.cache/datalab`
- [TTS](https://github.com/coqui-ai/TTS)
    TTS is a library for advanced Text-to-Speech generation. 
    Coqui-TTS is the successor to Mozilla-TTS [mozilla/TTS](https://github.com/mozilla/TTS)


- [ffmpy](https://github.com/Ch00k/ffmpy)
    ffmpy is a simple FFmpeg command line wrapper. 
    It implements a Pythonic interface for FFmpeg command line compilation and uses Python's subprocess to execute the compiled command line.

Details:
- [UV & python setup](#uv--python-setup)
- [Processing workflow](#processing-workflow)


## UV & python setup
We're using UV to create this project, if you don't have it, read the instructions [read more](https://docs.astral.sh/uv/getting-started/installation/)

### Create project from scratch
```sh
# Create a Virtual Env with UV 
uv venv --python 3.11

# Activate venv
source .venv/bin/activate

# Ruff linter
uv tool install ruff@latest
```
### Add dependencies
```sh
uv add marker-pdf[full]
uv add TTS
uv add ffmpy
uv add asyncio
uv add beautifulsoup4
uv add markdown
```

### create venv
After pulling the project, maybe you don't have the `.venv` folder.
you can create it and install all dependencies using UV
```sh
# to create the venv use
uv venv

# Then sync to install all dependencies
uv sync
```

## Processing workflow

To read and process the pdf, we use the `marker-pdf`, and will generate a markdown file.
if we try to read a markdown file with a model that was not trained to understand it, will try to said every tag, link and so on.... No really nice.
So I decide to convert the markdown file into a `txt` fila, that only will have a "```" for code blocks.
After having a clean text file, we start to use the `TTS`, but if we pass the entire file, some parts of audio could be large, and that is a lot of CPU/GPU process intensive.
So I decide to split a bit the text in many part of text and generate many small files, to make it lightweight.
and then using the `ffmpy` (ffmpeg) I merge all the `.wav` files (**TTS only use wav, more info in their description**) and convert to mp3.
 
