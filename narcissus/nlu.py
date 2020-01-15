from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, List
import os
import sys

import wit


@dataclass
class Understanding:
    """Class for keeping engine result."""

    engine: str
    intent: str
    entities: List[Any]


class UnderstandingEngine(metaclass=ABCMeta):
    """The base class that all NLU engine must inherit from."""

    @abstractmethod
    def engine_name(self) -> str:
        """Engine name."""
        ...

    @abstractmethod
    def parse_from_text(self, text: str) -> Understanding:
        """Parse text to get `Understanding` from the engine."""
        ...

    @abstractmethod
    def parse_from_audio(self, audio: Any) -> Understanding:
        """Parse audio to get `Understanding` from the engine."""
        ...


class WitAi(UnderstandingEngine):

    def __init__(self, intent_key: str = "intent"):
        self.intent_key = intent_key
        token = os.getenv("WIT_AI_TOKEN")
        if token is None:
            print("Specify WIT_AI_TOKEN as environment variable.")
            sys.exit(1)
        self.wit = wit.Wit(token)

    def engine_name(self) -> str:
        return "Wit"

    def parse_from_text(self, text: str) -> Understanding:
        message = self.wit.message(text)["entities"]
        intents_entity = message.pop(self.intent_key, None)
        if intents_entity:
            intent = max(intents_entity, key=lambda val: val["confidence"])["value"]
        else:
            intent = "_default_"

        return Understanding(engine=self.engine_name(), intent=intent, entities=message)

    def parse_from_audio(self, audio: Any) -> Understanding:
        raise NotImplementedError
