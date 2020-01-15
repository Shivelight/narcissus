from abc import ABCMeta
from typing import Callable
import time

from snowboy import snowboydecoder


from .util import get_resource_path


class HotwordDetectionEngine(metaclass=ABCMeta):
    def detect(self, callback: Callable) -> None:
        ...


_alexa = get_resource_path(__file__, "models/snowboy/alexa.umdl")


class Snowboy(HotwordDetectionEngine):
    def __init__(
        self,
        hotword_model: str = _alexa,
        timeout: float = 10
    ):
        self.timeout = timeout
        self.decoder = snowboydecoder.HotwordDetector(
            hotword_model, sensitivity=0.5, audio_gain=1
        )

    def _interrupt_check(self, start: float) -> bool:
        if time.time() - start > self.timeout:
            self.decoder.terminate()
            return True
        return False

    def _detected_callback(self, callback):
        self.decoder.terminate()
        callback()

    def detect(self, callback: Callable) -> None:
        start = time.time()
        self.decoder.start(
            detected_callback=lambda: self._detected_callback(callback),
            interrupt_check=lambda: self._interrupt_check(start),
            sleep_time=0.05,
        )
