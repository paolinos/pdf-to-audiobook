# PDF to Audiobook

This project is going to use different libraries, to read a PDF file and generate a audiobook in mp3 format.
So normal pdf libraries like `pymupdf` or `pypdf` can read, modify and do other stuff, but they cannot understand if there's a block of code. because code could be just a string with different background and font.

- [marker-pdf](https://github.com/datalab-to/marker):  
    Marker converts documents to markdown, JSON, chunks, and HTML quickly and accurately.  
    **NOTE** marker download all models at:
    `/home/{user}/.cache/datalab`
- [TTS](https://github.com/coqui-ai/TTS):  
    TTS is a library for advanced Text-to-Speech generation. 
    Coqui-TTS is the successor to Mozilla-TTS [mozilla/TTS](https://github.com/mozilla/TTS)


- [ffmpy](https://github.com/Ch00k/ffmpy):  
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


### v0.1
```mermaid
---
title: v0.1 of the PDF to Audiobook
---
stateDiagram
    direction LR
    %% App run
    [*] --> CLI
    state CLI {
      direction LR
      ParseArgs: Parse args
      PdfMp3ConverterRun: PdfMp3Converter run()
      ParseArgs --> PdfMp3ConverterRun
        state PdfMp3ConverterRun {
            validateFilePath: Validate pdf file path 
            pdfToText: Pdf to Text
            textToAudio: Text to Audio
            generateMp3: concat audios and convert to mp3

            [*] --> validateFilePath
            validateFilePath --> [*]: Error path not valid or file extension not valid
            validateFilePath --> pdfToText: 
            pdfToText --> textToAudio: Read pdf file and return a text file
            textToAudio --> generateMp3: Read the text file and split by `\n\n` to simulate a page split, and avoid to use all the VRAM, and start to generate many `.wav` files
            generateMp3 --> [*] : merge all the `.wav` files into a one `mp3`
            
            
        }
    }
    CLI --> [*]: ouput mp3 file in the same path
```
This was a fast approach to test every component and see if the ideas was possible.
- Pro:
    - Simple and straightforward
    - not much complexity
- Const:
    - large text can produce errors, for missing RAM.
    - not async.

### v0.2 (WIP Proposal)
To make a faster and improve version, we can do "Event-Driven Architecture" like, making workers, and make communication between events like PubSub.
We try to use the less amount of RAM, reading by each page. by doing like "EVA", we can start to process each page individually (pdf to text, text to audio) asynchronously. 

```mermaid
stateDiagram
    %%direction LR
    %% App run
    [*] --> CLI
    state CLI {
      %%direction LR

        topicProcessPdf: topic "process-pdf"
        topicProcessPage: topic "process-page-audio"
        topicProcessMerge: topic "process-merge"
        topicProcessCompleted: topic "process-completed"


        [*] --> main
        main --> createWorkers
        createWorkers --> PdfTextWorker 
        createWorkers --> TextAudioWorker
        createWorkers --> MergeAudioWorker
        main --> subscribeToComplete : listen for "process-completed" with the mp3 file
      
        state PdfTextWorker {
            processFile: process each page of the file using "marker-pdf"

            topicProcessPdf : start to consume "process-pdf" topic   
            topicProcessPdf --> processFile
            processFile --> readPage: read each page and generate a text.
            readPage --> publishPageToGenerateAudio: publish "process-page-audio" to generate the audio
            readPage --> processFile: read next page
            readPage --> [*]
        }

        state TextAudioWorker {
            topicProcessPage --> convertTextToAudio: generate N audios per page
            topicProcessPage: start listening for "process-page-audio" and generate the audios
            convertTextToAudio --> generatePagesAudio
            generatePagesAudio --> publishPageCompleted
            generatePagesAudio --> [*]
        }

        state MergeAudioWorker {
            
            topicProcessMerge --> mergeAudios
            topicProcessMerge: consume topic, and generate script to merge audio
            mergeAudios --> topicProcessCompleted: as
            mergeAudios --> [*] : save mp3 file. 
        }

        PdfTextWorker --> end  
        TextAudioWorker --> end 
        MergeAudioWorker --> end
        subscribeToComplete --> end: return mp3 file path and 
        end --> [*]

    }
    CLI --> [*]: ouput mp3 file in the same path
```
