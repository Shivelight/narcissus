from abc import ABCMeta, abstractmethod
from typing import Union, BinaryIO
from os import PathLike
import tempfile

from gtts import gTTS
from pydub import AudioSegment


class TextToSpeechEngine(metaclass=ABCMeta):

    @abstractmethod
    def synthesize(self, text: str) -> Union[AudioSegment, BinaryIO, PathLike]:
        ...


class GoogleTTS(TextToSpeechEngine):

    def __init__(self, language: str = "en"):
        self.language = language

    def synthesize(self, text: str) -> AudioSegment:
        tts = gTTS(text=text, lang=self.language)
        with tempfile.TemporaryFile() as fp:
            tts.write_to_fp(fp)
            fp.seek(0)
            song = AudioSegment.from_mp3(fp)
        return song
