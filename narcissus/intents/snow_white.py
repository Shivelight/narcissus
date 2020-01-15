import random


class SnowWhite:
    def __init__(self, intent_mgr):
        self.app = intent_mgr.app
        intent_mgr.register_intent("snow white", self.process)

    def process(self, data):
        phrases = ["You are", "You", "You are, of course"]
        self.app.mm_show_text_and_play(random.choice(phrases))


def setup(intent_manager):
    SnowWhite(intent_manager)
