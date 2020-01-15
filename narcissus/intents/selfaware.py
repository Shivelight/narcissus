import random


class SelfAware:
    def __init__(self, intent_mgr):
        self.app = intent_mgr.app
        intent_mgr.register_intent("personal status", self.process)

    def process(self, data):
        positive_status = [
            "I'm doing well",
            "Great, thanks for asking",
            "I'm doing great",
        ]

        self.app.mm_show_text_and_play(random.choice(positive_status))


def setup(intent_manager):
    SelfAware(intent_manager)
