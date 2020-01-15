from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Optional

from speech_recognition import AudioData, WaitTimeoutError
import speech_recognition as sr


def nop_callback(*args, **kwargs):
    pass


class SpeechtoTextEngine(metaclass=ABCMeta):
    @abstractmethod
    def listen(
        self,
        start_callback: Callable = nop_callback,
        end_callback: Callable = nop_callback,
    ) -> Any:
        ...

    @abstractmethod
    def recognize(self, audio: Any) -> Optional[str]:
        ...


class GoogleRecognition(SpeechtoTextEngine):
    def __init__(self, key: str = None, debug: bool = False):
        self.key = key
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1.0
        self.debug = debug

    def listen(
        self,
        start_callback: Callable = nop_callback,
        end_callback: Callable = nop_callback,
    ) -> Optional[AudioData]:
        mic = sr.Microphone()
        with mic as source:
            # self.recognizer.adjust_for_ambient_noise(source, duration=1)
            start_callback()
            # TODO: get rid
            if self.debug:
                print("I'm listening..")
                try:
                    audio = self.recognizer.listen(
                        source, timeout=5, phrase_time_limit=10
                    )
                except WaitTimeoutError:
                    return None
            if self.debug:
                print("Found audio")
            end_callback()
        return audio

    def recognize(self, audio: AudioData) -> Optional[str]:
        try:
            text = self.recognizer.recognize_google(audio, self.key)
            print(f"Google Speech Recognition thinks you said {text}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )
        else:
            return text
        return None
