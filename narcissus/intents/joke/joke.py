import random
import json

from narcissus.util import get_resource_path

with open(get_resource_path(__file__, "joke.json")) as fp:
    JOKES = json.load(fp)


class Joke:
    def __init__(self, intent_mgr):
        self.app = intent_mgr.app
        intent_mgr.register_intent("joke", self.process)

    def process(self, data):
        self.app.mm_show_text_and_play(random.choice(JOKES))


def setup(intent_manager):
    Joke(intent_manager)
