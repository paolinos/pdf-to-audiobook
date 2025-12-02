from enum import Enum

import torch
from TTS.api import TTS


class TTS_MODEL(str, Enum):
    GLOW_TTS = "tts_models/en/ljspeech/glow-tts"
    TACOTRON2_DDC = "tts_models/en/ljspeech/tacotron2-DDC"
    VITS = "tts_models/en/vctk/vits"


class TextToAudio:
    def __init__(self, model:TTS_MODEL = TTS_MODEL.VITS) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(model_name=model, progress_bar=False).to(self.device)

    @property
    def speakers(self):
        return self.tts.speakers
    

    def process(self, text:str, output:str):
        """
        Process the text to audio
        
        :param text: Input text to synthesize.
        :type text: str
        :param output: Output file path.
        :type output: str
        """
        self.tts.tts_to_file(
            text=text, split_sentences=True, file_path=output, speaker=self.tts.speakers[1]
        )