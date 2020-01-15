import time

import requests

from .audio import play
from .hotword import HotwordDetectionEngine, Snowboy
from .intent import IntentManager
from .nlu import UnderstandingEngine
from .nlu import WitAi
from .nlg import NaturalLanguageGenerator
from .stt import SpeechtoTextEngine, GoogleRecognition
from .tts import TextToSpeechEngine, GoogleTTS
from .vision import Vision


class Narcissus:
    def __init__(
        self,
        user_name: str = "Anakin",
        magicmirror_url: str = "http://localhost:8080",
        camera: int = 0,
        vision: Vision = None,
        hotword_engine: HotwordDetectionEngine = None,
        tts_engine: TextToSpeechEngine = None,
        stt_engine: SpeechtoTextEngine = None,
        nlu_engine: UnderstandingEngine = None,
        debug: bool = False,
    ):
        self.vision = vision or Vision()
        self.intent_manager = IntentManager(self)
        self.magicmirror_url = magicmirror_url
        self.hotword = hotword_engine or Snowboy()
        self.text_ts = tts_engine or GoogleTTS()
        self.understanding = nlu_engine or WitAi()
        self.nlg = NaturalLanguageGenerator(user_name)
        self.speech_tt = stt_engine or GoogleRecognition()

    def mm_mic_indicator(self, enable):
        requests.get(f"{self.magicmirror_url}/microphone?enabled={enable}")

    def mm_clear(self) -> None:
        requests.get(f"{self.magicmirror_url}/clear")

    def mm_show_text(self, text=None):
        if text is not None:
            requests.get(f"{self.magicmirror_url}/statement?text={text}")

    def mm_show_text_and_play(self, text=None):
        if text is not None:
            self.mm_show_text(text)
            play(self.text_ts.synthesize(text))

    def mm_show_face(self):
        requests.get(f"{self.magicmirror_url}/face")

    def mm_show_image(self, data):
        requests.post(f"{self.magicmirror_url}/image", json=data)

    def listen_for_intent(self) -> None:
        self.mm_mic_indicator(False)
        self.mm_show_text_and_play(self.nlg.acknowledge())
        while True:
            speech = self.speech_tt.listen(
                start_callback=lambda: self.mm_mic_indicator(True),
                end_callback=lambda: self.mm_mic_indicator(False),
            )
            if speech is None:
                return

            text = self.speech_tt.recognize(speech)
            if text:
                data = self.understanding.parse_from_text(text)
                ret = self.intent_manager.run_intent(data)
                # If ret is false then an intent is asking to stop any activity.
                if ret is False:
                    return
                else:
                    time.sleep(0.1)
                    continue

            return

    def start(self) -> None:
        self.mm_clear()
        while True:
            self.mm_mic_indicator(False)
            self.vision.recognize()
            self.mm_mic_indicator(True)
            self.hotword.detect(callback=self.listen_for_intent)
