from enum import Enum
from typing import Optional

import torch
from TTS.api import TTS


class TTS_MODEL(str, Enum):
    # EN
    GLOW_TTS = "tts_models/en/ljspeech/glow-tts"
    TACOTRON2_DDC = "tts_models/en/ljspeech/tacotron2-DDC"
    VITS = "tts_models/en/vctk/vits"
    TORTOISE_V2 = "tts_models/en/multi-dataset/tortoise-v2"

    # Multilingual
    BARK = "tts_models/multilingual/multi-dataset/bark"
    YOUR_TTS = "tts_models/multilingual/multi-dataset/your_tts"


def get_speaker(model: TTS_MODEL) -> Optional[str]:
    """
    Return speaker for each models. some of the models are not a multi-models, so no speaker.

    :param model: model
    :type model: TTS_MODEL
    :return: None or speaker
    :rtype: str | None
    """
    if model is TTS_MODEL.VITS:
        # p236, p292
        return "p292"

    return None


CUDA = "cuda"


class CoquiTTS:
    def __init__(self, model: TTS_MODEL = TTS_MODEL.VITS) -> None:
        self.device = CUDA if torch.cuda.is_available() else "cpu"
        self.model: TTS_MODEL = model

        self.tts = TTS(model_name=model, progress_bar=False).to(self.device)
        print(self.tts.list_models())

    @property
    def speakers(self):
        return self.tts.speakers

    def process(
        self,
        text: str,
        output: str,
        speaker: Optional[str] = None,
        language: Optional[str] = None,
    ):
        """
        Process the text to audio

        :param text: Input text to synthesize.
        :type text: str
        :param output: Output file path.
        :type output: str
        """

        if self.device == CUDA:
            # force clean cache ever time that run.
            torch.cuda.empty_cache()

        if speaker is None:
            speaker = get_speaker(self.model)

        self.tts.tts_to_file(
            text=text,
            split_sentences=False,
            file_path=output,
            speaker=speaker,
            language=language,
        )
