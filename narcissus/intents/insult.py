class Insult:
    def __init__(self, intent_mgr):
        self.app = intent_mgr.app
        intent_mgr.register_intent("insult", self.process)

    def process(self, data):
        self.app.mm_show_text_and_play(
            "That's not very nice. Talk to me again when you have fixed your attitude"
        )
        return False


def setup(intent_manager):
    Insult(intent_manager)
