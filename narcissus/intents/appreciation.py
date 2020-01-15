import random


class Appreciation:
    def __init__(self, intent_mgr):
        self.app = intent_mgr.app
        intent_mgr.register_intent("appreciation", self.process)

    def process(self, data):
        phrases = [
            "No problem!",
            "Any time",
            "You are welcome",
            "You're welcome",
            "Sure, no problem",
            "Of course",
            "Don't mention it",
            "Don't worry about it",
        ]
        self.app.mm_show_text_and_play(random.choice(phrases))
        return False


def setup(intent_manager):
    Appreciation(intent_manager)
